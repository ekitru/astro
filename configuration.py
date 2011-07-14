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
    """ Get database configuration from config file. If Db section is missing raise  Configuration Exception
    Attributes:
        config - SafeConfigParser object
    """
    try:
        list =  config.items("db configuration")
        dictionary={}
        for item in list:
            dictionary[item[0]]=item[1]
        return dictionary

    except ConfigParser.NoSectionError as error:
        raise ConfigurationException(error.args)


def getDbConnection(config):
    """ Get db connection dased on config file
    Attributes:
        config - SafeConfigParser object
    """
    try:
        confDict = getDbConfig(config)
        db = MySQLdb.connect(confDict['host'], confDict['user'], confDict['password'], confDict['database'],
                             port=int(confDict['port']))
        return db
    except Exception as error:
        raise ConfigurationException(error.args)

