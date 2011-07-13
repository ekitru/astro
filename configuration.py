import ConfigParser
import codecs

__author__ = 'kitru'

def getConfigFromFile(fileName):
    """ Opens configuration file    """
    config = ConfigParser.SafeConfigParser()
    config.readfp(codecs.open(fileName,"r","utf8"))
    return config

if __name__ == '__main__':
    config = getConfigFromFile("default.cnf")
    config.get
    print(config.get('db section','name'))
    pass