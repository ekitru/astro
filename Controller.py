from _mysql import connection
import os
from posixpath import join
import logging
import re
from DbManager import StarManager

from Exceptions import ConfigurationException, InitializationException, ClosingException
from Configs import ProgramConfig
from astronomy import Object
import astronomy

__author__ = 'kitru'

class Controller(object):
    def __init__(self):
        self.__initLogger()
        self.object = None
        self.setPoint = SetPoint() #In auto mode sends to plc

    def __initLogger(self):
        if not os.path.exists('logs'):
            os.makedirs('logs', mode=0711)
        logging.basicConfig(level=logging.DEBUG,
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
            self.dbManager = config.getDbManager()
            self.starManager = StarManager(self.dbManager.getCursor())
            self.PLCManager = config.getPLCManager()
            self.trans = config.getTranslation()
            self.controlMode = False
            self.setpointSpeed = 1
        except ConfigurationException as ce:
            logging.error('Erron during initialization occure: ' + ce.__str__())
            raise InitializationException(ce)

    def freeResources(self):
        try:
            logging.info('======= Free all resources: DB, MODBUS =======')
            self.dbManager.close()
            self.PLCManager.close()
        except Exception as e:
            raise ClosingException(e)

    def setObject(self, name):
        """ Stores new object for observer
        Attr:
            name - star name
        """
        print(name)
        star = self.starManager.getStarByName(name)
        print(star)
        if star:
            self.object.init(star['name'], star['ra'], star['dec'])

    def getObject(self):
        self.updateSetPoint() #TODO temporaly place for continues update
        return self.object

    def updateSetPoint(self):
        #TODO depend on mode (pc or plc, manual or auto) the coordinate source should change
        #source selection
        position = self.object.getCurrentPosition()
        ra, dec = position['ra'], position['dec']
        self.setPoint.setCoordinated(ra, dec)

    def getSetPointCoordinates(self):
        """ Get current Set point coordinates """
        return self.setPoint.getCoordinatesAsString()



    def getTelescopePosition(self):
        """ Return current and target telescope position
        {'cur':(str,str) ,'end':(str,str)}
        """
        telescopePosition = self.PLCManager.getPosition()
        position = {'cur': astronomy.rad2str(*telescopePosition[0]), 'end': astronomy.rad2str(*telescopePosition[1])}
        return position

    def getTelescopePositionInRad(self):
        """ Return current and target telescope position
        {'cur':(rad,rad) ,'end':(rad,rad)}
        """
        telescopePosition = self.PLCManager.getPosition()
        position = {'cur': telescopePosition[0], 'end': telescopePosition[1]}
        return position

    def setTelescopePosition(self,(ra,dec)):
        """Sets telescope position in radians
        (float, float)
        """
        self.PLCManager.setPosition((ra,dec))

    def getTelescopeFocus(self):
        """ Return current and target telescope focus
        {'current':str() ,'end':str()}
        """
        telescopeFocus = self.PLCManager.getFocus()
        focus = {'cur': str(telescopeFocus[0]), 'end': str(telescopeFocus[1])}
        return focus

    def getTelescopeFocusAsFloat(self):
        """ Return current and target telescope focus
        {'current':float ,'end':float}
        """
        telescopeFocus = self.PLCManager.getFocus()
        focus = {'cur': telescopeFocus[0], 'end': telescopeFocus[1]}
        return focus

    def setTelescopeFocus(self, focus):
        """Sets the telescope focus.
        (float)
        """
        self.PLCManager.setFocus(focus)

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
        star = self.starManager.getStarByName(name)
        print(star)
        if star:
            return True
        else:
            return False




    def incRAPosition(self, ra, spSpeed, step):
        if spSpeed == 1:
            ra += astronomy.getHour()/60/60*step
        if spSpeed == 2:
            ra += astronomy.getHour()/60*step
        if spSpeed == 3:
            ra += astronomy.getHour()*step
            if ra > astronomy.getHour()*24:
                ra -= astronomy.getHour()*step
        if ra >= astronomy.RA_235959():
            ra = astronomy.RA_235959()
        if ra < 0.0:
            ra = 0.0
        return ra

    def incDECPosition(self, dec, spSpeed, step):
        if spSpeed == 1:
            dec += astronomy.getDegree()/60/60*step
        if spSpeed == 2:
            dec += astronomy.getDegree()/60*step
        if spSpeed == 3:
            dec += astronomy.getDegree()*step
        if dec > astronomy.getDegree()*90:
            dec = astronomy.getDegree()*90
        if dec < -astronomy.getDegree()*90:
            dec = -astronomy.getDegree()*90
        return dec

    def incFocus(self, foc, step):
        min = 0.0
        max = 2.0
        f = foc + step
        if f < min:
            f = 0.0
        elif f > max:
            f = max
        return f

    def getSetpointSpeed(self):
        return self.setpointSpeed

    def setSetpointSpeed(self, spSpeed):
        self.setpointSpeed = spSpeed



class SetPoint(object):
    def __init__(self, ra=0, dec=0):
        self.setCoordinated(ra, dec)

    def setCoordinated(self, ra, dec):
        """ can take coordinates in RAD or string (HH:MIN:SEC) """
        ra, dec = astronomy.getCoordinates(ra, dec)
        self.ra, self.dec = astronomy.normCoordinates(ra, dec)

    def getCoordinates(self):
        return self.ra, self.dec

    def getCoordinatesAsString(self):
        return astronomy.rad2str(self.ra, self.dec)










