import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_tcp as modbus_tcp
from Exceptions import ConfigurationException
from logger import getLog

__author__ = 'kitru'

class PLCManager(object):
    def __init__(self, confDict):
        self.logger = getLog('comm')
        self.logger.info('Establishing connection')
        try:
            #Connect to the slave
            self.master = modbus_tcp.TcpMaster(host=confDict['host'], port=confDict['port'])
            self.ID = confDict['slave id']
            self.logger.info('Connection established')
        except modbus_tk.modbus.ModbusError as error:
            raise ConfigurationException(error.args, self.logger)

    def test(self):
        self.master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 100, output_value=xrange(12))
        print self.master.execute(1, cst.READ_HOLDING_REGISTERS, 100, 12)

        self.master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 44, output_value=xrange(20))
        print self.master.execute(1, cst.READ_HOLDING_REGISTERS, 60, 1)

    def getPosition(self):
        """ Return current and aim positions from PLC in radians """
        return (0.231, -0.0123), (0.231, -0.0123) #TODO make real in future

    def getFocus(self):
        """ Return current and aim focus from PLC in radians
        """
        return 0.3, 0.1 #TODO make real in future

    def close(self):
        self.logger.info("Close Communication connection")
        self.master.close()