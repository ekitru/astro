# -*- coding: utf-8 -*-
import re
from time import strftime
import ephem

__author__ = 'kitru'

class Object(object):
    def __init__(self, observer):
        self.__observer = observer
        self.__fixedBody = None
        self.__name = ''
        self.__id = None

    def init(self, id, name, ra, dec):
        """ Set new observation object
        Attr:
            name - name for object
            ra - RA in radians
            de - DEC in radians
        """
        self.__id = id
        self.__name = name
        self.__fixedBody = ephem.FixedBody()
        self.__fixedBody._ra = ephem.hours(ra)
        self.__fixedBody._dec = ephem.degrees(dec)

    def selected(self):
        if self.__fixedBody:
            return True
        else:
            return False

    def getId(self):
        return self.__id

    def getName(self):
        return self.__name

    def getData(self):
        if self.selected():
            ra, dec = rad2str(self.__fixedBody._ra, self.__fixedBody._dec)
            name = self.__name
        else:
            ra, dec, name, id = '', '', '', ''

        return {'name': name, 'ra': ra, 'dec': dec, 'id': self.__id}

    def getCurrentPosition(self):
        """ return position in radians like {'ra','dec','alt'}. If object is not selected return empty dictionary """
        if self.__fixedBody:
            self.__observer.updateToNow()
            self.__fixedBody.compute(self.__observer.observer)
            ra, dec = rad2str(self.__fixedBody.ra, self.__fixedBody.dec)
            alt = str(self.__fixedBody.alt)
            ha = rad2str((self.__observer.getLST() - self.__fixedBody.ra), 0)
            rise = self.getRisingTime()
            set = self.getSettingTime()
        else:
            ra, dec, alt, ha, rise, set = '', '', '', ' ', '', ''
        return {'ra': ra, 'dec': dec, 'alt': alt, 'ha': ha[0], 'rise': rise, 'set': set}

    def getRisingTime(self):
        try:
            time = self.__observer.observer.next_rising(self.__fixedBody)
            return str(time).split(" ")[1]
        except ephem.NeverUpError:
            return 'never'
        except ephem.AlwaysUpError:
            return 'always'

    def getSettingTime(self):
        try:
            time = self.__observer.observer.next_setting(self.__fixedBody)
            return str(time).split(" ")[1]
        except ephem.NeverUpError:
            return 'never'
        except ephem.AlwaysUpError:
            return 'always'


class Observer(object):
    """ This class imple
    """

    def __init__(self, confDict):
        self.observer = self.getObserver(confDict)

    def getObserver(self, confDict):
        """ Create observer based on configuration  """
        latitude = confDict['latitude']
        longitude = confDict['longitude']
        elevation = confDict['elevation']
        temp = confDict['temperature']
        return self.createObserver(elevation, latitude, longitude, temp)

    def createObserver(self, elevation, latitude, longitude, temp):
        observer = ephem.Observer()
        observer.long = ephem.degrees(str(longitude))
        observer.lat = ephem.degrees(str(latitude))
        observer.elevation = float(elevation)
        observer.temp = float(temp)
        return observer

    def getCurrentTimes(self):
        """ Return current (LT, UTC, JD, LST) """
        self.updateToNow()
        localtime = str(strftime("%Z %H:%M:%S")) #System time ZONE HOURS:MIN:SEC
        utc = str(self.observer.date)
        jd = str(ephem.julian_date())
        lst = str(self.observer.sidereal_time()) #observer local sidereal time
        return localtime, utc, jd, lst

    def getLST(self):
        self.updateToNow()
        lst = self.observer.sidereal_time()
        return lst

    def updateToNow(self):
        self.observer.date = ephem.now()

    def updateTemp(self, temp):
        self.observer.temp = float(temp)

    def updatePressure(self, pressure):
        self.observer.pressure = pressure #TODO not very needed, not will be good to add this functionality


RA_HOUR = ephem.twopi / 24
RA_MINUTE = RA_HOUR / 60
RA_SECOND = RA_MINUTE / 60
DEC_DEGREE = ephem.degree
DEC_MINUTE = ephem.arcminute
DEC_SECOND = ephem.arcsecond

