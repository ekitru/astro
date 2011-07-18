from os.path import join
from configuration import getConfigFromFile, getItemsBySection

__author__ = 'kitru'

def getSelectedTranslation(config):
    """
    Return codes for selected language
    """
    name = getSelectedLanguage(config)
    return getCodes(name)


def getSelectedLanguage(config):
    """
    Find selected translation from default config file
    """
    return config.get("common", "selected")


def getCodes(name):
    curTrans = getTranslationConfig(name)
    codes = getItemsBySection(curTrans, 'codes')
    return codes


def getTranslationConfig(name):
    """
    Return SafeConfigParser from name.cnf file
    """
    return getConfigFromFile(join("trans", name + ".cnf"))






  