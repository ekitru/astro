import ConfigParser
import codecs
from core.Exceptions import ConfigurationException
from core.logger import openLog, closeLog

__author__ = 'kitru'

class SimpleConfig(object):
    """ Abstract for reading system configuration files.    """

    def __init__(self, name):
        """ Writes log to name_config.log file
        Attr:
            name - logger name
        """
        self._logger = openLog('config_' + name)

    def __del__(self):
        """ Close logger before object closing """
        closeLog(self._logger)

    def readConfiguration(self, fileName):
        """ Opens configuration file. If file is missing or could not be read, new ConfigurationException will be raised.
        Attr:
            fileName - configuration file name
        """
        try:
            self._logger.info('Read configuration file: ' + fileName)
            self._config = ConfigParser.SafeConfigParser()
            self._config.readfp(codecs.open(fileName + '.conf', "r", "utf8"))
            return self._config
        except IOError as error:
            msg = error.args + (fileName,)
            raise ConfigurationException(msg, self._logger)

    def _getItemsBySection(self, section_name):
        """ Return dictionary of selected section items """
        list = self._config.items(section_name)
        return dict(list)

    def getConfigBySection(self, section_name):
        try:
            self._logger.info('Read section ' + '\"' + section_name + '\"')
            return self._getItemsBySection(section_name)
        except ConfigParser.NoSectionError as error:
            msg = error.args + (section_name,)
            raise ConfigurationException(msg, self._logger)
