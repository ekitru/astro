import ConfigParser
import codecs
import MySQLdb

__author__ = 'kitru'

class ConfigurationException(Exception):
    """Exception raised for errors during configuration system.

    Attributes:
        msg  -- explanation of the error
    """

    def __init__(self, msg):
        Exception.__init__(self, msg)


def getConfigFromFile(fileName):
    """ Opens configuration file. If file is missing or could not be read, new COnfigurationException will be raised    """
    try:
        config = ConfigParser.SafeConfigParser()
        config.readfp(codecs.open(fileName, "r", "utf8"))
        return config
    except IOError as error:
        print(error.message)
        raise ConfigurationException(error.args)


def getDbConfig(config):
    try:
        list =  config.items("db configuration")
        dictionary={}
        for item in list:
            dictionary[item[0]]=item[1]
        return dictionary

    except ConfigParser.NoSectionError as error:
        raise ConfigurationException(error.args)


def getDbConnection(config):
    dbConfigList = getDbConfig(config)
    print(dbConfigList)
    db = MySQLdb.connect(dbConfigList['host'], dbConfigList['user'], dbConfigList['password'], dbConfigList['database'],
                         port=int(dbConfigList['port']))
    return db

if __name__ == '__main__':
    config = getConfigFromFile("default.cnf")
    db = getDbConnection(config)
    cursor = db.cursor()
    cursor.execute('select version()')
    row = cursor.fetchone()
    print(row)

    pass