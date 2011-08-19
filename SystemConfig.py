import ConfigParser
import codecs
import logging
from os.path import join
from Exceptions import ConfigurationException

__author__ = 'kitru'

def getLog(name):
    logger = logging.getLogger(name)
    fileHandler = logging.FileHandler(join('logs', name + '.log'), mode='w')
    fileHandler.setFormatter(logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s'))
    logger.addHandler(fileHandler)
    return logger


class SystemConf(object):
    def __init__(self, loggerName):
        self.logger = getLog(loggerName)

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

  