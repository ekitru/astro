import ephem
import modbus_tk.defines as cst
import modbus_tk.modbus_tcp as modbus_tcp
from core.astronomy import normRa

from core.config.CommunicationConfig import CommunicationConfig
from logger import openLog, closeLog

import ctypes


COORD_SCALE = 100000000

__author__ = 'kitru'

class ModBusManager(object):
    def __init__(self, config):
        self._confDict = config
        self._master = self.openConnection()

    def openConnection(self):
        master = modbus_tcp.TcpMaster(host=self._confDict['host'], port=int(self._confDict['port']), timeout_in_sec=0.1)
        self.ID = int(self._confDict['slave id'])
#        master._do_open()
        return master

    def _mergeNumber(self, words):
        """ Merge two 16bit numbers into single 32 bit: words[0] - R16H, words[1] - R16L
        Attr:
            tuple of two number
        Return:
            32bit long number
        """
        nible1 = (words[0] & 0xffff) << 16
        nible2 = (words[1] & 0xffff)
        number = nible1 | nible2
        return ctypes.c_int32(number).value

    def _splitNumber(self, number):
        """ Split  32bit long number into two 16bit numbers: words[0] - R16H, words[1] - R16L
        Attr:
            32bit long number
        Return:
            tuple of two 16bit number
        """
        regA = (number >> 16) & 0xffff
        regB = number & 0xffff
        return int(regA), int(regB)

    def readNumber16bit(self, addr):
        """ Reads 16bit number as long from PLC.
        Attr:
            addr - address
        Return:
            long number
        """
        number = self._master.execute(self.ID, cst.READ_HOLDING_REGISTERS, long(addr), 1)[0]
        return ctypes.c_int16(number).value

    def writeNumber16bit(self, addr, number):
        """ Writes 16bit number to PLC.
        Attr:
            addr - address
            number - long number
        """
        self._master.execute(self.ID, cst.WRITE_MULTIPLE_REGISTERS, long(addr), output_value=(long(number),))


    def readNumber32bit(self, addr):
        """ Reads 32bit number as long from PLC. Due to 16bit limitation of Modbus protocol, number=addr<<16 && (addr+1).
        Attr:
            addr - starting address, 2 words will be readed
        Return:
            long number
        """
        words = self._master.execute(self.ID, cst.READ_HOLDING_REGISTERS, long(addr), 2)
        number = self._mergeNumber(words)
        return number

    def writeNumber32bit(self, addr, number):
        """ Writes 32bit number to PLC. Due to 16bit limitation of Modbus protocol, number=addr<<16 && (addr+1).
        Attr:
            addr - starting address, 2 words are used
            number - long number
        """
        words = self._splitNumber(number)
        self._master.execute(self.ID, cst.WRITE_MULTIPLE_REGISTERS, long(addr), output_value=words)

    def readFlag(self, addr):
        """ Reads flag from PLC
        Attr:
            addr - reading flags
        Return:
            True, False
        """
        return self._master.execute(self.ID, cst.READ_COILS, long(addr), 1)[0]

    def writeFlag(self, addr, value):
        """ Writes boolean flag  """
        self._master.execute(self.ID, cst.WRITE_SINGLE_COIL, long(addr), output_value=value)

    def readTemp(self, addr):
        """ Read temperatuer from PLC """
        return self.readNumber16bit(long(addr)) / 10.0


class PLCManager(object):
    def __init__(self):
        configs = CommunicationConfig()
        self.logger = openLog('plc_manager')
        confDict = configs.getConnectionConfig()
        self.logger.info('Establishing connection')
        self._conn = ModBusManager(confDict)
        self.logger.info('Connection established')

        #Helpers to work with PLC
        self.logger.info('Open helpers')
        self._stateHelper = StateHelper(self._conn, configs, self.logger)
        self._modeHelper = ModeHelper(self._conn, configs, self.logger)
        self._positionHelper = PositionHelper(self._conn, configs, self.logger)
        self._alarmHelper = AlarmHelper(self._conn, configs, self.logger)
        self.logger.info('Helpers are done')

        self._alarms = configs.getAlarms()
        self._state = configs.getStateAddresses()

    def __del__(self):
        closeLog(self.logger)

    def getStateHelper(self):
        """ Return the state helper
        @rtype StateHelper
        """
        return self._stateHelper

    def getModeHelper(self):
        """ Return the state helper
        @rtype ModeHelper
        """
        return self._modeHelper

    def getPositionHelper(self):
        """ Return the state helper
        @rtype PositionHelper
        """
        return self._positionHelper

    def getAlarmHelper(self):
        """ Return the alarm helper
        @rtype AlarmHelper
        """
        return self._alarmHelper

    def isSwitchedOn(self):
        if self.isConnected() and self._conn.readFlag(1030) is 1: #TODO switcher check is hardcoded!
            return True
        else:
            return False

    def isConnected(self):
        self._dummyRead()
        return self._conn._master._is_opened


    def _dummyRead(self):
        try:
            self._conn.readFlag(1000)
        except Exception:
            pass

    # =====================================


    def readAlarms(self):
        ret = dict()
        for key in self._alarms:
            state = self._conn.readFlag(self._alarms[key])
            if state == 1:
                ret[key] = 'On'

        return ret

    def readAlarmStatus(self):
        alarms = self.readAlarms()
        keys = alarms.keys()
        list = []
        for key in keys:
            list.append(self._alarms[key])
        status = ",".join(list)
        return status

    # Telescope controlling
    def takeControl(self):
        self.logger.info('Take control')
        self._conn.writeNumber16bit(self._state['take_control'], 1)

    def startMoving(self):
        self.logger.info('Start moving')
        self._conn.writeFlag(self._state['move'], 1)

    def stopMoving(self):
        self.logger.info('Stop moving')
        self._conn.writeFlag(self._state['stop'], 1)

    def close(self):
        self.logger.info("Close Communication connection")
        self.master.close()


