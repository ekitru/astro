# -*- coding: utf-8 -*-
import threading

import MySQLdb
import astronomy

from Exceptions import ConfigurationException, DbException
from logger import getLog, closeLog


__author__ = 'kitru'

class DbManager(object):
    """ Manage DB connection
    handle it opening and closing, also handle logs """

    def __init__(self, confDict):
        self._logger = getLog('database')
        self._dbName = confDict['database']
        self._db = self._getDbConnection(confDict)

    def __del__(self):
        self.close()
        closeLog(self._logger)

    def _getDbConnection(self, confDict):
        """ Get db connection dased on config file
        Attributes:
            config - SafeConfigParser object
        """
        try:
            self._logger.info('Establishing connection')
            db = MySQLdb.connect(confDict['host'], confDict['user'], confDict['password'], confDict['database'],
                                 port=int(confDict['port']), charset="utf8", use_unicode=True)
            self._logger.info('Connection established')
            return db
        except Exception as error:
            raise ConfigurationException(error.args, self._logger)

    def getDb(self):
        return self._db

    def getLog(self):
        return self._logger

    def close(self):
        """ Closes DB connection. If it clsoed logs event and do nothing """
        if self._db:
            self._logger.info("Close DB connection")
            self._db.close()
        else:
            self._logger.info("DB connection already closed")


class DBQuery(object):
    """ Simple db helper, makes easier data manipulations. Thread safe  """

    def __init__(self, db, logger):
        super(DBQuery, self).__init__()
        self._logger = logger
        self._db = db
        self.cursor = db.cursor()
        self._mutex = threading.RLock()

    def __del__(self):
        self.close()

    def selectOne(self, sql, args=None, where=None):
        try:
            with self._mutex:
                if where:
                    sql = sql + " WHERE " + where
                self.cursor.execute(sql, args)
                return self.cursor.fetchone()
        except Exception as error:
            raise DbException(error.args, self._logger)

    def selectAll(self, sql, args=None, where=None):
        try:
            with self._mutex:
                if where:
                    sql = sql + " WHERE " + where
                self.cursor.execute(sql, args)
                return self.cursor.fetchall()
        except Exception as error:
            raise DbException(error.args, self._logger)

    def insert(self, sql, args):
        """ Insert single row value
        Return: last row number  """
        try:
            with self._mutex:
                self.cursor.execute(sql, args)
                self._db.commit()
                return self.cursor.lastrowid
        except Exception as error:
            self._db.rollback()
            raise DbException(error.args, self._logger)

    def update(self, sql, args):
        try:
            with self._mutex:
                self.cursor.execute(sql, args)
                self._db.commit()
        except Exception as error:
            self._db.rollback()
            raise DbException(error.args, self._logger)

    def delete(self, sql, args):
        try:
            with self._mutex:
                self.cursor.execute(sql, args)
                self._db.commit()
        except Exception as error:
            self._db.rollback()
            raise DbException(error.args, self._logger)

    def close(self):
        """ Close cursor if not closed. Also will be called during object deleting """
        if self._db:
            self._logger.debug("Close cursor")
            self.cursor.close()
        else:
            self._logger.debug("Cursor already closed")


