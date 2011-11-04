from core.config.SimpleConfig import SimpleConfig

__author__ = 'kitru'

class ProgramConfig(SimpleConfig):
    """ Get program configuration from default.conf file  """

    _configFileName = 'default'

    def __init__(self):
        SimpleConfig.__init__(self, self._configFileName)
        self.readConfiguration(self._configFileName)

    def saveConfig(self):
        self.saveConfiguration(self._configFileName)

    def getLogger(self):
        return self._logger

    def getDbConfig(self):
        """ Get database connection configuration """
        return self.getConfigBySection('db configuration')

    def getObserverConfig(self):
        """ Get observer position for telescope  """
        return self.getConfigBySection('observer')


    def getDefaultLanguage(self):
        """ Find default translation language from config file """
        dict = self.getCommonConfigDict()
        self._logger.info('Read default translation codes')
        return dict['default translation']

    def setDefaultLanguage(self, lang):
        """ Set new default language """
        self._logger.info('Write new defult langguage ' + lang)
        self._config.set('common', 'default translation', lang)

    def getLoggingTime(self):
        """ Find logging time """
        dict = self.getCommonConfigDict()
        self._logger.info('Read logging time')
        return float(dict['logging time']) * 60

    def setLoggingTime(self, time):
        """ Set new logging time """
        self._logger.info('Write new logging time ' + time)
        self._config.set('common', 'logging time', time)


    def getCommonConfigDict(self):
        """ Get common configuration from config file. If common section is missing raise  Configuration Exception  """
        return self.getConfigBySection('common')
