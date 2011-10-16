import threading
from core.Exceptions import ConfigurationException
from db import Message, Log

__author__ = 'kitru'

class LogThread(object):
    """ Separate thread for logging stuff.
    It starts to log in separate thread as new instance will be done  or _start() method will be called
    Timer could be stopped be calling stop() method.  """
    _scale = 10 #should be 60 second in minute

    def __init__(self, controller):
        try:
#            minutes = float(config.getCommonConfigDict()['logging time'])
            minutes = 1
            self._period = minutes * self._scale
            self._controller = controller

            self._resourceKeeper = controller.getResourceKeeper()
            self._log = Log(self._resourceKeeper.getDbManager())
            self._message = Message(self._resourceKeeper.getDbManager())
            self._plc = self._resourceKeeper.getPLCManager()

            self._mutex = threading.RLock()
            self._start()
        except Exception as ex:
            raise ConfigurationException(ex.args)

    def _start(self):
        """ Starts timer to run, function is looped by itself.
        Should be interrupted by calling timer.cancel() in other case it will become a daemon  """
        self._doWork()
        self._timer = threading.Timer(self._period, self._start)
        self._timer.start()

    def stop(self):
        """ Thread safe method for stopping timer. It will finish as soon as timer
        thread stops working and thread will be closed"""
        with self._mutex:
            self._timer.cancel()
            self._timer.join()

    def _doWork(self):
        """ All logging stuff performs here. This method is calling by logging thread """
        with self._mutex:
            self._log.setMsgId(self.getMsgId())
            self._log.setCurrentRaDec(*self.getCurrentRaDec())
            self._log.setCurrentFocus(self.getCurrentFocus())
            self._log.setStarId(self.getStarId())
            self._log.writeToLog()

    def force(self):
        with self._mutex:
            self._timer.cancel()
            self._timer.join()
            self._start()

    def getStarId(self):
        """ return selected object id from controller, if object is not selected return None """
        object = self._controller.getObject()
        return object.getId()

    def getMsgId(self):
        """ for getting current message last stored message is used """
        id = self._message.getLastId()
        return id

    def getCurrentRaDec(self):
        """ current telescope positions are taken directly from plc """
        position = self._plc.getPosition()
        return position[0]

    def getCurrentFocus(self):
        """ current telescope positions are taken directly from plc """
        focus = self._plc.getFocus()
        return focus[0]

    def getTemperature(self, temp_in, temp_out):
        pass #PLC

    def getAlarmStatus(self, word):
        pass

#PLC