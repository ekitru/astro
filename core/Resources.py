from core.PLCManager import PLCManager
from core.astronomy import Object, Observer, SetPoint

from core.config import ProgramConfig
from core.logger import openLog

from db import Message, Log, Star
from db.DbManager import DbManager

__author__ = 'kitru'

class Resources(object):
    """ Holder for all resources: DB connection, PLC connection, translation codes and so on
    Also contain logger for resourses, if they need to log something: self.logger """
    dbStar = None
    dbLog = None
    dbMessage = None
    plcManager = None

    def __init__(self):
        """ Reads common configuration file and initialize transation codes, observer object """
        self.logger = openLog("resources")
        self.config = ProgramConfig()

        observerConfig = self.config.getObserverConfig()
        self.observer = Observer(observerConfig)
        self.object = Object(self.observer)

        self.setPoint = SetPoint()
        self.initResources()

    def initResources(self):
        self.initDbResources()
        self.initPlcResources()

    def initDbResources(self):
        self._dbManager = DbManager(self.config.getDbConfig())
        self.dbStar = Star(self._dbManager)
        self.dbLog = Log(self._dbManager)
        self.dbMessage = Message(self._dbManager)

    def initPlcResources(self):
        self.plcManager = PLCManager()
        self.logger.info('Init SetPoint object')
        self.setPoint = SetPoint()

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
        return  self.setPoint

    def getDbManager(self):
        return self._dbManager