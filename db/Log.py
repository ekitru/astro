from db.DbQuery import DBQuery
import time
import astronomy

__author__ = 'kitru'

class Log(DBQuery):
    """ manage operations with logs in Log table """

    def __init__(self, dbManager):
        super(Log, self).__init__(dbManager.getDb(), dbManager.getLog())
        self.cleanValues()

    def writeToLog(self):
        """ Saves new row in DB.
        can throw DbException """
        self._addRecord()
        self.cleanValues()

    def _addRecord(self):
        sql = self._getSQL()
        args = self._getArgs()
        self.insert(sql, args)

    def _getSQL(self):
        fields = "(`id`, `time`, `star_id`, `msg_id`, `ra`, `dec`, `focus`,`temp_in`, `temp_out`,`status`)"
        values = "(default, %(time)s, %(star_id)s, %(msg_id)s, %(ra)s, %(dec)s, %(focus)s, %(temp_in)s, %(temp_out)s, %(status)s)"
        sql = "INSERT INTO `log` " + fields + " VALUES " + values
        return sql

    def _getArgs(self):
        timestamp = int(time.time())
        return {'id': self._id, 'time': timestamp, 'star_id': self._star_id, 'msg_id': self._msg_id, 'ra': self._ra,
                'dec': self._dec,
                'focus': self._focus, 'temp_in': self._temp_in, 'temp_out': self._temp_out, 'status': self._status}

    def readLog(self, starName=None, startDate=None, endDate=None):
        """ Read log, result can be filtered by star name or logging period """
        select = "SELECT l.`id`,l.`time`, s.`name`, s.`ra`,s.`dec`, m.`text`, l.`ra`, l.`dec`, l.`temp_in`, l.`temp_out`, l.`status` FROM `log` l LEFT JOIN `star` s ON l.star_id=s.id LEFT JOIN `message` m ON l.msg_id=m.id"
        condition = self.condConstruct(starName, startDate, endDate)
        rows = self.selectAll(select, where=condition)
        list = []
        for row in rows:
            data = {}
            data['id'] = row[0]
            data['time'] = time.ctime(int(row[1]))
            data['name'] = row[2]
            data['sRa'], data['sDec'] = astronomy.rad2str(row[3], row[4])
            data['msg'] = row[5]
            data['ra'], data['dec'] = astronomy.rad2str(row[6], row[7])
            data['temp_in'], data['temp_out'] = row[8], row[9]
            data['status'] = row[10]
            list.append(data)
        return list


    def condConstruct(self, starName, startDate, endDate):
        """ Construct where codition """
        list = []
        if starName:
            list.append("s.`name` =\"" + starName + "\"")
        if startDate and endDate:
            list.append("l.`time` between " + str(startDate) + " and " + str(endDate))
        row = " AND ".join(list)
        print('condition', row)
        return row


    def cleanValues(self):
        #Parameters from program
        self._id = None
        self._star_id = None
        self._msg_id = None
        #Parameters from PLC
        self._ra = None
        self._dec = None
        self._focus = None
        self._temp_in = None
        self._temp_out = None
        self._status = None #alarm status word

    def setStarId(self, id):
        self._star_id = id

    def setMsgId(self, id):
        self._msg_id = id

    def setCurrentRaDec(self, ra, dec):
        self._ra = ra
        self._dec = dec

    def setCurrentFocus(self, focus):
        self._focus = focus

    def setTemperature(self, temp_in, temp_out):
        self._temp_in = temp_in
        self._temp_out = temp_out

    def setAlarmStatus(self, word):
        self._status = word
  