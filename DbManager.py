import MySQLdb
from configuration import ConfigurationException, getLogger

__author__ = 'kitru'

class DbManager(object):
    def __init__(self, confDict):
        self.logger = getLogger('astroDbManager')
        self.logger.info('Establish connection')
        self.conn = self.__getDbConnection(confDict)

    def __getDbConnection(self, confDict):
        """ Get db connection dased on config file
        Attributes:
            config - SafeConfigParser object
        """
        try:
            db = MySQLdb.connect(confDict['host'], confDict['user'], confDict['password'], confDict['database'],
                                 port=int(confDict['port']))
            return db
        except Exception as error:
            raise ConfigurationException(error.args, self.logger)

    def getVersion(self):
        cursor = self.conn.cursor()
        cursor.execute('select version()')
        row = cursor.fetchone()
        return row

  