import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_tcp as modbus_tcp

from Exceptions import ConfigurationException

from core.config.CommunicationConfig import CommunicationConfig
from logger import openLog, closeLog

import ctypes


COORD_SCALE = 100000000

__author__ = 'kitru'

class ModBusManager(object):
    def __init__(self, config):
        self._confDict = config
        self.openConnection()

    def openConnection(self):
        self._master = modbus_tcp.TcpMaster(host=self._confDict['host'], port=int(self._confDict['port']),
                                            timeout_in_sec=1)
        self.ID = int(self._confDict['slave id'])
        #        self._master._do_open()
        return self._master

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


PC_CONTROL = 1

class TelescopeState(object):
    """ Common telescope switchers state """

    def __init__(self, plcManager):
        self._plc = plcManager
        configs = CommunicationConfig()
        self._status = configs.getStatusAddresses()

    def getLabels(self):
        self._plc.logger.info('Read status lables')
        return self._status

    def readStatus(self):
        """ Read switchers state """
        ret = dict()
        for key in self._status:
            state = self._plc._conn.readFlag(self._status[key])
            ret[key] = state
        return ret


class TelescopeMode(object):
    def __init__(self, plcManager):
        self._plc = plcManager
        configs = CommunicationConfig()
        self._state = configs.getStateAddresses()

    def readConnectionStatus(self):
        return (self._plc._conn.readNumber16bit(self._state['comm_check']) == 1,
                self._plc._conn.readNumber16bit(self._state['comm_add_check']) == 1)

    def readMovingStatus(self):
        return self._plc._conn.readFlag(self._state['move_stop'])

    def readMovingFlag(self):
        return self._plc._conn.readFlag(self._state['moveable'])

    def readServiceMode(self):
        return  self._plc._conn.readNumber16bit(self._state['service_mode'])

    def readControlMode(self):
        return  self._plc._conn.readNumber16bit(self._state['control_mode'])

    def readTemperatures(self):
        return ((self._plc._conn.readTemp(self._state['temp_telescope'])),
                    (self._plc._conn.readTemp(self._state['temp_dome'])))


class TelescopePosition(object):
    def __init__(self, plcManager):
        self._plc = plcManager
        configs = CommunicationConfig()
        self._axes = configs.getAxesAddresses()

    def _readCoordinate(self, addr):
        """  Coordinate is scaled by 10^8
        Attr:
            addr - starting address, 2 words will be readed
        Return:
            coordinate in radians as float number
        """
        number = self._plc._conn.readNumber32bit(addr)
        return (float(number) / COORD_SCALE)

    def _writeCoordinate(self, addr, number):
        """  Coordinate is scaled by 10^8
        Attr:
            addr - starting address, 2 words will be used
            number - coordinate in radians
        """
        number = long(float(number) * COORD_SCALE)
        self._plc._conn.writeNumber32bit(addr, number)

    def getCurrentPosition(self):
        """ Returns current telescope position in radians """
        ra = self._readCoordinate(self._axes['ra_cur'])
        dec = self._readCoordinate(self._axes['dec_cur'])
        return ra, dec

    def getSetpointPosition(self):
        """ Returns setpoint telescope position in radians """
        ra = self._readCoordinate(self._axes['ra_task'])
        dec = self._readCoordinate(self._axes['dec_task'])
        return ra, dec

    def setSetpointPosition(self, ra, dec, ha, st):
        """ Store new setpoint position for telescope
        Attr:
            ra -  in radians
            dec - in radians
        """
        self._writeCoordinate(self._axes['ra_task'], ra)
        self._writeCoordinate(self._axes['dec_task'], dec)
        self._writeCoordinate(self._axes['ha_task'], ha)
        self._writeCoordinate(self._axes['st_task'], st)

    def getFocus(self):
        """ Get current and setpoint for focus from PLC
        Return:
            tuple(curFocus, taskFocus)"""
        cur = self._plc._conn.readNumber16bit(self._axes['focus_cur']) / 10.0
        task = self._plc._conn.readNumber16bit(self._axes['focus_task']) / 10.0
        return cur, task

    def setFocus(self, focus):
        """ Set new focus value """
        self._plc._conn.writeNumber16bit(self._axes['focus_task'], focus * 10.0)


class PLCManager(object):
    def __init__(self):
        try:
            configs = CommunicationConfig()
            self.logger = openLog('plc_manager')
            confDict = configs.getConnectionConfig()
            self.logger.info('Establishing connection')
            self._conn = ModBusManager(confDict)

            #Helpers to work with PLC
            self._state = TelescopeState(self)
            self._mode = TelescopeMode(self)
            self._position = TelescopePosition(self)

            self.logger.info('Connection established')
            self._alarms = configs.getAlarms()
        except modbus_tk.modbus.ModbusError as error:
            raise ConfigurationException(error.args, self.logger)
        except Exception as error:
            raise ConfigurationException(error.args, self.logger)

    def __del__(self):
        closeLog(self.logger)

    def getStateHelper(self):
        return self._state

    def getModeHelper(self):
        return self._mode

    def getPositionHelper(self):
        return self._position

    def isConnected(self):
        return self._conn._master._is_opened

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
        self.logger.info('Take telescope control')
        self._conn.writeNumber16bit(self._state['take_control'], PC_CONTROL)

    def startMoving(self):
        self.logger.info('start moving')
        self._conn.writeFlag(self._state['move_stop'], 1)

    def stopMoving(self):
        self.logger.info('stop moving')
        self._conn.writeFlag(self._state['move_stop'], 0)

    def close(self):
        self.logger.info("Close Communication connection")
        self.master.close()

