import logging
import os
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
    logPath = getLogPath()
    path = join(logPath, name + '.log')
    fileHandler = logging.FileHandler(path, mode='w')
    fileHandler.setFormatter(logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s'))
    logger.addHandler(fileHandler)
    return logger

def closeLog(log):
    """ Close selected log
    Attr:
        log logger object to be closed
    """
    if log:
        log.info("Close "+log.name+" log")
        x = list(log.handlers)
        for i in x:
            log.removeHandler(i)
            i.flush()
            i.close()

def getLogPath():
        logPath = join('resources', 'logs')
        if not os.path.exists(logPath):
            os.makedirs(logPath, mode=0777)
        return logPath







