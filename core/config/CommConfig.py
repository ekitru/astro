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
        logging.info('=== Read communication configuratio ===')
        return self.getConfigBySection('connection')


