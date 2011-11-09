import logging

from core.config.SimpleConfig import SimpleConfig

__author__ = 'kitru'

class CommunicationConfig(SimpleConfig):
    """Get configuration file for PLC  """

    def __init__(self):
        """  Reads plc ocnfiguration file and opens new logger  """
        name = 'plc'
        SimpleConfig.__init__(self, name)
        self.readConfiguration(name)

    def getConnectionConfig(self):
        """ Get common configuration from config file. If common section is missing raise  Configuration Exception  """
        logging.info('=== Read communication configuration ===')
        return self.getConfigBySection('connection')

    def getAxesAddresses(self):
        """ Addresses with axes possitions. may raise Configuration Exception  """
        logging.info('=== Read position addresses ===')
        return self.getConfigBySection('axes')

    def getStateAddresses(self):
        """ Addresses with state words, may raise Configuration Exception """
        logging.info('=== Read status addresses ===')
        return self.getConfigBySection('state')

    def getStatusAddresses(self):
        """ Addresses with status words, may raise Configuration Exception """
        logging.info('=== Read status addresses ===')
        return self.getConfigBySection('status')

    def getAlarms(self):
        """ Addresses of alarms, may raise Configuration Exception """
        logging.info('=== Read alarms  ===')
        return self.getConfigBySection('alarms')



