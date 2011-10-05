import ConfigParser
import codecs
import logging
from os.path import join

from Exceptions import ConfigurationException
from logger import  getLog, closeLog

from db import DbManager
from PLCManager import PLCManager
from astronomy import Observer

__author__ = 'kitru'

class SystemConf(object):
    def __init__(self, loggerName):
        self.logger = getLog(loggerName)

    def __del__(self):
        closeLog(self.logger)


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
        self._config = self.getConfigFromFile(configFileName)

    def getPLCManager(self):
        """ Get communication configuration from config file. If communication section is missing raise  Configuration Exception  """
        logging.info('=== Communication initialization ===')
        commConfig = self.getConfigBySection(self._config, "communication")
        return PLCManager(commConfig)

    def getDbManager(self):
        logging.info('=== DB initialization ===')
        dbConfig = self.getConfigBySection(self._config, "db configuration")
        return DbManager(dbConfig)

    def getObserver(self):
        """ get observer for telescope position """
        logging.info('=== Reading telescope configurations ===')
        configs = self.getConfigBySection(self._config, "observer")
        return Observer(configs)

    def getTranslation(self):
        logging.info('=== Reading translation page  ===')   #Read selected language translation
        language = self.getDefaultLanguage()
        return TransConf(language)

    def getDefaultLanguage(self):
        """ Find default translation from config file """
        dict = self.getCommonConfigDict()
        self.logger.info('Read default translation')
        return dict["default translation"]

    def getCommonConfigDict(self):
        """ Get common configuration from config file. If common section is missing raise  Configuration Exception  """
        return self.getConfigBySection(self._config, "common")
#        e=self.getConfigBySection(self.config, "common")

    def setCommonConfigDict(self, comDict):
        """ Takes a dictionary and saves into common dictionary """

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
