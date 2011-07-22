import ConfigParser
import codecs
import logging
from os.path import join

__author__ = 'kitru'

class ConfigurationException(Exception):
    """Exception raised for errors during configuration system.
    Attributes:
        msg  -- explanation of the error
    """

    def __init__(self, msg):
        Exception.__init__(self, msg)


class Configuration(object):
    """Get configuration from file

    Contains all configurations for DB,MODBUS and Translations
    """

    def __init__(self, configFileName):
        logging.info('Read configuration file:' + configFileName)
        self.config = self.__getConfigFromFile(configFileName)

    def __getConfigFromFile(self, fileName):
        """ Opens configuration file. If file is missing or could not be read, new COnfigurationException will be raised    """
        try:
            config = ConfigParser.SafeConfigParser()
            config.readfp(codecs.open(fileName, "r", "utf8"))
            return config
        except IOError as error:
            print(error.message)
            raise ConfigurationException(error.args)

    def getCommonConfigDict(self):
        """ Get common configuration from config file. If common section is missing raise  Configuration Exception  """
        return self.__getConfigBySection("common")

    def getDbConfigDict(self):
        """ Get database configuration from config file. If Db section is missing raise  Configuration Exception  """
        return self.__getConfigBySection("db configuration")

    def getCommunicationConfigDict(self):
        """ Get communication configuration from config file. If communication section is missing raise  Configuration Exception  """
        return self.__getConfigBySection("communication")

    def __getConfigBySection(self, section_name):
        try:
            return self.__getItemsBySection(self.config, section_name)
        except ConfigParser.NoSectionError as error:
            raise ConfigurationException(error.args)

    def __getItemsBySection(self, config, section_name):
        """   Return dictionary of selected section items      """
        list = config.items(section_name)
        return dict(list)


    # Tranlation stuff
    def getCodes(self):
        language = self.getDefaultLanguage()
        curTrans = self.__getTranslationConfig(language)
        codes = self.__getItemsBySection(curTrans, 'codes')
        return codes


    def getDefaultLanguage(self):
        """
        Find default translation from config file
        """
        dict = self.getCommonConfigDict()
        return dict["default translation"]

    def __getTranslationConfig(self, language):
        """
        Return SafeConfigParser from name.cnf file
        """
        return self.__getConfigFromFile(join("trans", language + ".cnf"))

