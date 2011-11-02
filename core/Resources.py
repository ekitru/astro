from core.Exceptions import InitializationException
from core.PLCManager import PLCManager
from core.astronomy import Object, Observer, SetPoint

from core.config import ProgramConfig
from core.config import TranslationConfig
from core.logger import openLog

from db import Message, Log, Star
from db.DbManager import DbManager

__author__ = 'kitru'

class Resources(object):
    """ Holder for all resources: DB connection, PLC connection, translation codes and so on  """

    def __init__(self):
        """ Reads common configuration file. As result after initialization
        common dictionary, codes, observer and object will be created """
        try:
            self._logger = openLog("resources")
            self._config = ProgramConfig()

            lang = self._config.getDefaultLanguage()
            self._codes = TranslationConfig(lang)

            observerConfig = self._config.getObserverConfig()
            self._observer = Observer(observerConfig)
            self._object = Object(self._observer)

            self._PLCManager = PLCManager()
            self._setPoint = self._initSetPoint()

            self._dbManager = DbManager(self._config.getDbConfig())
            self._dbStar = Star(self._dbManager)
            self._dbLog = Log(self._dbManager)
            self._dbMessage = Message(self._dbManager)
        except Exception as error:
            raise InitializationException(error.args, self._logger)

    def _initSetPoint(self):
        self._logger.info('Init SetPoint object')
        ra, dec = self._PLCManager.getSetpointPosition()
        focus = self._PLCManager.getFocus()[1]
        return SetPoint(ra, dec, focus)


    def __del__(self):
        self._logger.info('Closing resources')
        del self._dbMessage
        del self._dbLog
        del self._dbStar
        del self._dbManager
        del self._PLCManager
        del self._codes


    def getConfig(self):
        return  self._config

    def getCodes(self):
        return self._codes

    def getObserver(self):
        return self._observer

    def getObject(self):
        return self._object

    def setObject(self, name):
        self._logger.info('Set new object: ', name)
        star = self.getStarHolder().getStarByName(name)
        if star:
            self.getObject().init(star['id'], star['name'], star['ra'], star['dec'])

    def getSetPoint(self):
        return  self._setPoint

    def updateSetPoint(self):
        object = self.getObject()
        if object.selected():
            position = object.getCurrentCoordinates()
            self.getSetPoint().setPosition(position['ra'], position['dec'])

    def getPLCManager(self):
        return self._PLCManager

    def getDbManager(self):
        return self._dbManager

    def getStarHolder(self):
        return self._dbStar

    def getLogHolder(self):
        return self._dbLog

    def getMessageHolder(self):
        return self._dbMessage
  