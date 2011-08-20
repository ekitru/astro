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
                                 port=int(confDict['port']))
            self.logger.info('Connection established')
            return db
        except Exception as error:
            raise ConfigurationException(error.args, self.logger)

    def getStarById(self, id):
        sql = "SELECT * FROM stars where id=%(id)s"
        args = {'id': id}

        self.cursor.execute(sql, args)
        return self.cursor.fetchone()

    def getStarsByPartName(self, name):
        """ looks for all like name%   """
        sql = "select * from stars where name like %(name)s  limit 50"
        args = {'name': (name + '%')}

        self.cursor.execute(sql, args)
        return self.cursor.fetchall()

    def close(self):
        self.logger.info("Close DB connection")
        self.cursor.close()
        self.conn.close()
