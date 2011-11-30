from posixpath import join
import logging
from time import strftime
import ephem

from Exceptions import   ClosingException
from LogThread import LogThread
from core.Resources import Resources
from core.astronomy import rad2str, getHours, getDegrees
from core.config.TranslationConfig import TranslationConfig
from core.logger import getLogPath

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
        self.tsControl = ControlModeRepresenter(self.resources)

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
        self._object = starObject;

    def isSelected(self):
        return self._object.selected()

    def getData(self):
        """ Return dictionary of object data
        Return:
            dict(name, ra, dec) for epoch 2000 """
        name = self._object.getName()
        position = self._object.getPosition()
        ra, dec = rad2str(*position)
        return {'name': name, 'ra': ra, 'dec': dec}

    def getPosition(self):
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
        time = self._object.getExpositionTime() or 'N/A'
        return str(time)

    def _parseTime(self, time):
        if time:
            return str(time.strftime('%H:%M:%S'))
        else:
            return 'N/A'


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

    def __init__(self, modeHelper):
        self._mode = modeHelper

    def getLabels(self):
        return ['pCommCheck1', 'pCommCheck2', 'pMoveable', 'pMoveStop',
                'pState_service_mode', 'pState_control_mode', 'pState_tempT', 'pState_tempD']

    def readStatus(self):
        """ Return telescope modes and statuses
        dict(key, status)
        """
        status = dict()
        try:
            stat = self._mode.readConnectionStatus()
            status['pCommCheck1'] = str(stat[0])
            status['pCommCheck2'] = str(stat[1])
            status['pMoveStop'] = self._getMovingStatus()
            status['pMoveable'] = self._getMovingFlag()
            status['pState_service_mode'] = self._getServiceMode()
            status['pState_control_mode'] = self._getControlMode()
            status['pState_tempT'] = self._getTubeTemp()
            status['pState_tempD'] = self._getDomeTemp()
        except Exception as e:
            print(e)
        return status

    def _getMovingStatus(self):
        if self._mode.readMovingStatus():
            return 'pMoving'
        else:
            return 'pStopping'

    def _getMovingFlag(self):
        if self._mode.readMovingFlag():
            return 'pMoveableTrue'
        else:
            return 'pMoveableFalse'

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

    def getCurrentPosition(self):
        """ dict(position, value), keys 'ra','dec' """
        try:
            ra, dec = self._position.getCurrentPosition()
        except Exception as e:
            ra, dec = None, None
            self._position.logger.exception(e)
        return self._parsePosition(ra, dec)

    def getSetpointPosition(self):
        """ dict(position, value), keys 'ra','dec' """
        try:
            ra, dec = self._position.getSetpointPosition()
            print(ra, dec)
        except Exception as e:
            ra, dec = None, None
            self._position.logger.exception(e)
        return self._parsePosition(ra, dec)

    def _parsePosition(self, ra, dec):
        if ra is not None and dec is not None:
            position = rad2str(ra, dec)
        else:
            position = '##:##:##', '##:##:##'
        return {'ra': position[0], 'dec': position[1]}

    def getFocus(self):
        try:
            current, task = self._position.getFocus()
        except Exception:
            current, task = None, None
        return {'cur': str(current), 'task': str(task)}

    def setST(self, st):
        self._position.setST(self, st)

    def setHA(self, ha):
        self._position.setHA(self, ha)


class ControlModeRepresenter():
    def __init__(self, resources):
        self._res = resources

    def updateSetPoint(self):
        self._res.updateSetPoint()

    def getCurrentSetPoint(self):
        return self._res._setPoint.getRawData()

    def getCurrentST(self):
        time = ephem.hours(self._res.observer.getLST()).real
        return time

    def getCurrentHA(self):
        data = self.getCurrentSetPoint()
        ra = data['ra']
        st = self.getCurrentST()
        return ephem.hours(st-ra).norm.real

    def sendPosition(self, data):
        plc = self._res.plcManager
        plc.getPositionHelper().setSetpointPosition(ra=data['ra'], dec=data['dec'])

    def sendFocus(self, focus):
        plc = self._res.plcManager
        if focus:
            plc.getPositionHelper().setFocus(focus)

    def sendLST(self):
        plc = self._res.plcManager
        print('Send new LST: ',self.getCurrentST())
        plc.getPositionHelper.setST(self.getCurrentST())

    def sendHA(self):
        plc = self._res.plcManager
        print('Send new HA: ',self.getCurrentHA())
        plc.getPositionHelper.setHA(self.getCurrentHA())

    def setNewSetPoint(self):
        data = self.getCurrentSetPoint()
        print('RA', getHours(data['ra']), 'DEC', getDegrees(data['dec']))

        self.sendPosition(data)
        self.sendFocus(data['focus'])
        #        plc.getPositionHelper.setST(data['st'])
        self.sendLST()
        #        plc.getPositionHelper.setHA(data['ha'])
        self.sendHA()


    def isRemoveControl(self):
        return self._res.plcManager.getModeHelper().readControlMode() is not 1

    def takeControl(self):
        plc = self._res.plcManager
        plc.takeControl()

    def isMoveable(self):
        return self._res.plcManager.getModeHelper().readMovingFlag()

    def startMoving(self):
        plc = self._res.plcManager
        plc.startMoving()

    def stopMoving(self):
        plc = self._res.plcManager
        plc.stopMoving()

    def sendTimes(self):
        self.sendLST()
        self.sendHA()
