from core.config.SimpleConfig import SimpleConfig

__author__ = 'kitru'

class ProgramConfig(SimpleConfig):
    """ Get program configuration from default.conf file  """

    def __init__(self):
        configFileName = 'default'
        SimpleConfig.__init__(self, configFileName)
        self.readConfiguration(configFileName)

    #    def getPLCManager(self):
    #        """ Get communication configuration from config file. If communication section is missing raise  Configuration Exception  """
    #        logging.info('=== Communication initialization ===')
    #        commConfig = self.getConfigBySection('communication')
    #        return PLCManager(commConfig)

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

    def getLoggingTime(self):
        """ Find logging time """
        dict = self.getCommonConfigDict()
        self._logger.info('Read logging time')
        return float(dict['logging time']) * 60

    def getCommonConfigDict(self):
        """ Get common configuration from config file. If common section is missing raise  Configuration Exception  """
        return self.getConfigBySection('common')
