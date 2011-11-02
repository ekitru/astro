from posixpath import join
import logging

from Exceptions import   ClosingException
from LogThread import LogThread
from core.logger import getLogPath

__author__ = 'kitru'

class Controller(object):
    _controlMode = True

    def __init__(self):
        self.__initLogger()

        self.manPosition = None
        self.manFocus = None



    def __initLogger(self):
        logPath = getLogPath()
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                            datefmt='%m-%d %H:%M',
                            filename=join(logPath, 'common.log'),
                            filemode='w')

    def initialization(self, resources):
        """ Initialization for all components
        Opens DB connection and connection with PLCm also reads translation codes """
        try:
            logging.info('======= Program initialization =======')
            self._resources = resources
            self._logThread = LogThread(resources)
#        except ConfigurationException as ce:
#            raise InitializationException(ce)
#        except Exception as e:
#            raise InitializationException(e)
        except ImportError:
            pass


    def freeResources(self):
        try:
            logging.info('======= Free all resources: DB, MODBUS =======')
            # close database connections
            self._logThread.stop()
            del self._resources
        except Exception as e:
            raise ClosingException(e)

    def getResourceKeeper(self):
        return self._resources

    def logNow(self):
        """ Force to log message and start new timer  """
        self._logThread.force()


    def pcControlSelected(self):
        """  Returns True if status flag read from PLC equals "1" (PC control selected)
             Returns False if status flag read from PLC equals "0" (REMOTE control selected)"""
        return self._resources.getPLCManager().isPCControl()

    def remoteControlSelected(self):
        """  Returns True if status flag read from PLC equals "0" (REMOTE control selected)
             Returns False if status flag read from PLC equals "1" (PC control selected)"""
        return not self._resources.getPLCManager().isPCControl()

    def objSetpointControlSelected(self):
        """ Returns True if AUTO control selected
            Returns False if MANUAL control selected
        """
        return self._controlMode

    def scopeCanMove(self):
        return True #TODO add more complex logic here
