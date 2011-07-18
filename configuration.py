import ConfigParser
import codecs

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


def getItemsBySection(config, sectionName):
    """   Return dictionary of selected section items
    Attributes:
        config - config file object (SafeConfigParser
    """
    list = config.items(sectionName)
    dictionary = {}
    for key, value in list:
        dictionary[key] = value
    return dictionary


def getDbConfig(config):
    """ Get database configuration from config file. If Db section is missing raise  Configuration Exception
    Attributes:
        config - SafeConfigParser object
    """
    try:
        sectionName = "db configuration"
        return getItemsBySection(config, sectionName)
    except ConfigParser.NoSectionError as error:
        raise ConfigurationException(error.args)

