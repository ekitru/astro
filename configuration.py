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

    def __init__(self, msg, logger=None):
        Exception.__init__(self, msg)
        if logger:
            logger.error(msg)


def getLogger(name):
    logger = logging.getLogger(name)
    fileHandler = logging.FileHandler(name + '.log', mode='w')
    fileHandler.setFormatter(logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s'))
    logger.addHandler(fileHandler)
    return logger


class Configuration(object):
    """Get configuration from file

    Contains all configurations for DB,MODBUS and Translations
    """

    def __init__(self, configFileName):
        self.logger = getLogger('astroConfig')
        self.logger.info('Read configuration file:' + configFileName)
        self.config = self.__getConfigFromFile(configFileName)

    def __getConfigFromFile(self, fileName):
        """ Opens configuration file. If file is missing or could not be read, new COnfigurationException will be raised    """
        try:
            config = ConfigParser.SafeConfigParser()
            config.readfp(codecs.open(fileName, "r", "utf8"))
            return config
        except IOError as error:
            msg = error.args + (fileName,)
            raise ConfigurationException(msg,self.logger)

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
            self.logger.info('Read section ' + '\"' + section_name + '\"')
            return self.__getItemsBySection(self.config, section_name)
        except ConfigParser.NoSectionError as error:
            raise ConfigurationException(error.args,self.logger)

    def __getItemsBySection(self, config, section_name):
        """   Return dictionary of selected section items      """
        list = config.items(section_name)
        return dict(list)


    # Tranlation stuff
    def getCodes(self):
        try:
            self.logger.info('Get translation codes')
            language = self.getDefaultLanguage()
            curTrans = self.__getTranslationConfig(language)
            codes = self.__getItemsBySection(curTrans, 'codes')
            return codes
        except Exception as ex: #TODO may be create new exception, like Translation exception?
            raise ConfigurationException(ex.args,self.logger)


    def getDefaultLanguage(self):
        """
        Find default translation from config file
        """
        dict = self.getCommonConfigDict()
        self.logger.info('Read default translation')
        return dict["default translation"]

    def __getTranslationConfig(self, language):
        """
        Return SafeConfigParser from name.cnf file
        """
        self.logger.info('Read translations for ' + language)
        return self.__getConfigFromFile(join("trans", language + ".cnf"))

