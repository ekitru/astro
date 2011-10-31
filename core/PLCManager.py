import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_tcp as modbus_tcp

from Exceptions import ConfigurationException

from core.astronomy import rad2str
from core.config.CommConfig import CommConfig
from logger import openLog, closeLog

import ctypes


COORD_SCALE = 100000000

__author__ = 'kitru'

class PLCManager(object):
    def __init__(self):
        try:
            commConfig = CommConfig()
            self._logger = openLog('plc_comm')
            self._logger.info('Establishing connection')
            #Connect to the slave
            confDict = commConfig.getConnectionConfig()
            self.master = modbus_tcp.TcpMaster(host=confDict['host'], port=int(confDict['port']))
            self.ID = int(confDict['slave id'])
            self.master._do_open()
            self._logger.info('Connection established')

            self._logger.info('Start to reading addresses')
            self.axes =  commConfig.getAxesAddresses()

        except modbus_tk.modbus.ModbusError as error:
            raise ConfigurationException(error.args, self._logger)
        except Exception as error:
            raise ConfigurationException(error.args, self._logger)

        self.mockCurRA = 0.231
        self.mockCurDEC = -0.0123
        self.mockCurFoc = 0.3
        self.mockTaskRA = 0.301
        self.mockTaskDEC = -0.0102
        self.mockTaskFoc = 0.1
        self.mockPCMode = True

    def __del__(self):
        closeLog(self._logger)

    def _mergeNumber(self, words):
        """ Merge two 16bit numbers into single 32 bit: words[0] - R16H, words[1] - R16L
        Attr:
            tuple of two number
        Return:
            32bit long number
        """
        nible1 = (words[0]&0xffff) << 16
        nible2 = (words[1]&0xffff)
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

    def readNumber32bit(self, addr):
        """ Reads 32bit number as long from PLC. Due to 16bit limitation of Modbus protocol, number=addr<<16 && (addr+1).
        Attr:
            addr - starting address, 2 words will be readed
        Return:
            long number
        """
        words = self.master.execute(self.ID, cst.READ_HOLDING_REGISTERS, addr, 2)
        number = self._mergeNumber(words)
        return number

    def writeNumber32bit(self, addr, number):
        """ Writes 32bit number to PLC. Due to 16bit limitation of Modbus protocol, number=addr<<16 && (addr+1).
        Attr:
            addr - starting address, 2 words are used
            number - long number
        """
        words = self._splitNumber(number)
        self.master.execute(self.ID, cst.WRITE_MULTIPLE_REGISTERS, addr, output_value=words)


    def readCoordinate(self, addr):
        """  Coordinate is scaled by 10^8
        Attr:
            addr - starting address, 2 words will be readed
        Return:
            coordinate in radians as float number
        """
        number = self.readNumber32bit(int(addr))
        return (float(number) / COORD_SCALE)

    def writeCoordinate(self, addr, number):
        """  Coordinate is scaled by 10^8
        Attr:
            addr - starting address, 2 words will be used
            number - coordinate in radians
        """
        number = long(float(number) * COORD_SCALE)
        self.writeNumber32bit(int(addr), number)


    def test(self):
        self.master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 80, output_value=xrange(40))
        print self.master.execute(1, cst.READ_HOLDING_REGISTERS, 100, 12)

        self.master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 44, output_value=xrange(20))
        print self.master.execute(1, cst.READ_HOLDING_REGISTERS, 60, 1)

    def getPosition(self):
        """ Get current ant setpoint position from PLC as strings
        Return:
            tuple((str(curRA),str(curDEC)),(str(taskRA),str(taskDEC)))"""
        curRa,  curDec = self.getCurrentPosition()
        taskDec, taskRa = self.getSetpointPosition()

        return rad2str(curRa, curDec), rad2str(taskRa, taskDec)

    def getCurrentPosition(self):
        """ Return current telescope position in radians """
        curRa = self.readCoordinate(self.axes['ra_cur'])
        curDec = self.readCoordinate(self.axes['dec_cur'])
        return curRa, curDec

    def getSetpointPosition(self):
        taskRa = self.readCoordinate(self.axes['ra_task'])
        taskDec = self.readCoordinate(self.axes['dec_task'])
        return taskDec, taskRa

    def setSetpointPosition(self, ra, dec):
        """ Store new setpoint position for telescope
        Attr:
            ra -  in radians
            dec - in radians
        """
        self.writeCoordinate(self.axes['ra_task'], ra)
        self.writeCoordinate(self.axes['dec_task'], dec)


    def getFocus(self):
        """ Get current ant setpoint for focus from PLC as strings
        Return:
            tuple(str(curFocus), str(taskFocus))"""
        return self.mockCurFoc, self.mockTaskFoc #TODO make real in future

    def setPosition(self, (ra, dec)):
        self.mockTaskRA = ra
        self.mockTaskDEC = dec

    def setFocus(self, focus):
        self.mockTaskFoc = focus


    def close(self):
        self._logger.info("Close Communication connection")
        self.master.close()


    def isPCControl(self):
        """  Returns True if status flag read from PLC equals "1" (PC CONTROL selected)
             Returns False if status flag read from PLC equals "0" (REMOTE CONTROL selected)"""
        return self.mockPCMode #TODO real implementation

