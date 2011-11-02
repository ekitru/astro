from os.path import join

from core.Exceptions import ConfigurationException
from core.config.SimpleConfig import SimpleConfig

__author__ = 'kitru'

class TranslationConfig(SimpleConfig):
    def __init__(self, lang):
        SimpleConfig.__init__(self, 'translations')
        try:
            self._logger.info('Read translation codes for ' + lang)
            self._getTranslationConfig(lang)
            self._codes = self.getConfigBySection('codes')
        except Exception as ex:
            msg = ex.args + (lang,)
            raise ConfigurationException(msg, self._logger)

    def get(self, key):
        if key.lower() in self._codes:
            return self._codes[key.lower()]
        else:
            self._logger.warning('Missing translation code ' + key)
            return key

    def _getTranslationConfig(self, language):
        """
        Return SafeConfigParser from name.conf file
        """
        self._logger.info('Read translations for ' + language)
        return self.readConfiguration(join('resources', 'trans', language))

  