import logging

from core.config.SimpleConfig import SimpleConfig

__author__ = 'kitru'

class CommConfig(SimpleConfig):
    """Get configuration from file for PLC  """

    def __init__(self):
        name = 'plc';
        SimpleConfig.__init__(self, name)
        self._logger.info('Read configuration file: ' + name)
        self.readConfiguration(name)

    def getConnectionConfig(self):
        """ Get common configuration from config file. If common section is missing raise  Configuration Exception  """
        logging.info('=== Read communication configuration ===')
        return self.getConfigBySection('connection')

    def getAxesAddresses(self):
        """ Addresses with axes possitions. may raise Configuration Exception  """
        logging.info('=== Read position addresses ===')
        return self.getConfigBySection('axes')

    def getStatusAddresses(self):
        """ Addresses with status words, may raise Configuration Exception """
        logging.info('=== Read status addresses ===')
        return self.getConfigBySection('status')



