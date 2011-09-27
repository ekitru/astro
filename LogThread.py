import threading
from db import Message, Log

__author__ = 'kitru'

class LogThread(object):
    _scale = 30

    def __init__(self, controller, minutes=1):
        self._mutex = threading.RLock()
        self._period = minutes * self._scale
        self._controller = controller

        self._resurseKeeper = controller.getResourceKeeper()
        self._log = Log(self._resurseKeeper.getDbManager())
        self._message = Message(self._resurseKeeper.getDbManager())
        self._plc = self._resurseKeeper.getPLCManager()
        self._start()

    def _start(self):
        self._timer = threading.Timer(self._period, self.doWork)
        self._timer.start()

    def _stop(self):
        with self._mutex:
            self._timer.cancel()
            self._timer.join()

    def doWork(self):
        with self._mutex:
            self._log.setMsgId(self.getMsgId())
            self._log.setCurrentRaDec(*self.getCurrentRaDec())
            self._log.setCurrentFocus(self.getCurrentFocus())
            self._log.setStarId(self.getStarId())
            self._log.writeToLog()
            self._start()

    def getStarId(self):
        object = self._controller.getObject()
        return object.getId()

    def getMsgId(self):
        id = self._message.getLastId()
        return id

    def getCurrentRaDec(self):
        position = self._plc.getPosition()
        return position[0]

    def getCurrentFocus(self):
        focus = self._plc.getFocus()
        return focus[0]

    def getTemperature(self, temp_in, temp_out):
        pass #PLC

    def getAlarmStatus(self, word):
        pass

#PLC