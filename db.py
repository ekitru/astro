# -*- coding: utf-8 -*-

import MySQLdb
import astronomy

from Exceptions import ConfigurationException, DbException
from logger import getLog, closeLog


__author__ = 'kitru'

class DbManager(object):
    """ Manage DB connection
    handle it opening and closing, also handle logs """
    def __init__(self, confDict):
        self.__logger = getLog('database')
        self.__dbName = confDict['database']
        self.__db = self.__getDbConnection(confDict)

    def __del__(self):
        self.close()
        closeLog(self.__logger)

    def __getDbConnection(self, confDict):
        """ Get db connection dased on config file
        Attributes:
            config - SafeConfigParser object
        """
        try:
            self.__logger.info('Establishing connection')
            db = MySQLdb.connect(confDict['host'], confDict['user'], confDict['password'], confDict['database'],
                                 port=int(confDict['port']), charset="utf8", use_unicode=True)
            self.__logger.info('Connection established')
            return db
        except Exception as error:
            raise ConfigurationException(error.args, self.__logger)

    def getDb(self):
        return self.__db

    def getLog(self):
        return self.__logger

    def close(self):
        """ Closes DB connection. If it clsoed logs event and do nothing """
        if self.__db:
            self.__logger.info("Close DB connection")
            self.__db.close()
        else:
            self.__logger.info("DB connection already closed")


class DBQuery(object):
    """ Simple db helper, makes easier data manipulations  """

    def __init__(self, db, logger):
        super(DBQuery, self).__init__()
        self.__db = db
        self.cursor = db.cursor()
        self.__logger = logger

    def __del__(self):
        self.close()

    def selectOne(self, sql, args=None):
        try:
            self.cursor.execute(sql, args)
            return self.cursor.fetchone()
        except Exception as error:
            raise DbException(error.args, self.__logger)

    def selectAll(self, sql, args):
        try:
            self.cursor.execute(sql, args)
            return self.cursor.fetchall()
        except Exception as error:
            raise DbException(error.args, self.__logger)

    def insert(self, sql, args):
        """ Insert single row value
        Return: last row number  """
        try:
            self.cursor.execute(sql, args)
            self.__db.commit()
            return self.cursor.lastrowid
        except Exception as error:
            self.__db.rollback()
            raise DbException(error.args, self.__logger)

    def update(self, sql, args):
        try:
            self.cursor.execute(sql, args)
            self.__db.commit()
        except Exception as error:
            self.__db.rollback()
            raise DbException(error.args, self.__logger)

    def delete(self, sql, args):
        try:
            self.cursor.execute(sql, args)
            self.__db.commit()
        except Exception as error:
            self.__db.rollback()
            raise DbException(error.args, self.__logger)


    def close(self):
        if self.__db:
            self.__logger.debug("Close cursor")
            self.cursor.close()
        else:
            self.__logger.debug("Cursor already closed")


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
        ra, dec = astronomy.str2rad(str(ra), str(dec))
        sql = "INSERT INTO `star` (`id`,`name`,`ra`,`dec`) VALUES (default, %(name)s,%(ra)s,%(dec)s)"
        args = {'name': name, 'ra': float(ra), 'dec': float(dec)}
        self.insert(sql, args)

    def updateStar(self, name, ra, dec):
        ra, dec = astronomy.str2rad(str(ra), str(dec))
        sql = "update `star` set`ra`=%(ra)s, `dec`=%(dec)s WHERE `name`=%(name)s"
        args = {'name': name, 'ra': float(ra), 'dec': float(dec)}
        self.update(sql, args)

    def deleteStar(self, star):
        sql = "DELETE FROM `star` WHERE `name`=%(name)s"
        args = {'name': star['name']}
        self.delete(sql, args)

    def getStarByName(self, name):
        """ Take star from database by name
  Star name and position in suitable form for customer
  If star does not exist, return None"""
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
        """
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
        """ Convert database resultset into dictionary (name,ra,dec)
        Attr:
          star - one record from DB
        """
        id = star[0]
        name = star[1]
        ra, dec = astronomy.rad2str(star[2], star[3])
        return {'id': id, 'name': name, 'ra': ra, 'dec': dec}


class Message(DBQuery):
    """ manage operations with messages in DB """

    def __init__(self, dbManager):
        super(Message, self).__init__(dbManager.getDb(), dbManager.getLog())

    #    def getMsgById(self, id):
    #        sql = "SELECT `text` FROM `message` where id=%(id)s"
    #        args = {'id': id}
    #        return str(self.selectOne(sql, args))

    def setNew(self, text):
        """ return added message id """
        sql = "INSERT INTO `message` (`id`,`text`) VALUES (default, %(text)s)"
        args = {'text': text}
        return self.insert(sql, args)

    def getLastId(self):
        """ return last stored message idd, if there is no return empty string """
        if self.getLastRow():
            return self.getLastRow()[0]

    def getLastMsg(self):
        """ return last stored message, if there is no return empty string """
        if self.getLastRow():
            return self.getLastRow()[1]
        else:
            return ""

    def getLastRow(self):
        sql = "SELECT `id`,`text` FROM `message` ORDER BY `id` DESC LIMIT 1"
        return self.selectOne(sql)



class Log(DBQuery):
    """ manage operations with logs in Log table """

    def __init__(self, dbManager):
        super(Log, self).__init__(dbManager.getDb(), dbManager.getLog())
        self.cleanValues()

    def saveLog(self):
        self.addRecord()
        self.cleanValues()

    def addRecord(self):
        sql = self.createSQL()
        args = self.fillArgs()
        self.insert(sql, args)

    def createSQL(self):
        fields = "(`id`, `star_id`, `msg_id`, `ra`, `dec`, `focus`,`temp_in`, `temp_out`,`status`)"
        values = "(default, %(star_id)s, %(msg_id)s, %(ra)s, %(dec)s, %(focus)s, %(temp_in)s, %(temp_out)s, %(status)s)"
        sql = "INSERT INTO `log` " + fields + " VALUES " + values
        return sql

    def fillArgs(self):
        return {'id': self.__id, 'star_id': self.__star_id, 'msg_id': self.__msg_id, 'ra': self.__ra, 'dec': self.__dec,
                'focus': self.__focus, 'temp_in': self.__temp_in, 'temp_out': self.__temp_out, 'status': self.__status}

    def cleanValues(self):
        #Parameters from program
        self.__id = None
        self.__star_id = None
        self.__msg_id = None
        #Parameters from PLC
        self.__ra = None
        self.__dec = None
        self.__focus = None
        self.__temp_in = None
        self.__temp_out = None
        self.__status = None #alarm status word

    def setStarId(self, id):
        self.__star_id = id

    def setMsgId(self, id):
        self.__msg_id = id

    def setCurrentRaDec(self, ra, dec):
        self.__ra = ra
        self.__dec = dec

    def setCurrentFocus(self, focus):
        self.__focus = focus

    def setTemperature(self, temp_in, temp_out):
        self.__temp_in = temp_in
        self.__temp_out = temp_out

    def setAlarmStatus(self, word):
        self.__status = word


