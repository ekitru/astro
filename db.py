# -*- coding: utf-8 -*-

import MySQLdb
from Exceptions import ConfigurationException, DbException
import astronomy
from logger import getLog


__author__ = 'kitru'

class DbManager(object):
    def __init__(self, confDict):
        self.logger = getLog('database')
        self.database = confDict['database']
        self.db = self.__getDbConnection(confDict)

    def __getDbConnection(self, confDict):
        """ Get db connection dased on config file
        Attributes:
            config - SafeConfigParser object
        """
        try:
            self.logger.info('Establishing connection')
            db = MySQLdb.connect(confDict['host'], confDict['user'], confDict['password'], confDict['database'],
                                 port=int(confDict['port']), charset="utf8", use_unicode=True)
            self.logger.info('Connection established')
            return db
        except Exception as error:
            raise ConfigurationException(error.args, self.logger)

    def getDb(self):
        return self.db

    def getLog(self):
        return self.logger

    def close(self):
        self.logger.info("Close DB connection")
        self.db.close()


class DBQuery(object):
    def __init__(self, db, logger):
        self.db = db
        self.cursor = db.cursor()
        self.logger = logger

    def selectOne(self, sql, args):
        try:
            self.cursor.execute(sql, args)
            return self.cursor.fetchone()
        except Exception as error:
            raise DbException(error.args, self.logger)

    def selectAll(self, sql, args):
        try:
            self.cursor.execute(sql, args)
            return self.cursor.fetchall()
        except Exception as error:
            raise DbException(error.args, self.logger)

    def close(self):
        self.cursor.close()


class Star(DBQuery):
    """ manage operations with stars in DB """

    def __init__(self, db, logger):
        DBQuery.__init__(self, db, logger)
        self.db = db
        self.cursor = db.cursor()

    def starExists(self, name):
        """ Check DB for record with same name """
        star = self.getStarByName(name)
        if star:
            return True
        else:
            return False

    def getStarByName(self, name):
        """ Take star from database by name
  Star name and position in suitable form for customer
  If star does not exist, return None"""
        sql = "SELECT `name`,`ra`,`dec` FROM `stars` where name=%(name)s"
        args = {'name': name}

        star = self.selectOne(sql, args)
        if star:
            return self.parseStar(star)
        else:
            return None

    def saveStar(self, name, ra, dec):
        ra, dec = astronomy.str2rad(str(ra), str(dec))
        sql = "INSERT INTO `stars` (`id`,`name`,`ra`,`dec`) values (default, %(name)s,%(ra)s,%(dec)s)"
        args = {'name': name, 'ra': float(ra), 'dec': float(dec)}
        self.cursor.execute(sql, args)

    def updateStar(self, name, ra, dec):
        ra, dec = astronomy.str2rad(str(ra), str(dec))
        sql = "update `stars` set`ra`=%(ra)s, `dec`=%(dec)s where `name`=%(name)s"
        args = {'name': name, 'ra': float(ra), 'dec': float(dec)}
        self.cursor.execute(sql, args)

    def deleteStar(self, star):
        sql = "delete from `stars` where `name`=%(name)s"
        args = {'name': star['name']}
        self.cursor.execute(sql, args)

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
        sql = "select `name`,`ra`,`dec` from `stars` where name like %(name)s order by `name`  limit 20"
        args = {'name': (name + '%')}
        return self.selectAll(sql, args)

    def parseStar(self, star):
        """ Convert database resultset into dictionary (name,ra,dec)
        Attr:
          star - one record from DB
        """
        name = star[0]
        ra, dec = astronomy.rad2str(star[1], star[2])
        return {'name': name, 'ra': ra, 'dec': dec}

class Message(object):
    """ manage operations with messages in DB """

    def __init__(self, db):
        self.db = db
        self.cursor = db.cursor()

    def getMsgById(self, id):
        sql = "SELECT `text` FROM `message` where id=%(id)s"
        args = {'id': id}

        self.cursor.execute(sql, args)
        return self.cursor.fetchone()

    def addMessage(self, text):
        sql = "INSERT INTO `message` (`id`,`text`) values (default, %(text)s)"
        args = {'text': text}
        return self.cursor.execute(sql, args)



