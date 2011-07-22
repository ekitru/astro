__author__ = 'kitru'

class Translate(object):
    def __init__(self, codes):
        self.codes = codes

    def get(self, key):
        """
        return right translation or key
        """
        if key in self.codes:
            return self.codes[key]
        else:
            return key











  