class Star(DBQuery):
    """ manage operations with stars in DB """

    def __init__(self, dbManager):
        super(Star, self).__init__(dbManager.getDb(), dbManager.getLog())

    def starExists(self, name):
        """ Check DB for record with same name """
        star = self.getStarByName(name)
        if star:
            return True
        else:
            return False

    def saveStar(self, name, ra, dec):
        """ Saves star object into database
        Attr:
             ra -  in string (hours:MIN:SEC)
             dec - in string (DEG:MIN:SEC)
        can throw DbException """
        ra, dec = astronomy.str2rad(str(ra), str(dec))
        sql = "INSERT INTO `star` (`id`,`name`,`ra`,`dec`) VALUES (default, %(name)s,%(ra)s,%(dec)s)"
        args = {'name': name, 'ra': float(ra), 'dec': float(dec)}
        self.insert(sql, args)

    def updateStar(self, name, ra, dec):
        """ Updates star object in database
        Attr:
             ra -  in string (hours:MIN:SEC)
             dec - in string (DEG:MIN:SEC)
         can throw DbException """
        ra, dec = astronomy.str2rad(str(ra), str(dec))
        sql = "update `star` set`ra`=%(ra)s, `dec`=%(dec)s WHERE `name`=%(name)s"
        args = {'name': name, 'ra': float(ra), 'dec': float(dec)}
        self.update(sql, args)

    def deleteStar(self, star):
        """Deletes star object from database
        Attr:
             ra -  in string (hours:MIN:SEC)
             dec - in string (DEG:MIN:SEC)
         can throw DbException """
        sql = "DELETE FROM `star` WHERE `name`=%(name)s"
        args = {'name': star['name']}
        self.delete(sql, args)

    def getStarByName(self, name):
        """ Take star from database by name
        return:
             Star name and position in suitable form for customer (: separated)
             If star does not exist, return None
        can throw DbException """
        sql = "SELECT `id`,`name`,`ra`,`dec` FROM `star` WHERE name=%(name)s"
        args = {'name': name}
        star = self.selectOne(sql, args)
        if star:
            return self.parseStar(star)
        else:
            return None

    def getStars(self, name):
        """ Returns list of star objects(name,ra,dec)
        Fetchs all rows with similar star name like name%
        Star name and position in suitable form for customer
        can throw DbException """
        stars = self.getStarsByPartName(name)
        resp = []
        for star in stars:
            resp.append(self.parseStar(star))
        return resp

    def getStarsByPartName(self, name):
        """ looks for all like name%   """
        name = name.encode('utf-8')
        sql = "SELECT `id`,`name`,`ra`,`dec` FROM `star` WHERE name LIKE %(name)s ORDER BY `name`  LIMIT 20"
        args = {'name': (name + '%')}
        return self.selectAll(sql, args)

    def parseStar(self, star):
        """ Convert row from DB into dictionary
        Attr:
          star - one record from DB
        Return:
           dic('id','name','ra','dec')
        """
        id = star[0]
        name = star[1]
        ra, dec = astronomy.rad2str(star[2], star[3])
        return {'id': id, 'name': name, 'ra': ra, 'dec': dec}


class Message(DBQuery):
    """ manage operations with messages in DB """

    def __init__(self, dbManager):
        super(Message, self).__init__(dbManager.getDb(), dbManager.getLog())

    def setNew(self, text):
        """ return added message id
        can throw DbException """
        sql = "INSERT INTO `message` (`id`,`text`) VALUES (default, %(text)s)"
        args = {'text': text}
        return self.insert(sql, args)

    def getLastId(self):
        """ return last stored message id, if there is no return empty string
        can throw DbException """
        if self.getLastRow():
            return self.getLastRow()[0]

    def getLastMsg(self):
        """ return last stored message, if there is no return empty string
        can throw DbException """
        if self.getLastRow():
            return self.getLastRow()[1]
        else:
            return ""

    def getLastRow(self):
        """ Last row is the newest message in DB
        can throw DbException """
        sql = "SELECT `id`,`text` FROM `message` ORDER BY `id` DESC LIMIT 1"
        return self.selectOne(sql)


class Log(DBQuery):
    """ manage operations with logs in Log table """

    def __init__(self, dbManager):
        super(Log, self).__init__(dbManager.getDb(), dbManager.getLog())
        self.cleanValues()

    def writeToLog(self):
        """ Saves new row in DB.
        can throw DbException """
        self.addRecord()
        self.cleanValues()

    def addRecord(self):
        sql = self._insertSQL()
        args = self._insertSQLargs()
        self.insert(sql, args)

    def _insertSQL(self):
        fields = "(`id`, `star_id`, `msg_id`, `ra`, `dec`, `focus`,`temp_in`, `temp_out`,`status`)"
        values = "(default, %(star_id)s, %(msg_id)s, %(ra)s, %(dec)s, %(focus)s, %(temp_in)s, %(temp_out)s, %(status)s)"
        sql = "INSERT INTO `log` " + fields + " VALUES " + values
        return sql

    def _insertSQLargs(self):
        return {'id': self._id, 'star_id': self._star_id, 'msg_id': self._msg_id, 'ra': self._ra, 'dec': self._dec,
                'focus': self._focus, 'temp_in': self._temp_in, 'temp_out': self._temp_out, 'status': self._status}

    def readLog(self, starName=None):
        select = "SELECT l.id,s.id,s.ra,s.dec, m.text, l.ra, l.dec, l.temp_in, l.temp_out, l.status FROM `log` l LEFT JOIN `star` s ON l.star_id=s.id LEFT JOIN `message` m ON l.msg_id=m.id"
        if starName:
            condition = "s.name= \"" + starName + "\""
        else:
            condition = None
        ret = self.selectAll(select, args=None, where=condition)
        return ret


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


