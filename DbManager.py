import MySQLdb
from config import ConfigurationException, getLogger

__author__ = 'kitru'

class DbManager(object):
    def __init__(self, confDict):
        self.logger = getLogger('database')
        self.database = confDict['database']
        self.conn = self.__getDbConnection(confDict)

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

    def saveNewStar(self,name,alfa,delta):
        sql = "INSERT INTO stars SET name='"+name+"', alfa="+alfa+",delta="+delta+";"
        cursor = self.conn.cursor()
        cursor.execute(sql)
        cursor.close()

    def getStar(self,name):
        sql = "SELECT name,alfa,delta FROM stars where name='"+name+"';"
        cursor = self.conn.cursor()
        cursor.execute(sql)
        response = cursor.fetchone()
        cursor.close()
        return response

    def close(self):
        self.logger.info("Close DB connection")
        self.conn.close()

  