import threading
from core.Exceptions import ConfigurationException
from db import Message, Log

__author__ = 'kitru'

class LogThread(object):
    """ Separate thread for logging stuff.
    It starts to log in separate thread as new instance will be done  or _start() method will be called
    Timer could be stopped be calling stop() method.  """
    _scale = 10 #should be 60 second in minute

    def __init__(self, resources):
        try:
#            minutes = float(config.getCommonConfigDict()['logging time'])
            minutes = 1
            self._period = minutes * self._scale

            self._resources = resources
            self._log = Log(self._resources.getDbManager())
            self._message = Message(self._resources.getDbManager())
            self._plc = self._resources.getPLCManager()

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
#            self._timer.join() #TODO discover, some times thread is not started yet
            self._start()

    def getStarId(self):
        """ return selected object id from controller, if object is not selected return None """
        object = self._resources.getObject()
        return object.getId()

    def getMsgId(self):
        """ for getting current message last stored message is used """
        id = self._message.getLastId()
        return id

    def getCurrentRaDec(self):
        """ current telescope positions are taken directly from plc """
        return self._plc.getCurrentPosition()

    def getCurrentFocus(self):
        """ current telescope positions are taken directly from plc """
        focus = self._plc.getFocus()
        return focus[0]

    def getTemperature(self, temp_in, temp_out):
        pass #PLC

    def getAlarmStatus(self, word):
        pass

#PLC