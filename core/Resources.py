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
    """ Holder for all resources: DB connection, PLC connection, translation codes and so on
    Also contain logger for resourses, if they need to log something: self.logger """

    def __init__(self):
        """ Reads common configuration file. As result after initialization
        common dictionary, codes, observer and object will be created """
        try:
            self.logger = openLog("resources")
            self.config = ProgramConfig()

            lang = self.config.getDefaultLanguage()
            self.codes = TranslationConfig(lang)

            observerConfig = self.config.getObserverConfig()
            self.observer = Observer(observerConfig)
            self.object = Object(self.observer)

            self.plcManager = PLCManager()
            self._setPoint = self._initSetPoint()

            self._dbManager = DbManager(self.config.getDbConfig())
            self.dbStar = Star(self._dbManager)
            self.dbLog = Log(self._dbManager)
            self.dbMessage = Message(self._dbManager)
        except Exception as error:
            raise InitializationException(error.args, self.logger)

    def _initSetPoint(self):
        self.logger.info('Init SetPoint object')
        ra, dec = self.plcManager.getSetpointPosition()
        focus = self.plcManager.getFocus()[1]
        return SetPoint(ra, dec, focus)


    def __del__(self):
        self.logger.info('Closing resources')
        del self.dbMessage
        del self.dbLog
        del self.dbStar
        del self._dbManager
        del self.plcManager
        del self.codes

    def setObject(self, name):
        self.logger.info('Set new object: ' + name)
        star = self.dbStar.getStarByName(name)
        if star:
            self.object.init(star['id'], star['name'], star['ra'], star['dec'])

    def getSetPoint(self):
        return  self._setPoint

    def updateSetPoint(self):
        if self.object.selected():
            position = self.object.getCurrentCoordinates()
            self.getSetPoint().setPosition(position['ra'], position['dec'])

    def getDbManager(self):
        return self._dbManager