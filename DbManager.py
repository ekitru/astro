# -*- coding: utf-8 -*-

import MySQLdb
from Exceptions import ConfigurationException, DbException
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
                                 port=int(confDict['port']), charset="utf8", use_unicode=True)
            self.logger.info('Connection established')
            return db
        except Exception as error:
            raise ConfigurationException(error.args, self.logger)

    def getStarById(self, id):
        try:
            sql = "SELECT `name`,`ra`,`dec` FROM stars where id=%(id)s"
            args = {'id': id}
            self.cursor.execute(sql, args)
            return self.cursor.fetchone()
        except Exception as error:
            raise DbException(error.args, self.logger)

    def getStarByName(self, name):
        try:
            sql = "SELECT `name`,`ra`,`dec` FROM stars where name=%(name)s"
            args = {'name': name}
            self.cursor.execute(sql, args)
            return self.cursor.fetchone()
        except Exception as error:
            raise DbException(error.args, self.logger)

    def saveStar(self, name, ra, dec):
        try:
            sql = "INSERT INTO `stars` (`id`,`name`,`ra`,`dec`) values (default, %(name)s,%(ra)s,%(dec)s)"
            args = {'name': name, 'ra': ra, 'dec': dec}
            self.cursor.execute(sql, args)
        except Exception as error:
            raise DbException(error.args, self.logger)

    def getStarsByPartName(self, name):
        """ looking for start by name like name%   """
        try:

            name = name.encode('utf-8')
            sql = "select `name`,`ra`,`dec` from stars where name like %(name)s  limit 20"
            args = {'name': (name + '%')}
            self.cursor.execute(sql, args)
            return self.cursor.fetchall()
        except Exception as error:
            raise DbException(error.args, self.logger)

    def close(self):
        try:
            self.logger.info("Close DB connection")
            self.cursor.close()
            self.conn.close()
        except Exception as error:
            raise DbException(error.args, self.logger)