def hours(ra):
    return ephem.hours(ra)


def degrees(dec):
    return ephem.degrees(dec)




# Astronomy coordinates, coordinates can be represented as angles in hours or radians(degrees)
# ICRS (International Celestial Reference System) system is used: Right Ascension (RA), declination (DEC)
# For representation follow standard is used: HH:MIN:SEC and DEG:MIN:SEC

def checkCoordinates(ra, dec):
    """ Checks correct star coordinates in ICRS format:
    right acsension (hours - HH:MIN:SEC) and declination(degrees- DEG:MIN:SEC)
    Attr:
        ra, dec input strings to be checked
    Return:
        both right and in range ? True: False
    """
    return checkHours(ra) and checkDegrees(dec)


def checkHours( hours):
    """ Checks correct hour angle format:  "HOUR:MIN:SEC"
    Attr:
        hours input string to be checked
    Return:
        hours correct? True : False
    """
    try:
        h, m, s = re.split(':', hours)
        return _checkHour(h) and _checkMin(m) and _checkSec(s)
    except Exception:
        return False


def checkDegrees(degrees):
    """ Checks correct degree angle format:  "DEG:MIN:SEC"
    Attr:
        degrees input string to be checked
    Return:
        degrees correct? True: False
    """
    try:
        deg, m, s = re.split(':', degrees)
        return _checkDegree(deg) and _checkMin(m) and _checkSec(s)
    except Exception:
        return False


def _checkDegree(deg):
    return -90 < int(deg) < 90


def _checkHour(hour):
    return 0 <= int(hour) < 24


def _checkMin(min):
    return 0 <= int(min) < 60


def _checkSec(sec):
    return 0 <= float(sec) < 60


# Convertion coordinates:  (RAD - STR) and (STR - RAD)
def rad2str(ra, dec):
    """ Convert right ascension (ra) and declination (dec) coordination to string form
    Attr:
        ra - right ascension in radians (or correct string form (see pyephem,angle))
        dec - declination in radiand (or correct string form (see pyephem,angle))
    Return:
       tuple(string, string)
    """
    _ra, _dec = getCoordinates(ra, dec)
    return str(_ra), str(_dec)


def str2rad(ra, dec):
    """ Convert right ascension (ra) and declination (dec) coordination to radians
    Attr:
        ra - right ascension in radians (or correct string form (see pyephem,angle))
        dec - declination in radiand (or correct string form (see pyephem,angle))
    Return:
       tuple(float, float)
    """
    _ra, _dec = getCoordinates(ra, dec)
    return _ra.real, _dec.real


def getCoordinates(ra, dec):
    """ Creates right ascension (ra) and declination (dec) coordinates as ephem.angle objects
    Attr:
        ra - right ascension in radians (or correct string form (see pyephem,angle))
        dec - declination in radiand (or correct string form (see pyephem,angle))
    Return:
       tuple(ephem.hours, ephem.degrees)
    """
    _ra = ra or 0.0
    _dec = dec or 0.0
    return ephem.hours(_ra), ephem.degrees(_dec)


#Coordinatea normalization.
#According to ICSR standard right ascension(ra) and declination(dec) should be in ranges:
#       ra - right ascension [0,2π)
#       dec - declination (-π/2,π/2]

def normCoordinates(ra, dec):
    """ Right ascension and declination coordinates normalization
    Attr:
        ra - right ascension [0,2π)
        dec - declination (-π/2,π/2]
    Return:
        tuple(ra, dec) normalized
    """
    return normRa(ra), normDec(dec)


def normRa(ra):
    """ Right ascension normalization
    Attr:
        ra - right ascension angle (ephem.angle)
    Return:
        right ascension in range [0,2π)
    """
    return ra.norm  # normalization to the interval [0, 2π)


def normDec(dec):
    """ Declination normalization
    Attr:
        dec - declination angle (ephem.angle)
    Return:
        declination in range (-π/2,π/2]
    """
    doubleDec = ephem.degrees(2 * dec)
    zDec = doubleDec.znorm  # normalization to the interval (-π, π]
    return ephem.degrees(zDec / 2)


