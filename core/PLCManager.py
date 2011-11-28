import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_tcp as modbus_tcp

from Exceptions import ConfigurationException

from core.astronomy import rad2str
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
        self._master = modbus_tcp.TcpMaster(host=self._confDict['host'], port=int(self._confDict['port']), timeout_in_sec=0.2)
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

class PLCManager(object):
    def __init__(self):
        try:
            configs = CommunicationConfig()
            self._logger = openLog('plc_manager')
            self._logger.info('Establishing connection')
            confDict = configs.getConnectionConfig()
            self._conn = ModBusManager(confDict)
            self._logger.info('Connection established')

            self._axes = configs.getAxesAddresses()
            self._status = configs.getStatusAddresses()
            self._state = configs.getStateAddresses()
            self._alarms = configs.getAlarms()
        except modbus_tk.modbus.ModbusError as error:
            raise ConfigurationException(error.args, self._logger)
        except Exception as error:
            raise ConfigurationException(error.args, self._logger)

    def __del__(self):
        closeLog(self._logger)

    def readCoordinate(self, addr):
        """  Coordinate is scaled by 10^8
        Attr:
            addr - starting address, 2 words will be readed
        Return:
            coordinate in radians as float number
        """
        number = self._conn.readNumber32bit(addr)
        return (float(number) / COORD_SCALE)

    def writeCoordinate(self, addr, number):
        """  Coordinate is scaled by 10^8
        Attr:
            addr - starting address, 2 words will be used
            number - coordinate in radians
        """
        number = long(float(number) * COORD_SCALE)
        self._conn.writeNumber32bit(addr, number)


    def getPosition(self):
        """ Get current ant setpoint position from PLC as strings
        Return:
            tuple((str(curRA),str(curDEC)),(str(taskRA),str(taskDEC)))"""
        curRa, curDec = self.getCurrentPosition()
        taskRa, taskDec = self.getSetpointPosition()

        return rad2str(curRa, curDec), rad2str(taskRa, taskDec)

    def getCurrentPosition(self):
        """ Returns current telescope position in radians """
        curRa = self.readCoordinate(self._axes['ra_cur'])
        curDec = self.readCoordinate(self._axes['dec_cur'])
        return curRa, curDec

    def getSetpointPosition(self):
        """ Returns setpoint telescope position in radians """
        taskRa = self.readCoordinate(self._axes['ra_task'])
        taskDec = self.readCoordinate(self._axes['dec_task'])
        return taskRa, taskDec

    def setSetpointPosition(self, ra, dec, ha, st):
        """ Store new setpoint position for telescope
        Attr:
            ra -  in radians
            dec - in radians
        """
        self.writeCoordinate(self._axes['ra_task'], ra)
        self.writeCoordinate(self._axes['dec_task'], dec)
        self.writeCoordinate(self._axes['ha_task'], ha)
        self.writeCoordinate(self._axes['st_task'], st)

    def getFocus(self):
        """ Get current and setpoint for focus from PLC as strings
        Return:
            tuple(str(curFocus), str(taskFocus))"""
        cur = self._conn.readNumber16bit(self._axes['focus_cur']) / 10.0
        task = self._conn.readNumber16bit(self._axes['focus_task']) / 10.0
        return cur, task

    def setFocus(self, focus):
        """ Set new focus value """
        self._conn.writeNumber16bit(self._axes['focus_task'], focus * 10.0)


    def readTelescopeStatus(self):
        ret = dict()
        for key in self._status:
            state = self._conn.readFlag(self._status[key])
            if state == 1:
                state = 'On'
            else:
                state = 'Off'

            ret[key] = state
        return ret

    def readAlarms(self):
        ret = dict()
        for key in self._alarms:
            state = self._conn.readFlag(self._alarms[key])
            if state == 1:
                ret[key] = 'On'

        return ret


    def readConnectionStatus(self):
        return (self._conn.readNumber16bit(self._state['comm_check']) == 1, self._conn.readNumber16bit(self._state['comm_add_check']) == 1)

    def readMovingStatus(self):
        return self._conn.readFlag(self._state['move_stop'])

    def readMovingFlag(self):
        return self._conn.readFlag(self._state['moveable'])

    def readTelescopeMode(self):
        """ Get current telescope  service and control modes
        Return:
            dict(pState_service_mode,pState_control_mode)
        """
        return {'pState_service_mode':self.readServiceMode() ,'pState_control_mode':self.readControlMode()}

    def readServiceMode(self):
        serviceMode =  self._conn.readNumber16bit(self._state['service_mode'])
        serviceModes = {'0': 'pState_unknown_service_state', '1': 'pState_online', '2': 'pState_service'}
        return serviceModes[str(serviceMode)]

    def readControlMode(self):
        controlMode =  self._conn.readNumber16bit(self._state['control_mode'])
        controlModes = {'0': 'pState_nobody', '1': 'pState_PC', '2': 'pState_Obs_room', '3': 'pState_Scope_room', '4': 'pState_Remote_control'}
        return controlModes[str(controlMode)]

    def readTemperature(self):
        ret = dict()
        ret['pState_tempT'] = str(self._conn.readTemp(self._state['temp_telescope']))
        ret['pState_tempD'] = str(self._conn.readTemp(self._state['temp_dome']))
        return ret

    def readCommonAlarmStatus(self):
        try:
            state = self._conn.readFlag(self._status['alarmCommon2'])
        except Exception as ex:
            print(ex)
        state = 1
        if state == 1:
            return 'Fault'
        else:
            return 'Normal'

    def readAlarmStatus(self):
        alarms = self.readAlarms()
        keys = alarms.keys()
        list = []
        for key in keys:
            list.append(self._alarms[key])
        status = ",".join(list)
        return status

    def takeControl(self):
        self._logger.info('Take telescope control')
        self._conn.writeNumber16bit(self._state['take_control'], PC_CONTROL)

    def startMoving(self):
        self._logger.info('start moving')
        self._conn.writeFlag(self._state['move_stop'], 1)

    def stopMoving(self):
        self._logger.info('stop moving')
        self._conn.writeFlag(self._state['move_stop'], 0)

    def close(self):
        self._logger.info("Close Communication connection")
        self.master.close()

