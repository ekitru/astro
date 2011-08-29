from time import strftime
import ephem

__author__ = 'kitru'

class Object(object):
    def __init__(self, observer):
        self.observer = observer
        self.object = None
        self.objectName = ''

    def setObject(self, name, ra, dec):
        """ Set new observation object
        Attr:
            name - name for object
            ra - RA in radians
            de - DEC in radians
        """
        self.objectName = name
        self.object = ephem.FixedBody()
        self.object._ra = ephem.hours(ra)
        self.object._dec = ephem.degrees(dec)

    def getObject(self):
        """ Object{'name','ra','dec'} or None if not """
        if self.object:
            return {'name': self.objectName, 'ra': self.object._ra, 'dec': self.object._dec}
        else:
            return None

    def getObjectPositionNow(self):
        """ return position in radians like {'ra','dec','alt'}. If object is not degined return empty dictionary """
        if self.object:
            self.observer.updateObserverTime()
            self.object.compute(self.observer.observer)
            ra, dec = rad2str(self.object.ra, self.object.dec)
            alt = str(self.object.alt)
        else:
            ra,dec,alt = '','',''
        return {'ra': ra, 'dec': dec, 'alt': alt}


class Observer(object):
    def __init__(self, confDict):
        self.observer = self.getObserver(confDict)

    def getObserver(self, confDict):
        """ Create observer based on configuration  """
        latitude = confDict['latitude']
        longitude = confDict['longitude']
        elevation = confDict['elevation']
        temp = confDict['temperature']
        #preassure can be also corrected

        observer = ephem.Observer()
        observer.long = ephem.degrees(str(longitude))
        observer.lat = ephem.degrees(str(latitude))
        observer.elevation = float(elevation)
        observer.temp = float(temp)
        return observer

    def getTimeDateNow(self):
        """ return tuple of LT, UTC, JD, LST """
        self.updateObserverTime()
        utc = str(self.observer.date)
        lst = str(self.observer.sidereal_time())
        localtime = str(strftime("%Z %H:%M:%S"))
        jd = str(ephem.julian_date())
        return localtime, utc, jd, lst

    def updateObserverTime(self):
        self.observer.date = ephem.now()

    def updateObserverTemp(self, temp):
        self.observer.temp = float(temp)

    def updateObserverPressure(self, pressure):
        pass  #TODO neet very needed, not will be good to add this functionality


def rad2str(ra, dec):
    """ Convert (ra,dec) in radians to more readable form
    Attr:
      ra - right ascension in radians
      dec - declination in radians
    """
    ra, dec = getCoordinates(ra, dec)
    return str(ra), str(dec)

def str2rad(ra, dec):
    ra, dec = getCoordinates(ra, dec)
    return ra.real, dec.real

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