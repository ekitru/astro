from configuration import getLogger

__author__ = 'kitru'

class Translate(object):
    def __init__(self, codes):
        self.codes = codes
        self.logger = getLogger('astroTranslations')
        self.logger.info(codes)

    def get(self, key):
        """
        return right translation or key
        """
        if key.lower() in self.codes:
            return self.codes[key.lower()]
        else:
            self.logger.warning('Missing translation for ' + key)
            return key











  