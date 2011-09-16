import threading
from db import Message, Log, Star

__author__ = 'kitru'

class LogThread(object):
    __scale=1
    def __init__(self,  controller, minutes=1):
        self.__period = minutes * self.__scale
        self.__controller = controller
        self.__star = Star(controller.getDbManager())
        self.__log = Log(controller.getDbManager())
        self.__message = Message(controller.getDbManager())
        self.start()

    def start(self):
        self.__timer = threading.Timer(self.__period, self.doWork)
        self.__timer.start()

    def stop(self):
        self.__timer.cancel()

    def doWork(self):
        self.__log.setStarId(self.getStarId())
        self.__log.setMsgId(self.getMsgId())

        self.__log.saveLog()
        self.start()

    def getStarId(self):
        object = self.__controller.getObject()
        starName = object.getName()
        if starName:
            star = self.__star.getStarByName(starName)
            star_id = star['id']
            return star_id
        else:
            return None

    def getMsgId(self):
        id = self.__message.getLastId()
        return id
