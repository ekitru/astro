import os
from posixpath import join
import logging
import re

from Exceptions import ConfigurationException, InitializationException, ClosingException
from Configs import ProgramConfig

__author__ = 'kitru'

class Controller(object):
    def __init__(self):
        self.__initLogger()
        self.object = {'name': '', 'ra': '', 'dec': ''}



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
        Opens DB connection and connection with PLCm also reads translation codes
        """
        try:
            logging.info('======= Program initialization =======')
            config = ProgramConfig('default.conf')
            self.mechanics = config.openAstroMechanics()
            self.dbManager = config.getDbManager()
            self.commManager = config.getPLCManager()
            self.trans = config.getTranslationConf()
        except ConfigurationException as ce:
            logging.error('Erron during initialization occure: ' + ce.__str__())
            raise InitializationException(ce)

    def freeResources(self):
        try:
            logging.info('======= Free all resources: DB, MODBUS =======')
            self.dbManager.close()
            self.commManager.close()
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
        ra, dec = self.mechanics.convCoordStr2Rad(str(ra), str(dec))
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
        ra, dec = self.mechanics.convCoordRad2Str(star[1], star[2])
        return {'name': name, 'ra': ra, 'dec': dec}

    def setObject(self, name):
        """ Stores new object for observer
        Attr:
            name - star name
        """
        star = self.dbManager.getStarByName(name)
        self.object = {'name': star[0], 'ra': star[1], 'dec': star[2]}

    def getObject(self):
        name = self.object['name']
        ra, dec = self.mechanics.convCoordRad2Str(self.object['ra'], self.object['dec'])
        return {'name': name, 'ra': ra, 'dec': dec}

    def getCurrentObjectPosition(self):
        if self.object['name']:
            position = self.mechanics.getStarPosition(self.object['ra'], self.object['dec'])
            ra, dec = self.mechanics.convCoordRad2Str(position['ra'], position['dec'])
            alt = str(position['alt'])
        else:
            ra,dec,alt ='','',''
        return {'ra': ra, 'dec': dec, 'alt': alt}

    def getTelescopePosition(self):
        """ Return current and aim telescope position
        {'current':(str,str) ,'end':(str,str)}
        """
        telescopePosition = self.commManager.getPosition()
        position = {'cur': self.mechanics.convCoordRad2Str(*telescopePosition[0]), 'end': self.mechanics.convCoordRad2Str(*telescopePosition[1])}
        return position


    def getTelescopeFocus(self):
        """ Return current and aim telescope focus
        {'current':str() ,'end':str()}
        """
        telescopeFocus = self.commManager.getFocus()
        focus = {'cur': str(telescopeFocus[0]), 'end': str(telescopeFocus[1])}
        return focus

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