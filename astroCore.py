import logging
from CommManager import CommManager
from DbManager import DbManager
from configuration import Configuration, ConfigurationException
from translations import Translate

__author__ = 'kitru'

class InitializationException(Exception):
    """Exception raised for errors during system initialization.
    Attributes:
        msg  -- explanation of the error
    """

    def __init__(self, msg, logger=None):
        Exception.__init__(self, msg)
        if logger:
            logger.error(msg)


class AstroController(object):
    def __init__(self):
        self.initialization()

    def initialization(self):
        try:
            config = self.openConfig('default.cnf')
            self.communication = self.openCommConfig(config)
            self.dbManager = self.openDbManager(config)
            self.transCodes = self.openTranslationCodes(config)
        except ConfigurationException as ce:
            print("Error during configuration occure:" + ce.__str__())
            raise InitializationException(ce)

    def openConfig(self, confFileName):
        logging.info('======= Program initialization =======')
        return Configuration(confFileName)

    def openCommConfig(self, config):
        logging.info('=== Communication initialization ===')
        return CommManager(config)

    def openDbManager(self, config):
        logging.info('=== DB initialization ===')
        dbConfig = config.getDbConfigDict()
        return DbManager(dbConfig)

    def openTranslationCodes(self, config):
        logging.info('=== Read translation page  ===')   #Read selected language translation
        codes = config.getCodes()
        return Translate(codes)