class BaseHelper(object):
    def __init__(self, connection, logger):
        self._conn = connection
        self.logger = logger

    def isConnected(self):
        self._dummyRead()
        return self._conn._master._is_opened

    def _dummyRead(self):
        try:
            self._conn.readFlag(1000)
        except Exception:
            pass

class StateHelper(BaseHelper):
    """ Common telescope switchers state """

    def __init__(self, connection, config, logger):
        BaseHelper.__init__(self, connection, logger)
        self._status = config.getStatusAddresses()

    def getLabels(self):
        self.logger.info('Read status lables')
        return self._status

    def readStatus(self):
        """ Read switchers state """
        ret = dict()
        for key in self._status:
            state = self._conn.readFlag(self._status[key])
            ret[key] = state
        return ret


class ModeHelper(BaseHelper):
    def __init__(self, connection, config, logger):
        BaseHelper.__init__(self, connection, logger)
        self._state = config.getStateAddresses()

    def readConnectionStatus(self):
        return (self._conn.readNumber16bit(self._state['comm_check']) == 1,
                self._conn.readNumber16bit(self._state['comm_add_check']) == 1)

    def readMovingStatus(self):
        if self.isConnected():
            return self._conn.readFlag(self._state['move'])
        else:
            return False

    def readMovingFlag(self):
        return self._conn.readFlag(self._state['moveable'])

    def readServiceMode(self):
        return  self._conn.readNumber16bit(self._state['service_mode'])

    def readControlMode(self):
        return  self._conn.readNumber16bit(self._state['control_mode'])

    def readTemperatures(self):
        return ((self._conn.readTemp(self._state['temp_telescope'])),
                    (self._conn.readTemp(self._state['temp_dome'])))


class PositionHelper(BaseHelper):
    def __init__(self, connection, config, logger):
        BaseHelper.__init__(self, connection, logger)
        self._axes = config.getAxesAddresses()

    def _readCoordinate(self, addr):
        """  Coordinate is scaled by 10^8
        Attr:
            addr - starting address, 2 words will be readed
        Return:
            coordinate in radians as float number
        """
        number = self._conn.readNumber32bit(addr)
        return (float(number) / COORD_SCALE)

    def _writeCoordinate(self, addr, number):
        """  Coordinate is scaled by 10^8
        Attr:
            addr - starting address, 2 words will be used
            number - coordinate in radians
        """
        #        print('write coordinate to'+str(addr),number)
        number = long(float(number) * COORD_SCALE)
        self._conn.writeNumber32bit(addr, number)

    def getCurrentHourAngle(self):
        return self._readCoordinate(self._axes['ha_cur'])

    def getTaskHourAngle(self):
        return self._readCoordinate(self._axes['ha_task'])

    def getCurrentPosition(self):
        """ Returns current telescope position in radians """
        #TODO ask Ivan ra = self._readCoordinate(self._axes['ra_cur'])
        raw_ra = self._readCoordinate(self._axes['st_task']) - self.getCurrentHourAngle()
        ra = normRa(ephem.hours(raw_ra))
#        print("orig: "+str(raw_ra)+" norm: "+str(ra.real))
        dec = self._readCoordinate(self._axes['dec_cur'])
        return ra.real, dec

    def getSetpointPosition(self):
        """ Returns setpoint telescope position in radians """
        ra = self._readCoordinate(self._axes['ra_task'])
        dec = self._readCoordinate(self._axes['dec_task'])
        return ra, dec

    def setSetpointPosition(self, ra, dec):
        """ Store new setpoint position for telescope
        Attr:
            ra -  in radians
            dec - in radians
        """
        self.logger.info('Set new setpoint')
        self.logger.info('RA: ' + str(ra) + ', DEC: ' + str(dec))
#        print('RA: ' + str(ra) + ', DEC: ' + str(dec))
        self._writeCoordinate(self._axes['ra_task'], ra)
        self._writeCoordinate(self._axes['dec_task'], dec)

    def setTaskHA(self, ha):
        self._writeCoordinate(self._axes['ha_task'], ha)

    def setST(self, st):
        self._writeCoordinate(self._axes['st_task'], st)

    def getFocus(self):
        """ Get current focus from PLC """
        cur = self._conn.readNumber32bit(self._axes['focus_cur']) / 100.0
        return cur

    def getDomePosition(self):
        """ Get dome positions: current and task """
        cur = self._readCoordinate(self._axes['dome_cur'])
        task = self._readCoordinate(self._axes['dome_task'])
        return cur, task

class AlarmHelper(BaseHelper):
    """ Alarm history helper"""

    def __init__(self, connection, config, logger):
        BaseHelper.__init__(self, connection, logger)
        self._alarm = config.getAlarmsAddresses()
        print(self._alarm)


    def getNextAlarm(self):
        isAlarm = self._alarm['newalarm']
        if self._conn.readNumber16bit(isAlarm) is 1:
            print('Get new alarm')
            time = self._getTime()
            id = self._getID()
            status = self._getStatus()
            print('ID: '+str(id)+" status: "+str(status)+" time: "+str(time))
            self._conn.writeNumber16bit(isAlarm, 0)
            return id,status,time

    def _getID(self):
        return int(self._conn.readNumber16bit(self._alarm['id']))

    def _getStatus(self):
        status = self._conn.readNumber16bit(self._alarm['status'])
        if status is 20:
            return True
        elif status is 10:
            return False
        else:
            return None

    def _getTime(self):
        time = self._conn.readNumber32bit(self._alarm['time'])
        return int(time)


