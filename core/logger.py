import logging
from os.path import join

__author__ = 'kitru'

def openLog(name):
    """ Open new logger with FileHandler with filename: name.log
    Attr:
        name filename, full path if resources/logs/name.log
    Return:
        new logger from  logging module
    """
    logger = logging.getLogger(name)
    path = join('resources', 'logs', name + '.log')
    fileHandler = logging.FileHandler(path, mode='w')
    fileHandler.setFormatter(logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s'))
    logger.addHandler(fileHandler)
    return logger

def closeLog(log):
    """ Close selected log
    Attr:
        log logger object to be closed
    """
    log.info("close "+log.name+" log")
    x = list(log.handlers)
    for i in x:
        log.removeHandler(i)
        i.flush()
        i.close()







