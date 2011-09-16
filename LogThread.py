import threading
from db import Message, Log, Star

__author__ = 'kitru'

class LogThread(object):
    __scale = 1

    def __init__(self, controller, minutes=1):
        self.__period = minutes * self.__scale
        self.__controller = controller
        self.__log = Log(controller.getDbManager())
        self.__message = Message(controller.getDbManager())
        self.__plc = controller.PLCManager
        self.start()

    def start(self):
        self.__timer = threading.Timer(self.__period, self.doWork)
        self.__timer.start()

    def stop(self):
        self.__timer.cancel()

    def doWork(self):
        self.__log.setStarId(self.getStarId())
        self.__log.setMsgId(self.getMsgId())
        self.__log.setCurrentRaDec(*self.getCurrentRaDec())
        self.__log.setCurrentFocus(self.getCurrentFocus())
        self.__log.saveLog()
        self.start()

    def getStarId(self):
        object = self.__controller.getObject()
        return object.getId()

    def getMsgId(self):
        id = self.__message.getLastId()
        return id

    def getCurrentRaDec(self):
        position = self.__plc.getPosition()
        return position[0]

    def getCurrentFocus(self):
        focus = self.__plc.getFocus()
        return focus[0]

    def getTemperature(self, temp_in, temp_out):
        pass #PLC

    def getAlarmStatus(self, word):
        pass #PLC