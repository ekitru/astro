# -*- coding: utf-8 -*-

import MySQLdb
from Exceptions import ConfigurationException
from logger import getLog


__author__ = 'kitru'

class DbManager(object):
    def __init__(self, confDict):
        self.logger = getLog('database')
        self.database = confDict['database']
        self.conn = self.__getDbConnection(confDict)
        self.cursor = self.conn.cursor()

    def __getDbConnection(self, confDict):
        """ Get db connection dased on config file
        Attributes:
            config - SafeConfigParser object
        """
        try:
            self.logger.info('Establishing connection')
            db = MySQLdb.connect(confDict['host'], confDict['user'], confDict['password'], confDict['database'],
                                 port=int(confDict['port']), charset = "utf8", use_unicode = True)
            self.logger.info('Connection established')
            return db
        except Exception as error:
            raise ConfigurationException(error.args, self.logger)

    def getStarById(self, id):
        sql = "SELECT `name`,`ra`,`dec` FROM stars where id=%(id)s"
        args = {'id': id}

        self.cursor.execute(sql, args)
        return self.cursor.fetchone()

    def getStarByName(self, name):
        sql = "SELECT `name`,`ra`,`dec` FROM stars where name=%(name)s"
        args = {'name': name}

        self.cursor.execute(sql, args)
        return self.cursor.fetchone()

    def saveStar(self, name, ra, dec):
        sql = "INSERT INTO `stars` (`id`,`name`,`ra`,`dec`) values (default, %(name)s,%(ra)s,%(dec)s)"
        args = {'name': name, 'ra':ra,'dec':dec}

        self.cursor.execute(sql, args)
        return self.cursor.fetchone()

    def getStarsByPartName(self, name):
        """ looks for all like name%   """
        name = name.encode('utf-8')
        sql = "select `name`,`ra`,`dec` from stars where name like %(name)s  limit 20"
        args = {'name': (name + '%')}

        self.cursor.execute(sql, args)
        return self.cursor.fetchall()

    def close(self):
        self.logger.info("Close DB connection")
        self.cursor.close()
        self.conn.close()
