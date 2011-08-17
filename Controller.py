from apt_pkg import Configuration
import logging
import os
from posixpath import join
from AstroMechanics import AstroMechanics
from CommManager import CommManager
from DbManager import DbManager
from config import ConfigurationException, TransConf, ProgramConfig

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


class Controller(object):
    def __init__(self):
        self.__initLogger()
        self.initialization()

    def __initLogger(self):
        if not os.path.exists('logs'):
            os.makedirs('logs', mode=0711)
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                            datefmt='%m-%d %H:%M',
                            filename=join('logs', 'common.log'),
                            filemode='w')

    def initialization(self):
        """ Initialization for all components
        Opens DB connection and connection with PLCm also reads translation codes
        """
        try:
            logging.info('======= Program initialization =======')
            config = ProgramConfig('default.conf')
            self.mechanics = self.openAstroMechanics(config)
            self.dbManager = self.openDbManager(config)
            self.commManager = self.openCommManager(config)
            self.trans = self.getTranslationConf(config)
        except ConfigurationException as ce:
            logging.error('Erron during initialization occure: ' + ce.__str__())
            raise InitializationException(ce)

    def freeResources(self):
        try:
            logging.info('======= Free all resources: DB, MODBUS =======')
            self.dbManager.close()
            self.commManager.close()
        except Exception as e:
            raise ClosingException(e)

    def openCommManager(self, config):
        logging.info('=== Communication initialization ===')
        commConfig = config.getCommunicationConfigDict()
        return CommManager(commConfig)

    def openDbManager(self, config):
        logging.info('=== DB initialization ===')
        dbConfig = config.getDbConfigDict()
        return DbManager(dbConfig)

    def getTranslationConf(self, config):
        logging.info('=== Reading translation page  ===')   #Read selected language translation
        language = config.getDefaultLanguage()
        return TransConf(language)

    def openAstroMechanics(self, config):
        """ get observer for telescope position """
        logging.info('=== Reading telescope configurations ===')
        configs = config.getObserverDict()
        return AstroMechanics(configs)