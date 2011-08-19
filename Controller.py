import os
from posixpath import join
import logging

from Exceptions import ConfigurationException, InitializationException, ClosingException
from Config import ProgramConfig

__author__ = 'kitru'

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
            self.mechanics = config.openAstroMechanics()
            self.dbManager = config.getDbManager()
            self.commManager = config.getPLCManager()
            self.trans = config.getTranslationConf()
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