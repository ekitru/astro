import ConfigParser
import codecs
import logging
from os.path import join

__author__ = 'kitru'

def getLogger(name):
    logger = logging.getLogger(name)
    fileHandler = logging.FileHandler(join('logs', name + '.log'), mode='w')
    fileHandler.setFormatter(logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s'))
    logger.addHandler(fileHandler)
    return logger


class ConfigurationException(Exception):
    """Exception raised for errors during configuration system.
    Attributes:
        msg  -- explanation of the error
    """

    def __init__(self, msg, logger=None):
        Exception.__init__(self, msg)
        if logger:
            logger.error(msg)


class SystemConf(object):
    def __init__(self, loggerName):
        self.logger = getLogger(loggerName)

    def getConfigFromFile(self, fileName):
        """ Opens configuration file. If file is missing or could not be read, new ConfigurationException will be raised    """
        try:
            config = ConfigParser.SafeConfigParser()
            config.readfp(codecs.open(fileName, "r", "utf8"))
            return config
        except IOError as error:
            msg = error.args + (fileName,)
            raise ConfigurationException(msg, self.logger)

    def getItemsBySection(self, config, section_name):
        """   Return dictionary of selected section items      """
        list = config.items(section_name)
        return dict(list)

    def getConfigBySection(self, config, section_name):
        try:
            self.logger.info('Read section ' + '\"' + section_name + '\"')
            return self.getItemsBySection(config, section_name)
        except ConfigParser.NoSectionError as error:
            raise ConfigurationException(error.args, self.logger)


class ProgramConfig(SystemConf):
    """Get configuration from file
    Contains all configurations for DB,MODBUS and Translations
    """

    def __init__(self, configFileName):
        SystemConf.__init__(self, 'programConfig')
        self.logger.info('Read configuration file: ' + configFileName)
        self.config = self.getConfigFromFile(configFileName)

    def getCommonConfigDict(self):
        """ Get common configuration from config file. If common section is missing raise  Configuration Exception  """
        return self.getConfigBySection(self.config, "common")

    def getObserverDict(self):
        """ Get observer parameters: position, altitude, eval  """
        return self.getConfigBySection(self.config, "observer")

    def getDbConfigDict(self):
        """ Get database configuration from config file. If Db section is missing raise  Configuration Exception  """
        return self.getConfigBySection(self.config, "db configuration")

    def getCommunicationConfigDict(self):
        """ Get communication configuration from config file. If communication section is missing raise  Configuration Exception  """
        return self.getConfigBySection(self.config, "communication")

    def getDefaultLanguage(self):
        """ Find default translation from config file """
        dict = self.getCommonConfigDict()
        self.logger.info('Read default translation')
        return dict["default translation"]


class TransConf(SystemConf):
    def __init__(self, lang):
        SystemConf.__init__(self, 'translations')
        try:
            self.logger.info('Get translation codes')
            config = self.getTranslationConfig(lang)
            self.codes = self.getItemsBySection(config, 'codes')
        except Exception as ex: #TODO may be create new exception, like Translation exception?
            raise ConfigurationException(ex.args, self.logger)

    def get(self, key):
        if key.lower() in self.codes:
            return self.codes[key.lower()]
        else:
            self.logger.warning('Missing translation for ' + key)
            return key

    def getTranslationConfig(self, language):
        """
        Return SafeConfigParser from name.conf file
        """
        self.logger.info('Read translations for ' + language)
        return self.getConfigFromFile(join("trans", language + ".conf"))
