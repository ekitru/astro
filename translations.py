from configuration import getLogger

__author__ = 'kitru'

class Translate(object):
    def __init__(self, codes):
        self.codes = codes
        self.logger = getLogger('astroTranslations')

    def get(self, key):
        """
        return right translation or key
        """
        if key in self.codes:
            return self.codes[key]
        else:
            self.logger.warning('Missing translation for '+key)
            return key











  