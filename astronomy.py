import re
from time import strftime
import ephem

__author__ = 'kitru'

class Object(object):
    def __init__(self, observer):
        self.observer = observer
        self.fixedBody = None
        self.fixedBodyName = ''

    def init(self, name, ra, dec):
        """ Set new observation object
        Attr:
            name - name for object
            ra - RA in radians
            de - DEC in radians
        """
        self.fixedBodyName = name
        self.fixedBody = ephem.FixedBody()
        self.fixedBody._ra = ephem.hours(ra)
        self.fixedBody._dec = ephem.degrees(dec)

    def selected(self):
        if self.fixedBody:
            return True
        else:
            return False

    def getData(self):
        if self.selected():
            ra, dec = rad2str(self.fixedBody._ra, self.fixedBody._dec)
            name = self.fixedBodyName
        else:
            ra, dec, name = '', '', ''

        return {'name': name, 'ra': ra, 'dec': dec}

    def getCurrentPosition(self):
        """ return position in radians like {'ra','dec','alt'}. If object is not selected return empty dictionary """
        if self.fixedBody:
            self.observer.updateToNow()
            self.fixedBody.compute(self.observer.observer)
            ra, dec = rad2str(self.fixedBody.ra, self.fixedBody.dec)
            alt = str(self.fixedBody.alt)
            ha = rad2str((self.observer.getLST()-self.fixedBody.ra), 0)
            rise = self.getRisingTime()
            set = self.getSettingTime()
        else:
            ra, dec, alt, ha, rise, set  = '', '', '', ' ', '', ''
        return {'ra': ra, 'dec': dec, 'alt': alt, 'ha':ha[0], 'rise':rise, 'set':set}

    def getRisingTime(self):
        try:
            time = self.observer.observer.next_rising(self.fixedBody)
            return str(time).split(" ")[1]
        except ephem.NeverUpError:
            return 'never'
        except ephem.AlwaysUpError:
            return 'always'

    def getSettingTime(self):
        try:
            time = self.observer.observer.next_setting(self.fixedBody)
            return str(time).split(" ")[1]
        except ephem.NeverUpError:
            return 'never'
        except ephem.AlwaysUpError:
            return 'always'


class Observer(object):
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


RA_HOUR = ephem.twopi/24
RA_MINUTE = RA_HOUR/60
RA_SECOND = RA_MINUTE/60
DEC_DEGREE = ephem.degree
DEC_MINUTE = ephem.arcminute
DEC_SECOND = ephem.arcsecond

def hours(ra):
    return ephem.hours(ra)

def degrees(dec):
    return ephem.degrees(dec)

# working with coordinates
def getCoordinates(ra, dec):
    """ Return angles RA,DEC (topocentric position)
    Attr:
       ra - radians or string (hour:min:sec)
       dec - radians or string (deg:min:sec)
    return:
       tuple(ephem.hours, ephem.degrees)
    """
    ra = ephem.hours(ra)
    dec = ephem.degrees(dec)
    return ra, dec

def rad2str(ra, dec):
    """ Convert (ra,dec) in radians to more readable form """
    ra, dec = getCoordinates(ra, dec)
    return str(ra), str(dec)

def str2rad(ra, dec):
    """ Convert (ra,dec) strings to radians  """
    ra, dec = getCoordinates(ra, dec)
    return ra.real, dec.real

def normCoordinates(ra, dec):
    return normRa(ra), normDec(dec)

def normRa(ra):
    return ra.norm

def normDec(dec):
    dec = ephem.degrees(2*dec)
    dec =  dec.znorm
    return ephem.degrees(dec/2)

def checkCoordinates(dec, ra):
        return checkHours(ra) and checkDegrees(dec)

def checkHours( hours):
    try:
        h, m, s = re.split(':', hours)
        return _checkHour(h) and _checkMin(m) and _checkSec(s)
    except Exception:
        return False

def checkDegrees(degrees):
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


