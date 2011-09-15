import logging
from os.path import join

__author__ = 'kitru'

def getLog(name):
    logger = logging.getLogger(name)
    fileHandler = logging.FileHandler(join('logs', name + '.log'), mode='w')
    fileHandler.setFormatter(logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s'))
    logger.addHandler(fileHandler)
    return logger

def closeLog(log):
    log.debug("close "+log.name+" log")
    x = list(log.handlers)
    for i in x:
        log.removeHandler(i)
        i.flush()
        i.close()
  