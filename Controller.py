import os
from posixpath import join
import logging
import re

from Exceptions import ConfigurationException, InitializationException, ClosingException
from Configs import ProgramConfig
from astronomy import Object
import astronomy

__author__ = 'kitru'

class Controller(object):
    def __init__(self):
        self.__initLogger()
        self.object = None
        self.setPoint = SetPoint()

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

    def starExists(self, name):
        return self.dbManager.starExists(name)

    def getStarByName(self, name):
        """ Take star from database by name
        Star name and position in suitable form for customer
        If star does not exist, return None"""
        star = self.dbManager.getStarByName(name)
        if star:
            return self.parseStar(star)
        else:
            return None

    def saveStar(self, name, ra, dec):
        ra, dec = astronomy.str2rad(str(ra), str(dec))
        self.dbManager.saveStar(name, ra, dec)

    def updateStar(self, name, ra, dec):
        ra, dec = astronomy.str2rad(str(ra), str(dec))
        self.dbManager.updateStar(name, ra, dec)

    def deleteStar(self, star):
        name = star['name']
        self.dbManager.deleteStar(name)

    def getStars(self, name):
        """ Returns list of star objects(name,ra,dec)
        Fetchs all rows with similar star name like name%
        Star name and position in suitable form for customer
        """
        stars = self.dbManager.getStarsByPartName(name)

        resp = []
        for star in stars:
            resp.append(self.parseStar(star))
        return resp

    def parseStar(self, star):
        """ Convert database resultset into dictionary(id,name,ra,dec)
        Attr:
          star - one record fron DB
        """
        name = star[0]
        ra, dec = astronomy.rad2str(star[1], star[2])
        return {'name': name, 'ra': ra, 'dec': dec}

    def setObject(self, name):
        """ Stores new object for observer
        Attr:
            name - star name
        """
        star = self.dbManager.getStarByName(name)
        if star:
            self.object.init(star[0], star[1], star[2])

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
        star = self.dbManager.getStarByName(name)
        print(star)
        if star:
            return True
        else:
            return False

    def checkCoordinates(self, dec, ra):
        return self.checkHours(ra) and self.checkDegrees(dec)

    def checkHours(self, hours):
        try:
            h, m, s = re.split(':', hours)
            return self._checkHour(h) and self._checkMin(m) and self._checkSec(s)
        except Exception:
            return False

    def checkDegrees(self, degrees):
        try:
            deg, m, s = re.split(':', degrees)
            return self._checkDegree(deg) and self._checkMin(m) and self._checkSec(s)
        except Exception:
            return False


    def _checkDegree(self, deg):
        return -90 < int(deg) < 90

    def _checkHour(self, hour):
        return 0 <= int(hour) < 24

    def _checkMin(self, min):
        return 0 <= int(min) < 60

    def _checkSec(self, sec):
        return 0 <= float(sec) < 60


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
        ra, dec = astronomy.getCoordinates(ra, dec)
        self.ra, self.dec = ra, dec #astronomy.normCoord(ra, dec)

    def getCoordinates(self):
        return self.ra, self.dec

    def getCoordinatesAsString(self):
        return astronomy.rad2str(self.ra, self.dec)





