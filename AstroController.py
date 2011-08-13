import logging
import os
from posixpath import join
from AstroMechanics import AstroMechanics
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


class ClosingException(object):
    """Exception raised for errors during system closing.
    Attributes:
        msg  -- explanation of the error
    """

    def __init__(self, msg, logger=None):
        Exception.__init__(self, msg)
        if logger:
            logger.error(msg)


class AstroController(object):
    def __init__(self):
        self.__initLogger()
        self.initialization()

    def __initLogger(self):
        if not os.path.exists('logs'):
            os.makedirs('logs', mode=0711)
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                            datefmt='%m-%d %H:%M',
                            filename=join('logs', 'astroFull.log'),
                            filemode='w')

    def initialization(self):
        """ Initialization for all components
        Opens DB connection and connection with PLCm also reads translation codes
        """
        try:
            config = self.openConfig('default.conf')
            self.mechanics = self.openAstroMechanics(config)
            self.commManager = self.openCommManager(config)
            self.dbManager = self.openDbManager(config)
            self.transCodes = self.openTranslationCodes(config)
        except ConfigurationException as ce:
            logging.error('Erron during initialization occure: ' + ce.__str__())
            raise InitializationException(ce)

    def freeResources(self):
        try:
            logging.info('======= Free all resources: DB, MODBUS =======')
            self.dbManager.close()
        except Exception as e:
            raise ClosingException(e)

    def openConfig(self, confFileName):
        logging.info('======= Program initialization =======')
        return Configuration(confFileName)

    def openCommManager(self, config):
        logging.info('=== Communication initialization ===')
        commConfig = config.getCommunicationConfigDict()
        return CommManager(commConfig)

    def openDbManager(self, config):
        logging.info('=== DB initialization ===')
        dbConfig = config.getDbConfigDict()
        return DbManager(dbConfig)

    def openTranslationCodes(self, config):
        logging.info('=== Reading translation page  ===')   #Read selected language translation
        codes = config.getCodes()
        return Translate(codes)

    def openAstroMechanics(self, config):
        """ get observer for telescope position """
        logging.info('=== Reading telescope configurations ===')
        configs = config.getObserverDict()
        return AstroMechanics(configs)