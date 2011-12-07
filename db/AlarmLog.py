from db.DbQuery import DBQuery
import time

__author__ = 'kitru'

class AlarmLog(DBQuery):
    """ manage operations with logs in alarm log table """
    _log = None

    def __init__(self, dbManager):
        super(AlarmLog, self).__init__(dbManager.getDb(), dbManager.getLogger())
        self.cleanValues()

    def writeToLog(self):
        """ Saves new row in DB.
        can throw DbException """
        self._addRecord()
        self.cleanValues()

    def _addRecord(self):
        sql = self._getSQL()
        args = self._getArgs()
        print(sql, args)
        self.insert(sql, args)

    def _getSQL(self):
        fields = "(`id`, `code`,`time`, `action`)"
        values = "(default, %(code)s, %(time)s, %(action)s)"
        sql = "INSERT INTO `alarm_log` " + fields + " VALUES " + values
        return sql

    def _getArgs(self):
        return {'code': self._code, 'time': self._timestamp, 'action': self._action}

    def readLog(self, code=None, startDate=None, endDate=None):
        """ Read log, result can be filtered by star name or logging period """
        select = "SELECT l.`id`, l.`code`, l.`time`, l.`action` FROM `alarm_log` l order by time"
        condition = self.conditionConstruct(code, startDate, endDate)
        rows = self.selectAll(select, where=condition)
        list = []
        for row in rows:
            data = dict()
            data['id'] = row[0]
            data['code'] = row[1]
            data['time'] = time.ctime(int(row[2]))
            data['action'] = row[3]
            list.append(data)
        self._log = list
        return list


    def conditionConstruct(self, code, startDate, endDate):
        """ Construct where codition """
        list = []
        if code:
            list.append("`code` =\"" + code + "\"")
        if startDate and endDate:
            list.append("`time` between " + str(startDate) + " and " + str(endDate))
        row = " AND ".join(list)
        print('condition', row)
        return row


    def cleanValues(self):
        #Parameters from program
        self._code = None
        self._timestamp = None
        self._action = None

    def setCode(self, code):
        self._code = code

    def setTime(self, time):
        #TODO  make conversion
        self._timestamp = time

    def setAction(self, word):
        if word:
            self._action = True
        else:
            self._action = False

  