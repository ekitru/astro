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

    def isStarExist(self, name):
        if self.getStarByName(name):
            return True
        else:
            return False

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
        return self.object

    def getTelescopePosition(self):
        """ Return current and aim telescope position
        {'cur':(str,str) ,'end':(str,str)}
        """
        telescopePosition = self.PLCManager.getPosition()
        position = {'cur': astronomy.rad2str(*telescopePosition[0]), 'end': astronomy.rad2str(*telescopePosition[1])}
        return position


    def getTelescopeFocus(self):
        """ Return current and aim telescope focus
        {'current':str() ,'end':str()}
        """
        telescopeFocus = self.PLCManager.getFocus()
        focus = {'cur': str(telescopeFocus[0]), 'end': str(telescopeFocus[1])}
        return focus

    def scopeCanMove(self):
        canMove = True
        if not self.object.selected():
            canMove = False
        return canMove

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