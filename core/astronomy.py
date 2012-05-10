# -*- coding: utf-8 -*-
from math import sin, cos
from numpy.lib.scimath import arcsin
from core.Exceptions import ConfigurationException

import re
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
            pressure = confDict['pressure']
            horizon = confDict['horizon']
            self._createObserver(elevation, latitude, longitude, horizon, temp, pressure)
        except Exception as ex:
            raise ConfigurationException(ex.args)

    def _createObserver(self, elevation, latitude, longitude, horizon, temp, pressure):
        self.long = ephem.degrees(str(longitude))
        self.lat = ephem.degrees(str(latitude))
        self.elevation = float(elevation)
        self.horizon = str(horizon)
        self.temp = float(temp)  #temperature will be corrected by PLC later
        self.pressure = float(pressure)

    def getUTC(self):
        return self.date

    def getLST(self):
        """ Calculates current local sidereal time """
        self._now()
        return self.sidereal_time()

    def getJulianDate(self):
        """ Calculates current Julian date """
        return ephem.julian_date()

    def _now(self):
        """ Updates observer date to current date """
        self.date = ephem.now()

#    def updateTemp(self, temp):
#        self.temp = float(temp) #TODO not very needed, not will be good to add this functionality
#
#    def updatePressure(self, pressure):
#        self.pressure = pressure #TODO not very needed, not will be good to add this functionality


class Object(object):
    """ Observation object. Object is observing from observer position. In addition to pyephem.FixedBoby
    Object holds system selected object and able to return current star position in the sky """

    def __init__(self, observer):
        """ By default selected object is not selected """
        self._observer = observer

        self._fixedBody = None

        self._name = ' '
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

    def getOriginalPosition(self):
        """ Get objects original position for J2000 """
        return self._fixedBody._ra, self._fixedBody._dec

    def _now(self):
        """ Update obsever to now and recalculate object position """
        self._observer._now()
        self._fixedBody.compute(self._observer)

    def recalculateEquatorialPosition(self):
        Lat = self._observer.lat
        Alt = self._fixedBody.alt
        Az = self._fixedBody.az
        Ra = self._fixedBody.ra
#        print("ALT-AZ", self._fixedBody.alt, self._fixedBody.az, "LST",self._observer.getLST())
        Dec = arcsin(sin(Alt) * sin(Lat) + cos(Alt) * cos(Lat) * cos(Az))
#        HA = arccos((sin(Alt) - sin(Dec)*sin(Lat)) / (cos(Dec)*cos(Lat)))
#        HA2 = arcsin(-sin(Az)*cos(Alt)/cos(Dec))
#        Ra = self._observer.getLST() -HA
#        print('Calculated','HA',getHours(HA),'RA-DEC',getCoordinates(Ra,Dec))
#        print('Original', 'HA', self.getCurrentHA(), 'RA-DEC',self._fixedBody.ra, self._fixedBody.dec)
#        getHours(self._observer.long)
        return getCoordinates(Ra,Dec)

    def printInfo(self):
        self._now()
#        print("ALT-AZ", self._fixedBody.alt, self._fixedBody.az)
#        print("RA-DEC OF", self._observer.radec_of(az=self._fixedBody.az, alt=self._fixedBody.alt))
#        print('Object position: ', self._fixedBody._ra, self._fixedBody._dec)
#        print('Astrometric Geocentric Position: ', self._fixedBody.a_ra, self._fixedBody.a_dec)
#        print('Apparent Geocentric Position: ', self._fixedBody.g_ra, self._fixedBody.g_dec)
        print('Apparent Topocentric Position: ', self._fixedBody.ra, self._fixedBody.dec)
        print('Recalculated position:', self.recalculateEquatorialPosition())

    def getEquatorialPosition(self):
        """ position for now """
        self._now()
#        print("TEST")
#        print("Zero pressure")
#        self._observer.pressure=0
#        self.printInfo()
#        print("Pressure 1005mm")
#        self._observer.pressure=1005
#        self.printInfo()
#        return self._fixedBody.ra, self._fixedBody.dec
        self.printInfo()
        return self.recalculateEquatorialPosition()

    def getHorizontalPosition(self):
        """ position for now """
        self._now()
        return self._fixedBody.alt, self._fixedBody.az

    def getHorizon(self):
        return  self._observer.horizon

    def getCurrentHA(self):
        """ Calculates current object HA for observer. """
        self._now()
        return getHours(self._observer.getLST() - self._fixedBody.ra).norm # added normalization from [0, 2π)

    def getRisingTime(self):
        """ Calcutes next rising time for selected object
        Return:
            rise time or None """
        try:
            return ephem.localtime(self._observer.next_rising(self._fixedBody))
        except ephem.CircumpolarError:
            return

    def getSettingTime(self):
        """ Calcutes next setting time for selected object
        Return:
            rise time or None """
        try:
            return ephem.localtime(self._observer.next_setting(self._fixedBody))
        except ephem.CircumpolarError:
            return

    def getExpositionTime(self):
        """ Calculate exposition time """
        try:
            return ephem.localtime(self._observer.next_setting(self._fixedBody)) - ephem.localtime(ephem.now())
        except ephem.CircumpolarError:
            return
        except Exception:
            return


class SetPoint(object):
    """ Holding set point position: Ra, Dec. This values will be used for sending setpoint to PLC """

    def __init__(self, ra=0, dec=0):
        self._ra = float(ra)
        self._dec = float(dec)

    def setPosition(self, ra, dec):
        """ Set setpoint position
        Attr:
            ra, dec - coordinates in RAD or string (HH:MIN:SEC) """
        ra, dec = getCoordinates(str(ra), str(dec))
        self._ra, self._dec = normCoordinates(ra, dec)


    def getData(self):
        """ Get position as strings """
        data = dict()
        data['ra'], data['dec'] = rad2str(self._ra, self._dec)
        return data

    def getRawData(self):
        """ get setpoint in radians """
        data = dict()
        data['ra'], data['dec'] = self._ra.real, self._dec.real
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


