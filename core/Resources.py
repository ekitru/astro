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
            self.codes = TranslationConfig(lang)

            observerConfig = self._config.getObserverConfig()
            self._observer = Observer(observerConfig)
            self._object = Object(self._observer)

            self.plcManager = PLCManager()
            self._setPoint = self._initSetPoint()

            self._dbManager = DbManager(self._config.getDbConfig())
            self.dbStar = Star(self._dbManager)
            self.dbLog = Log(self._dbManager)
            self.dbMessage = Message(self._dbManager)
        except Exception as error:
            raise InitializationException(error.args, self._logger)

    def _initSetPoint(self):
        self._logger.info('Init SetPoint object')
        ra, dec = self.plcManager.getSetpointPosition()
        focus = self.plcManager.getFocus()[1]
        return SetPoint(ra, dec, focus)


    def __del__(self):
        self._logger.info('Closing resources')
        del self.dbMessage
        del self.dbLog
        del self.dbStar
        del self._dbManager
        del self.plcManager
        del self.codes


    def getConfig(self):
        return  self._config

    def getObserver(self):
        return self._observer

    def getObject(self):
        return self._object

    def setObject(self, name):
        self._logger.info('Set new object: ' + name)
        star = self.dbStar.getStarByName(name)
        if star:
            self.getObject().init(star['id'], star['name'], star['ra'], star['dec'])

    def getSetPoint(self):
        return  self._setPoint

    def updateSetPoint(self):
        object = self.getObject()
        if object.selected():
            position = object.getCurrentCoordinates()
            self.getSetPoint().setPosition(position['ra'], position['dec'])

    def getDbManager(self):
        return self._dbManager