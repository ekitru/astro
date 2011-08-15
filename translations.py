from configuration import getLogger

__author__ = 'kitru'

class TranslationCodes(object):
    def __init__(self, codes):
        self.codes = codes
        self.logger = getLogger('astroTranslations')

    #        self.logger.info(codes)

    def get(self, key):
        """ Returns translation for code or key if translation is missing """
        if key.lower() in self.codes:
            return self.codes[key.lower()]
        else:
            self.logger.warning('Missing translation for ' + key)
            return key











  