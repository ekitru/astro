import logging
from time import strftime
from posixpath import join
from core.logger import getLogPath

from Exceptions import   ClosingException
from core.LogThread import LogThread
from core.AlarmLogThread import AlarmLogThread
from core.Resources import Resources
from core.astronomy import rad2str, getHours, getDegrees
from core.config.TranslationConfig import TranslationConfig
import ephem

__author__ = 'kitru'

class Controller(object):
    def __init__(self):
        self.__initLogger()
        self.resources = Resources()
        lang = self.resources.config.getDefaultLanguage()
        self.codes = TranslationConfig(lang)

        plcManager = self.resources.plcManager
        self.object = ObjectRepresenter(self.resources.object)
        self.tsTimes = TimeRepresenter(self.resources.observer)
        self.tsMode = TelescopeModeRepresenter(plcManager.getModeHelper())
        self.tsStatus = TelescopeStateRepresenter(plcManager.getStateHelper())
        self.tsPosition = PositionRepresenter(plcManager.getPositionHelper())
        self.tsControl = ControlModeRepresenter(self.resources, self)


    def __initLogger(self):
        """ Initialize base system logger  """
        logPath = getLogPath()
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                            datefmt='%m-%d %H:%M',
                            filename=join(logPath, 'common.log'),
                            filemode='w')

    def initialization(self):
        """ Initialization for all components
        Opens DB connection and connection with PLCm also reads translation codes """
        #        try:
        logging.info('======= Program initialization =======')
        self.logThread = LogThread(self.resources)
        self.alarmLogThred = AlarmLogThread(self.resources)

    #        except ConfigurationException as ce:
    #            logging.info('Error during initialization occure', ce)
    #            raise InitializationException(ce)
    #        except Exception as e:
    #            logging.info('Error during initialization occure', e)
    #            raise InitializationException(e)


    def freeResources(self):
        """ free all resources, close all connections """
        try:
            logging.info('======= Program closing =======')
            self.logThread.stop()
            self.alarmLogThred.stop()
            del self.resources
        except Exception as e:
            raise ClosingException(e)

    def isConnected(self):
        return self.resources.plcManager.isConnected()

    def forceLog(self):
        """ Force to log message and start new timer  """
        self.logThread.force()

    def updateLogTime(self, time):
        """ update logging period, time in minutes """
        self.logThread.updatePeriod(int(time) * 60)


# Presenters
class ObjectRepresenter(object):
    """ Sky Object representation """

    def __init__(self, starObject):
        """ object - astronomy object """
        self._object = starObject

    def isSelected(self):
        return self._object.selected()

    def getData(self):
        """ Return dictionary of object data
        Return:
            dict(name, ra, dec) for epoch 2000 """
        name = self._object.getName()
        position = self._object.getOriginalPosition()
        ra, dec = rad2str(*position)
        return {'name': name, 'ra': ra, 'dec': dec}

    def getCurrentPosition(self):
        """ Return current equatorial and horizontl position """
        coord = self._object.getEquatorialPosition()
        ra, dec = rad2str(*coord)
        alt, az = self._object.getHorizontalPosition()
        return {'ra': ra, 'dec': dec, 'alt': str(alt), 'az': str(az)}

    def getHA(self):
        """ Objects current HA value (HH:MM:SEC) normalized to [0;2PI) """
        ha = self._object.getCurrentHA()
        return str(ha)

    def getRiseSetTimes(self):
        """ Object rising nd setting times """
        rt = self._parseTime(self._object.getRisingTime())
        st = self._parseTime(self._object.getSettingTime())
        return {'rise': rt, 'set': st}

    def getExpositionTime(self):
        time = self._object.getExpositionTime()
        if time:
            expTime = self._roundTime(str(time))
        else:
            expTime = 'N/A'
        return expTime

    def _parseTime(self, time):
        if time:
            return str(time.strftime('%H:%M:%S'))
        else:
            return 'N/A'

    def _roundTime(self, time):
        return time.split(".")[0]

    def isAccessible(self):
        alt, az = self._object.getHorizontalPosition()
        horizon = self._object.getHorizon()
