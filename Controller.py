import os
from posixpath import join
import logging
from db import  Message
from db import Star

from Exceptions import ConfigurationException, InitializationException, ClosingException
from Configs import ProgramConfig
from astronomy import Object
import astronomy

__author__ = 'kitru'

class Controller(object):
    def __init__(self):
        self.__initLogger()
        self.object = None
        self.setpoint = SetPoint() #In auto mode it is sent to plc
        self.focus = Focus()    #In Auto mode it is sent to plc
        self.controlMode = True

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
            self.__dbManager = config.getDbManager()
            self.star = Star(self.__dbManager)
            self.message = Message(self.__dbManager)
            self.PLCManager = config.getPLCManager()
            self.trans = config.getTranslation()
        except ConfigurationException as ce:
            logging.error('Erron during initialization occure: ' + ce.__str__())
            raise InitializationException(ce)

    def freeResources(self):
        try:
            logging.info('======= Free all resources: DB, MODBUS =======')
            del self.star
            del self.message
            del self.__dbManager

            self.PLCManager.close()
        except Exception as e:
            raise ClosingException(e)

    def setObject(self, name):
        """ Stores new object for observer
        Attr:
            name - star name
        """
        print(name)
        star = self.star.getStarByName(name)
        print(star)
        if star:
            self.object.init(star['name'], star['ra'], star['dec'])

    def getObject(self):
        return self.object

    def updateSetPoint(self):
        #TODO depend on mode (pc or plc, manual or auto) the coordinate source should change
        #source selection
        position = self.object.getCurrentPosition()
        ra, dec = position['ra'], position['dec']
        self.setpoint.setCoordinates(ra, dec)

    def getSetpointCoordinates(self):
        """ Get setpoint coordinates """
        return self.setpoint.getCoordinatesAsString()


    def getTelescopePosition(self):
        """ Return current and target telescope position
        {'cur':(str,str) ,'end':(str,str)}
        """
        telescopePosition = self.PLCManager.getPosition()
        position = {'cur': astronomy.rad2str(*telescopePosition[0]), 'end': astronomy.rad2str(*telescopePosition[1])}
        return position

    def getSetpointFocus(self):
        """ Get setpoint focus"""
        return self.focus.getFocusAsString()

    def getTelescopeFocus(self):
        """ Return current and target telescope focus
        {'current':str() ,'end':str()}
        """
        telescopeFocus = self.PLCManager.getFocus()
        focus = {'cur': str(telescopeFocus[0]), 'end': str(telescopeFocus[1])}
        return focus


    def pcControlSelected(self):
        """  Returns True if status flag read from PLC equals "1" (PC control selected)
             Returns False if status flag read from PLC equals "0" (REMOTE control selected)"""
        return self.PLCManager.isPCControl()

    def autoControlSelected(self):
        """ Returns True if AUTO control selected
            Returns False if MANUAL control selected
        """
        return self.controlMode

    def selectAutoControl(self):
        self.controlMode = True

    def selectManualControl(self):
        self.controlMode = False

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
        self.setFocus(focus)

    def setFocus(self, focus):
        """setFocus(float)"""
        self.focus = focus

    def getFocus(self):
        return self.focus

    def getFocusAsString(self):
        return str(self.focus)










