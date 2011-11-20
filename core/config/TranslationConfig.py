from os.path import join

from core.Exceptions import ConfigurationException
from core.config.SimpleConfig import SimpleConfig

__author__ = 'kitru'

class TranslationConfig(SimpleConfig):
    """ Reads tranlation codes for selected language. Translation file should be placed in ./resources/trans  """
    def __init__(self, lang):
        """ Reads translation file and opens new translation log """
        SimpleConfig.__init__(self, 'translations')
        try:
            self._logger.info('Read translation codes for ' + lang)
            self._getTranslationConfig(lang)
            self._codes = self.getConfigBySection('codes')
        except Exception as ex:
            msg = ex.args + (lang,)
            raise ConfigurationException(msg, self._logger)

    def get(self, key):
        """ Get translation for code - key. The keys are case insensitive
        Attr:
            key - code, need to be trnaslated
        Return:
            translation or key  value """
        if key.lower() in self._codes:
            return self._codes[key.lower()]
        else:
            self._logger.warning('Missing translation code ' + key)
            self._codes[key.lower()] = key.lower()
            return key

    def _getTranslationConfig(self, language):
        """ Return SafeConfigParser from name.conf file   """
        self._logger.info('Read translations for ' + language)
        return self.readConfiguration(join('resources', 'trans', language))

  