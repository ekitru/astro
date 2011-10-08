# -*- coding: utf-8 -*-
import MySQLdb
from Exceptions import ConfigurationException
from logger import getLog, closeLog


__author__ = 'kitru'

class DbManager(object):
    """ Manage DB connection
    handle it opening and closing, also handle db log """

    def __init__(self, confDict):
        self._logger = getLog('database')
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
