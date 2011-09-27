import os
from posixpath import join
import logging
from db import  Message, Log
from db import Star

from Exceptions import ConfigurationException, InitializationException, ClosingException
from Configs import ProgramConfig
from astronomy import Object
import astronomy
from LogThread import LogThread

__author__ = 'kitru'

class ResourceKeeper(object):
    def __init__(self, config):
        self._codes = config.getTranslation()
        self._PLCManager = config.getPLCManager()
        self._dbManager = config.getDbManager()
        self._star = Star(self._dbManager)
        self._log = Log(self._dbManager)
        self._message = Message(self._dbManager)

    def __del__(self):
        del self._message
        del self._log
        del self._star
        del self._dbManager
        del self._PLCManager
        del self._codes

    def getCodes(self):
        return self._codes

    def getPLCManager(self):
        return self._PLCManager

    def getDbManager(self):
        return self._dbManager

    def getStarHolder(self):
        return self._star

    def getLogHolder(self):
        return self._log

    def getMessageHolder(self):
        return self._message


class Controller(object):
    __controlMode = True
    def __init__(self):
        self.__initLogger()
        self.object = None
        self.currentCoordinates = Coordinates()  #read from PLC
        self.setpointCoordinates = Coordinates() #sent to PLC
        self.currentFocus = Focus()     #read from PLC
        self.setpointFocus = Focus()    #sent to PLC
        self.manPosition = None
        self.manFocus = None

    def __initLogger(self):
        if not os.path.exists('logs'):
            os.makedirs('logs', mode=0711)
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                            datefmt='%m-%d %H:%M',
                            filename=join('logs', 'common.log'),
                            filemode='w')

    def initialization(self):
        """ Initialization for all components
        Opens DB connection and connection with PLCm also reads translation codes """
        try:
            logging.info('======= Program initialization =======')
            config = ProgramConfig('default.conf')
            self.observer = config.getObserver()
            self.object = Object(self.observer)

            self._resourceKeeper = ResourceKeeper(config)
            minutes = float(config.getCommonConfigDict()['logging time'])
            self.logThread = LogThread(self, minutes)
        except ConfigurationException as ce:
            logging.error('Erron during initialization occure: ' + ce.__str__())
            raise InitializationException(ce)


    def freeResources(self):
        try:
            logging.info('======= Free all resources: DB, MODBUS =======')
            # close database connections
            self.logThread._stop()
            del self._resourceKeeper
        except Exception as e:
            raise ClosingException(e)

    def getResourceKeeper(self):
        return self._resourceKeeper

    def setObject(self, name):
        """ Stores new object for observer
        Attr:
            name - star name
        """
        star = self._resourceKeeper.getStarHolder().getStarByName(name)
        if star:
            self.object.init(star['id'], star['name'], star['ra'], star['dec'])

    def getObject(self):
        return self.object

    def updateSetPoint(self):
        #TODO depend on mode (pc or plc, manual or auto) the coordinate source should change
        #source selection
        if self.objSetpointControlSelected():
            position = self.object.getCurrentPosition()
            ra, dec = position['ra'], position['dec']
            self.setpointCoordinates.setValue(ra, dec)

    def logNow(self):
        print('forse log to write')
        self.logThread.doWork()


    def pcControlSelected(self):
        """  Returns True if status flag read from PLC equals "1" (PC control selected)
             Returns False if status flag read from PLC equals "0" (REMOTE control selected)"""
        return self._resourceKeeper.getPLCManager().isPCControl()

    def remoteControlSelected(self):
        """  Returns True if status flag read from PLC equals "0" (REMOTE control selected)
             Returns False if status flag read from PLC equals "1" (PC control selected)"""
        return not self._resourceKeeper.getPLCManager().isPCControl()

    def objSetpointControlSelected(self):
        """ Returns True if AUTO control selected
            Returns False if MANUAL control selected
        """
        return self.__controlMode

    def selObjSetpointControl(self):
        self.__controlMode = True

    def selManSetpointControl(self):
        self.__controlMode = False

    def scopeCanMove(self):
        canMove = True
        if not self.object.selected():
            canMove = False
        return canMove

    def checkName(self, name):
        star = self.star.getStarByName(name)
        print(star)
        if star:
            return True
        else:
            return False


class SetPoint(object):
    def __init__(self, ra=0, dec=0):
        self.setCoordinates(ra, dec)

    def setCoordinates(self, ra, dec):
        """ can take coordinates in RAD or string (HH:MIN:SEC) """
        ra, dec = astronomy.getCoordinates(ra, dec)
        self.ra, self.dec = astronomy.normCoordinates(ra, dec)

    def getCoordinates(self):
        return self.ra, self.dec

    def getCoordinatesAsString(self):
        return astronomy.rad2str(self.ra, self.dec)


class Focus(object):
    def __init__(self, focus=0.0):
        self.setValue(focus)

    def setValue(self, focus):
        """setValue(float)"""
        self.focus = focus

    def getValue(self):
        return self.focus

    def getAsString(self):
        return str(self.focus)

class Coordinates(object):
    def __init__(self, ra=0, dec=0):
        self.setValue(ra, dec)

    def setValue(self, ra, dec):
        """ can take coordinates in RAD or string (HH:MIN:SEC) """
        ra, dec = astronomy.getCoordinates(ra, dec)
        self.ra, self.dec = astronomy.normCoordinates(ra, dec)

    def getValue(self):
        return self.ra, self.dec

    def getAsString(self):
        return astronomy.rad2str(self.ra, self.dec)