#        print('alt '+str(alt)+' and horizon '+str(horizon))
        if alt.real>horizon.real:
            return 'pObjVisible'
        else:
            return 'pObjNotVisible'



class TimeRepresenter(object):
    """ Local time representation """

    def __init__(self, observer):
        self._observer = observer

    def getCurrentTimes(self):
        return self._observer.getCurrentTimes()

    def getLocalTime(self):
        """ Local time system time ZONE HOURS:MIN:SEC """
        return  str(strftime("%Z %H:%M:%S"))

    def getUTC(self):
        utc = self._observer.getUTC()
        return str(utc)

    def getLST(self):
        """ Local sidereal time  for observation point """
        lst = self._observer.getLST()
        return str(lst)

    def getJulianDay(self):
        """ current julian date """
        jd = self._observer.getJulianDate()
        return str(jd)


class TelescopeModeRepresenter(object):
    """ Telescope mode and statuses representer  """
    conStat1 = [False,False]
    conStat2 = [False,False]

    def __init__(self, modeHelper):
        self._mode = modeHelper

    def getLabels(self):
        return ['pCommCheck1', 'pCommCheck2', 'pMovable', 'pMoveStop',
                'pState_service_mode', 'pState_control_mode', 'pState_tempT', 'pState_tempD']

    def readStatus(self):
        """ Return telescope modes and statuses
        dict(key, status)
        """
        status = dict()
        try:
            flags = self._mode.readConnectionStatus()
            connState = self._getConnStatus(flags)

            status['pCommCheck1'] = connState[0]
            status['pCommCheck2'] = connState[1]
            status['pMoveStop'] = self._getMovingStatus()
            status['pMovable'] = self._getMovingFlag()
            status['pState_service_mode'] = self._getServiceMode()
            status['pState_control_mode'] = self._getControlMode()
            status['pState_tempT'] = self._getTubeTemp()
            status['pState_tempD'] = self._getDomeTemp()
        except Exception as e:
            print(e)
        return status

    def _getConnStatus(self, status):
        self.conStat1[0], self.conStat2[0] = status[0], status[1]
        status = self.conStat1[0] ^ self.conStat1[1], self.conStat2[0] ^ self.conStat2[1]
        self.conStat1[1], self.conStat2[1] = self.conStat1[0], self.conStat2[0]
        return self._translateStatus(status[0]), self._translateStatus(status[1])

    def _translateStatus(self, state):
        if state:
            return 'pCommStatus_ok'
        else:
            return 'pCommStatus_broken'



    def _getMovingStatus(self):
        if self._mode.readMovingStatus():
            return 'pMoving'
        else:
            return 'pStopping'

    def _getMovingFlag(self):
        if self._mode.readMovingFlag():
            return 'pMovableTrue'
        else:
            return 'pMovableFalse'

    def _getServiceMode(self):
        mode = self._mode.readServiceMode()
        if mode is 1:
            ret = 'pState_online'
        elif mode is 2:
            ret = 'pState_service'
        else:
            ret = 'pState_unknown_service_state'
        return ret

    def _getControlMode(self):
        mode = self._mode.readControlMode()
        if mode is 1:
            ret = 'pState_PC'
        elif mode is 2:
            ret = 'pState_Obs_room'
        elif mode is 3:
            ret = 'pState_Scope_room'
        elif mode is 4:
            ret = 'pState_Remote_control'
        else:
            ret = 'pState_nobody'
        return ret

    def _getTubeTemp(self):
        return str(self._mode.readTemperatures()[0])

    def _getDomeTemp(self):
        return str(self._mode.readTemperatures()[1])


class TelescopeStateRepresenter(object):
    """ Telescope state representer """

    def __init__(self, stateHelper):
        self._state = stateHelper

    def getLabels(self):
        """ Status labels are taken from section [status] in plc.conf """
        labels = self._state.getLabels().keys()
        labels.sort()
        return labels

    def readStatus(self):
        """ Return telescope statuses
        dict(key, status)
        """
        status = dict()
        try:
            status = self._state.readStatus()
            for key in status:
                if status[key] is 1:
                    temp = 'On'
                else:
                    temp = 'Off'
                status[key] = str(temp)
        except Exception as e:
            print(e)
        return status


