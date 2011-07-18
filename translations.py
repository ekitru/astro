from os.path import join
from configuration import getConfigFromFile, getItemsBySection

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


def getSelectedTranslation(config):
    """
    Return codes for selected language
    """
    name = _getSelectedLanguage(config)
    return _getCodes(name)


def _getSelectedLanguage(config):
    """
    Find selected translation from default config file
    """
    return config.get("common", "selected")


def _getCodes(name):
    curTrans = _getTranslationConfig(name)
    codes = getItemsBySection(curTrans, 'codes')
    return codes


def _getTranslationConfig(name):
    """
    Return SafeConfigParser from name.cnf file
    """
    return getConfigFromFile(join("trans", name + ".cnf"))






  