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
        self.__Message = Message(controller.getDbManager())
        self.start()

    def start(self):
        self.__timer = threading.Timer(self.__period, self.doWork)
        self.__timer.start()

    def stop(self):
        self.__timer.cancel()

    def doWork(self):

        self.start()
  