class PositionRepresenter(object):
    """ Current telescope and setpoint position  """

    def __init__(self, positionHelper):
        self._position = positionHelper

    def getCurrentHourAngle(self):
        try:
            ha = self._position.getCurrentHourAngle()
            ha = getHours(ha)
        except Exception as e:
            ha = None
            self._position.logger.exception(e)
        return str(ha)

    def getTaskHourAngle(self):
        try:
            ha = self._position.getTaskHourAngle()
            ha = getHours(ha)
        except Exception as e:
            ha = None
            self._position.logger.exception(e)
        return str(ha)

    def getCurrentPosition(self):
        try:
            ra, dec = self._position.getCurrentPosition()
        except Exception as e:
            ra, dec = None, None
            self._position.logger.exception(e)
        return self._parseCoordinates(ra, dec)

    def getSetpointPosition(self):
        """ dict(position, value), keys 'ra','dec' """
        try:
            ra, dec = self._position.getSetpointPosition()
#            print(ra, dec)
        except Exception as e:
            ra, dec = None, None
            self._position.logger.exception(e)
        return self._parseCoordinates(ra, dec)

    def _parseCoordinates(self, ra, dec):
        if ra is not None and dec is not None:
            position = rad2str(ra, dec)
        else:
            position = '##:##:##', '##:##:##'
        return {'ra': position[0], 'dec': position[1]}

    def getFocus(self):
        try:
            current = self._position.getFocus()
        except Exception:
            current = None
        return str(current)

    def getDomePosition(self):
        cur, task = self._position.getDomePosition()
        cur = str(getDegrees(cur))
        task = str(getDegrees(task))
        print(cur,task)
        pos = dict()
        pos['cur'] = cur.split(':')[0]+':'+cur.split(':')[1]
        pos['task'] = task.split(':')[0]+':'+task.split(':')[1]
        return pos

class ControlModeRepresenter():
    def __init__(self, resources, controller):
        self._res = resources
        self.controller = controller
        self._taskRa = 0

    def updateSetPointByObjectCoordinates(self):
        object = self._res.object
        setPoint = self._res.setPoint

        if object.selected():
            ra,dec = object.getEquatorialPosition() #FIX set position with defraction correction
            setPoint.setPosition(ra, dec)

    def getCurrentSetPoint(self):
        return self._res.setPoint.getRawData()

    def getCurrentST(self):
        time = ephem.hours(self._res.observer.getLST()).real
        return time

    def getCurrentHA(self):
        st = self.getCurrentST()
        return ephem.hours(st-self._taskRa).norm.real

    def sendPosition(self, data):
        plc = self._res.plcManager
        plc.getPositionHelper().setSetpointPosition(ra=data['ra'], dec=data['dec'])
        self._taskRa = data['ra']


    def sendLST(self):
        plc = self._res.plcManager
#        print('Send new LST: ',self.getCurrentST())
        plc.getPositionHelper().setST(self.getCurrentST())

    def sendHA(self):
        plc = self._res.plcManager
#        print('Send new HA: ',self.getCurrentHA())
        plc.getPositionHelper().setTaskHA(self.getCurrentHA())

    def setNewSetPoint(self):
        data = self.getCurrentSetPoint()
#        print('RA', getHours(data['ra']), 'DEC', getDegrees(data['dec']))
        self.sendPosition(data)
        self.sendLST()
        self.sendHA()


    def isRemoveControl(self):
        return self._res.plcManager.getModeHelper().readControlMode() is not 1

    def takeControl(self):
        plc = self._res.plcManager
        plc.takeControl()

    def isMovable(self):
        return self._res.plcManager.getModeHelper().readMovingFlag()

    def isMoving(self):
        plc = self._res.plcManager
        return plc.getModeHelper().readMovingStatus()

    def startMoving(self):
        plc = self._res.plcManager
        plc.startMoving()
        self.controller.forceLog()

    def stopMoving(self):
        plc = self._res.plcManager
        plc.stopMoving()

    def sendTimes(self):
        self.sendLST()
        self.sendHA()
