import logging
from os.path import join

from Exceptions import ConfigurationException
from SystemConfig import  SystemConf

from DbManager import DbManager
from CommManager import CommManager
from AstroMechanics import AstroMechanics

__author__ = 'kitru'

class ProgramConfig(SystemConf):
    """Get configuration from file
    Contains all configurations for DB,MODBUS and Translations
    """

    def __init__(self, configFileName):
        SystemConf.__init__(self, 'programConfig')
        self.logger.info('Read configuration file: ' + configFileName)
        self.config = self.getConfigFromFile(configFileName)

    def getPLCManager(self):
        """ Get communication configuration from config file. If communication section is missing raise  Configuration Exception  """
        logging.info('=== Communication initialization ===')
        commConfig = self.getConfigBySection(self.config, "communication")
        return CommManager(commConfig)

    def getDbManager(self):
        logging.info('=== DB initialization ===')
        dbConfig = self.getConfigBySection(self.config, "db configuration")
        return DbManager(dbConfig)

    def openAstroMechanics(self):
        """ get observer for telescope position """
        logging.info('=== Reading telescope configurations ===')
        configs = self.getConfigBySection(self.config, "observer")
        return AstroMechanics(configs)

    def getTranslationConf(self):
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
        return self.getConfigBySection(self.config, "common")


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
