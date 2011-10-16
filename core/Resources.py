from core.Exceptions import InitializationException
from core.PLCManager import PLCManager
from core.astronomy import Object, Observer

from core.config import ProgramConfig
from core.config import TranslationConfig

from db import Message, Log, Star
from db.DbManager import DbManager

__author__ = 'kitru'

class Resources(object):
    """ Holder for all resources: DB connection, PLC connection, translation codes and so on  """
    def __init__(self):
        """ Reads common configuration file. As result after initialization
        common dictionary, codes, observer and object will be created """
        try:
            config = ProgramConfig()
            self._commonDict = config.getCommonConfigDict()

            lang = config.getDefaultLanguage()
            self._codes = TranslationConfig(lang)

            observerConfig = config.getObserverConfig()
            self._observer = Observer(observerConfig)
            self._object = Object(self._observer)

            self._PLCManager = PLCManager()

            self._dbManager = DbManager(config.getDbConfig())
            self._star = Star(self._dbManager)
            self._log = Log(self._dbManager)
            self._message = Message(self._dbManager)
        except Exception as error:
            msg = error.args
            logger = config.getLogger()
            raise InitializationException(msg, logger)


    def __del__(self):
        del self._message
        del self._log
        del self._star
        del self._dbManager
        del self._PLCManager
        del self._codes

    def getCodes(self):
        return self._codes

    def getObserver(self):
        return self._observer

    def getObject(self):
        return self._object

    def setObject(self, name):
        star = self.getStarHolder().getStarByName(name)
        if star:
            self.getObject().init(star['id'], star['name'], star['ra'], star['dec'])

    def getPLCManager(self):
        return self._PLCManager

    def getDbManager(self):
        return self._dbManager

    def getStarHolder(self):
        return self._star

    def getLogHolder(self):
        return self._log

    def getMessageHolder(self):
        return self._message
  