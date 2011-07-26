from configuration import getLogger

__author__ = 'kitru'

class CommManager(object):
    def __init__(self, confDict):
        self.logger = getLogger('astroCommManager')
        self.logger.info('Establish connection')
        print(confDict)


  