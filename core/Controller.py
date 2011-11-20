from posixpath import join
import logging

from Exceptions import   ClosingException
from LogThread import LogThread
from core.Resources import Resources
from core.Exceptions import ConfigurationException, InitializationException
from core.logger import getLogPath

__author__ = 'kitru'

class Controller(object):
    def __init__(self):
        self.__initLogger()

    def __initLogger(self):
        logPath = getLogPath()
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                            datefmt='%m-%d %H:%M',
                            filename=join(logPath, 'common.log'),
                            filemode='w')

    def initialization(self):
        """ Initialization for all components
        Opens DB connection and connection with PLCm also reads translation codes """
        try:
            logging.info('======= Program initialization =======')
            self.resources = Resources()
            self.logThread = LogThread(self.resources)
        except ConfigurationException as ce:
            logging.info('Error during initialization occure', ce)
            raise InitializationException(ce)
        except Exception as e:
            logging.info('Error during initialization occure', e)
            raise InitializationException(e)


    def freeResources(self):
        """ free all resources, close all connections """
        try:
            logging.info('======= Program closing =======')
            self.logThread.stop()
            del self.resources
        except Exception as e:
            raise ClosingException(e)

    def forceLog(self):
        """ Force to log message and start new timer  """
        self.logThread.force()

    def updateLogTime(self, time):
        """ update logging period, time in minutes """
        self.logThread.updatePeriod(int(time)*60)
