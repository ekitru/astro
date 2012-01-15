import logging
import threading
from db.AlarmLog import AlarmLog

__author__ = 'kitru'

class AlarmLogThread(object):
    """ Separate thread for alarm logging stuff.
    It starts to log in separate thread as new instance will be done  or _start() method will be called
    Timer could be stopped be calling stop() method.  """

    def __init__(self, resources):
#        try:
        self._mutex = threading.RLock()
        logging.info('Starting alarm logging thread')
        self._resources = resources
        self._plcHelper = self._resources.plcManager.getAlarmHelper()
        db = self._resources.getDbManager()
        self._log = AlarmLog(db)
        self._period = 10
        self._start()
#        except Exception as ex:
#            raise ConfigurationException(ex)

    def _start(self):
        """ Starts timer to run, function is looped by itself.
        Should be interrupted by calling timer.cancel() in other case it will become a daemon  """
        if self._resources.plcManager.isSwitchedOn():
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
                nextAlarm = self._plcHelper.getNextAlarm()
                while nextAlarm:
                    print('Processing alarm')
                    print(nextAlarm)
                    self.storeRecord(nextAlarm)
                    nextAlarm = self._plcHelper.getNextAlarm()

    def storeRecord(self, nextAlarm):
        self._log.cleanValues()
        self._log.setCode(nextAlarm[0])
        self._log.setAction(nextAlarm[1])
        self._log.setTime(int(nextAlarm[2])+2*60*60)
        self._log.writeToLog()
