import logging
import threading
from db import Message, Log

__author__ = 'kitru'

class LogThread(object):
    """ Separate thread for logging stuff.
    It starts to log in separate thread as new instance will be done  or _start() method will be called
    Timer could be stopped be calling stop() method.  """

    def __init__(self, resources):
#        try:
        self._mutex = threading.RLock()
        logging.info('Starting logging thread')
        self._resources = resources
        db = self._resources.getDbManager()
        self._log = Log(db)
        self._message = Message(db)
        self._plc = self._resources.plcManager
        self._position = self._resources.plcManager.getPositionHelper()
        self._period = resources.config.getLoggingTime()
        self._start()
#        except Exception as ex:
#            raise ConfigurationException(ex)

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
            if self._resources.plcManager.isConnected():
                self._log.setStarId(self._getStarId())
                self._log.setMsgId(self._getMsgId())
                self._log.setCurrentRaDec(*self._getCurrentRaDec())
                self._log.setCurrentFocus(self._getCurrentFocus())
                self._log.setTemperature(*self._getTemperature())
                self._log.setAlarmStatus(self._getAlarmStatus())
                self._log.writeToLog()

    def force(self):
        with self._mutex:
            self._timer.cancel()
            self._timer.join()
            self._start()

    def updatePeriod(self, time):
        """ Update logging period, period in seconds """
        self._period = time

    def _getStarId(self):
        """ return selected object id from controller, if object is not selected return None """
        object = self._resources.object
        return object.getId()

    def _getMsgId(self):
        """ for getting current message last stored message is used """
        id = self._message.getLastId()
        return id

    def _getCurrentRaDec(self):
        """ current telescope positions are taken directly from plc """
        return self._position.getCurrentPosition()

    def _getCurrentFocus(self):
        """ current telescope positions are taken directly from plc """
        focus = self._position.getFocus()
        return focus[0]

    def _getTemperature(self):
        """ current dome and telescope temperatures """
        return self._plc.getModeHelper().readTemperatures()

    def _getAlarmStatus(self):
        """ alarm status as a alarm codes separated by ',' """
        return self._plc.readAlarmStatus()

