# -*- coding: utf-8 -*-
from core.Exceptions import ConfigurationException

import re
from time import strftime
import ephem

__author__ = 'kitru'

class Observer(ephem.Observer):
    """ Observer presents observation point on planet surface (telescope position).
    Position and other dislocation data get from configuration dictionary.
    Accurate sidereal time is calculated based on observation position and current local time
    """

    def __init__(self, confDict):
        """ Create observer based on configuration dictionary """
        try:
            latitude = confDict['latitude']
            longitude = confDict['longitude']
            elevation = confDict['elevation']
            temp = confDict['temperature']
            self._createObserver(elevation, latitude, longitude, temp)
        except Exception as ex:
            raise ConfigurationException(ex.args)

    def _createObserver(self, elevation, latitude, longitude, temp):
        self.long = ephem.degrees(str(longitude))
        self.lat = ephem.degrees(str(latitude))
        self.elevation = float(elevation)
        self.temp = float(temp)  #temperature will be corrected by PLC later

    def getCurrentTimes(self):
        """ Calculates current time, julian date and sidereal time
        Return:
            tuple(LT, UTC, JD, LST)
        """
        self.updateToNow()
        localtime = str(strftime("%Z %H:%M:%S")) #System time ZONE HOURS:MIN:SEC
        utc = str(self.date)
        jd = str(ephem.julian_date())
        lst = str(self.sidereal_time()) #observer local sidereal time
        return localtime, utc, jd, lst

    def getLST(self):
        """ Calculates current local sidereal time
        Return:
            LST in radians
        """
        self.updateToNow()
        lst = self.sidereal_time()
        return lst

    def updateToNow(self):
        """ Updates observer date to current date """
        self.date = ephem.now()

    def updateTemp(self, temp):
        self.temp = float(temp) #TODO implement this

    def updatePressure(self, pressure):
        self.pressure = pressure #TODO not very needed, not will be good to add this functionality


class Object(object):
    """ Observation object. Object is observing from observer position. In addition to pyephem.FixedBoby
    Object holds system selected object and able to return current star position in the sky """

    def __init__(self, observer):
        """ By default selected object is not selected """
        self._observer = observer
        self._fixedBody = None
        self._name = ''
        self._id = None

    def init(self, id, name, ra, dec):
        """ Set new observation object
        Attr:
            id - selected star id
            name - name for object
            ra - RA in radians
            de - DEC in radians
        """
        self._id = id
        self._name = name
        self._fixedBody = ephem.FixedBody()
        self._fixedBody._ra = ephem.hours(ra)
        self._fixedBody._dec = ephem.degrees(dec)

    def selected(self):
        """ Checks object selection
        Return:
            selected ? True : False
        """
        if self._fixedBody:
            return True
        else:
            return False

    def getId(self):
        return self._id

    def getName(self):
        return self._name

    def getData(self):
        """ Get common selected object data in HH:MM:SEC format
        Return:
            dict(name, str(ra), str(dec))
        """
        ra, dec, name = '', '', ''
        if self.selected():
            ra, dec = rad2str(self._fixedBody._ra, self._fixedBody._dec)
            name = self._name
        return {'name': name, 'ra': ra, 'dec': dec}

    def getCurrentCoordinates(self):
        """ Returns current object position
        Return:
            ra, dec - radians """
        ra, dec = '', ''
        if self.selected():
            self._observer.updateToNow()
            self._fixedBody.compute(self._observer)
            ra, dec = self._fixedBody.ra, self._fixedBody.dec
        return {'ra': ra, 'dec': dec}

    def getCurrentPosition(self):
        """ Calculates current object position in sky. If object is not selected return empty dictionary
        Return:
            dict(ra,dec,alt,ha,rise,set)
        """
        ra, dec, alt, az, ha, rise, set = '', '', '', ' ', '', '', ''
        if self.selected():
            self._observer.updateToNow()
            self._fixedBody.compute(self._observer)
            ra, dec = rad2str(self._fixedBody.ra, self._fixedBody.dec)
            alt = str(self._fixedBody.alt)
            az = str(self._fixedBody.az)
            rise = self.getRisingTime()
            set = self.getSettingTime()
            ha = str(getHours(self._observer.getLST() - self._fixedBody.ra).norm) # LHA=LST-RA   #add normalization from 0 to 2PI

        return {'ra': ra, 'dec': dec, 'alt': alt, 'az': az, 'ha': ha, 'rise': rise, 'set': set}

    def getRisingTime(self):
        """ Calcutes next rising time for selected object
        Return:
            rise time, if object rises
            never or always, if object always up, down
        """
        try:
            time = ephem.localtime(self._observer.next_rising(self._fixedBody))
            return str(time.strftime('%H:%M:%S'))
        except ephem.NeverUpError:
            return 'never'
        except ephem.AlwaysUpError:
            return 'always'

    def getSettingTime(self):
        """ Calcutes next setting time for selected object
        Return:
            set time, if object sets
            never or always, if object always up, down
        """
        try:
            time = ephem.localtime(self._observer.next_setting(self._fixedBody))
            return str(time.strftime('%H:%M:%S'))
        except ephem.NeverUpError:
            return 'never'
        except ephem.AlwaysUpError:
            return 'always'


class SetPoint(object):
    """ Holding set point position: Ra, Dec, Ha, Focus. This values will be used for sending setpoint to PLC """
    def __init__(self, ra=0, dec=0, focus=None):
        self._ra = float(ra)
        self._dec = float(dec)
        self._focus = float(focus)

    def setPosition(self, ra, dec):
        """ Set setpoint position
        Attr:
            ra, dec - coordinates in RAD or string (HH:MIN:SEC) """
        ra, dec = getCoordinates(str(ra), str(dec))
        self._ra, self._dec = normCoordinates(ra, dec)

    def setFocus(self, focus):
        """ Set setpoint focus
        Attr:
            focus - focus as float """
        if focus:
            self._focus = float(focus)
        else:
            self._focus = None

    def getFocus(self):
        return self._focus

    def getData(self):
        """ Get position as strings """
        data = dict()
        data['ra'], data['dec'] = rad2str(self._ra, self._dec)
        data['focus'] = str(self._focus)
        return data

    def getRawData(self):
        """ get setpoint in radians """
        data = dict()
        data['ra'], data['dec'], data['focus'] = self._ra, self._dec, self._focus
        return data


# Astronomy coordinates, coordinates can be represented as angles in hours or radians(degrees)
# ICRS (International Celestial Reference System) system is used: Right Ascension (RA), declination (DEC)
# For representation follow standard is used: HH:MIN:SEC and DEG:MIN:SEC
RA_HOUR = ephem.twopi / 24
RA_MINUTE = RA_HOUR / 60
RA_SECOND = RA_MINUTE / 60
DEC_DEGREE = ephem.degree
DEC_MINUTE = ephem.arcminute
DEC_SECOND = ephem.arcsecond

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
    return getHours(ra), getDegrees(dec)


def getHours(ra):
    """ Creates right ascension (ra) coordinate as ephem.angle objects
    Attr:
        ra - right ascension in radians (or correct string form (see pyephem,angle))
    Return:
       ephem.hours
    """
    _ra = ra or 0.0
    return ephem.hours(_ra)


def getDegrees(dec):
    """ Creates declination (dec) coordinate as ephem.angle objects
    Attr:
        dec - declination in radiand (or correct string form (see pyephem,angle))
    Return:
       ephem.degrees
    """
    _dec = dec or 0.0
    return ephem.degrees(_dec)


#Check coordinates ranges
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


