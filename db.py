# -*- coding: utf-8 -*-

import MySQLdb
import astronomy

from Exceptions import ConfigurationException, DbException
from logger import getLog, closeLog


__author__ = 'kitru'

class DbManager(object):
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
        sql = "INSERT INTO `stars` (`id`,`name`,`ra`,`dec`) values (default, %(name)s,%(ra)s,%(dec)s)"
        args = {'name': name, 'ra': float(ra), 'dec': float(dec)}
        self.insert(sql, args)

    def updateStar(self, name, ra, dec):
        ra, dec = astronomy.str2rad(str(ra), str(dec))
        sql = "update `stars` set`ra`=%(ra)s, `dec`=%(dec)s where `name`=%(name)s"
        args = {'name': name, 'ra': float(ra), 'dec': float(dec)}
        self.update(sql, args)

    def deleteStar(self, star):
        sql = "delete from `stars` where `name`=%(name)s"
        args = {'name': star['name']}
        self.delete(sql, args)

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
        sql = "INSERT INTO `message` (`id`,`text`) values (default, %(text)s)"
        args = {'text': text}
        return self.insert(sql, args)

    def getLast(self):
        """ return last stored message, if there is no return empty string """
        sql = "SELECT `text` FROM `message` ORDER BY `id` DESC LIMIT 1"
        ret = self.selectOne(sql)
        if len(ret)==1:
            return ret[0]
        else:
            return ""





