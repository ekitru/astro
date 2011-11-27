from posixpath import join
import logging

from Exceptions import   ClosingException
from LogThread import LogThread
from core.Resources import Resources
from core.Exceptions import ConfigurationException, InitializationException
from core.astronomy import rad2str
from core.config.TranslationConfig import TranslationConfig
from core.logger import getLogPath

__author__ = 'kitru'

class Controller(object):
    def __init__(self):
        self.__initLogger()
        self.resources = Resources()

        self.object = ObjectRepresenter(self.resources.object)

        lang = self.resources.config.getDefaultLanguage()
        self.codes = TranslationConfig(lang)

    def __initLogger(self):
        """ Initialize base system logger  """
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
            self.resources.initResources()
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
        self.logThread.updatePeriod(int(time) * 60)

        # Presenter


class ObjectRepresenter(object):
    """ Sky Object representation """

    def __init__(self, starObject):
        """ object - astronomy object """
        self._object = starObject;

    def isSelected(self):
        return self._object.selected()

    def getData(self):
        """ Return dictionary of object data
        Return:
            dict(name, ra, dec) for epoch 2000 """
        name = self._object.getName()
        position = self._object.getPosition()
        ra, dec = rad2str(*position)
        return {'name': name, 'ra': ra, 'dec': dec}

    def getPosition(self):
        coord = self._object.getEquatorialPosition()
        ra, dec = rad2str(*coord)
        alt, az = self._object.getHorizontalPosition()
        return {'ra': ra, 'dec': dec, 'alt': str(alt), 'az': str(az)}

    def getHA(self):
        ha = self._object.getCurrentHA()
        return str(ha)

    def getRiseSetTimes(self):
        rt = self._parseTime(self._object.getRisingTime())
        st = self._parseTime(self._object.getSettingTime())
        return {'rise': rt, 'set': st}

    def getExpositionTime(self):
        time =  self._object.getExpositionTime() or 'N/A'
        return str(time)

    def _parseTime(self, time):
        if time:
            return str(time.strftime('%H:%M:%S'))
        else:
            return 'N/A'