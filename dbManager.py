import MySQLdb
from configuration import ConfigurationException

__author__ = 'kitru'

def getDbConnection(confDict):
    """ Get db connection dased on config file
    Attributes:
        config - SafeConfigParser object
    """
    try:
        db = MySQLdb.connect(confDict['host'], confDict['user'], confDict['password'], confDict['database'],
                             port=int(confDict['port']))
        return db
    except Exception as error:
        raise ConfigurationException(error.args)


  