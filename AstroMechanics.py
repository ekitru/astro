from time import strftime
import ephem

__author__ = 'kitru'

class AstroMechanics(object):
    def __init__(self, confDict):
        self.observer = self.getObserver(confDict)
        self.objectName = ""
        self.object = None

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
        if self.object:
            return {'name':self.objectName, 'ra': self.object._ra, 'dec': self.object._dec}
        else:
            return None

    def getObjectPositionNow(self):
        """ return position in radians like {'name','ra','dec','alt'}  """
        if self.object:
            self.updateObserverTime()
            self.object.compute(self.observer)
            return {'name':self.objectName, 'ra': self.object.ra, 'dec': self.object.dec, 'alt':self.object.alt}
        else:
            return {'name':'', 'ra': '', 'dec': '', 'alt':''}

    def getTimeDateNow(self):
        """ return tuple of LT, UTC, JD, LST """
        self.updateObserverTime()
        utc = str(self.observer.date)
        lst = str(self.observer.sidereal_time())
        localtime = str(strftime("%Z %H:%M:%S"))
        jd = str(ephem.julian_date())
        return localtime, utc, jd, lst

    def getLT(self):
        localtime = str(strftime("%Z %H:%M:%S"))
        return localtime

    def getYD(self):
        return ephem.julian_date()

    def getUTC(self):
        self.updateObserverTime()
        return self.observer.date

    def getLST(self):
        return self.observer.sidereal_time()

    def updateObserverTime(self):
        self.observer.date = ephem.now()

    def rad2str(self, ra, dec):
        """ Convert (ra,dec) in radians to more readable form
        Attr:
          ra - right ascension in radians
          dec - declination in radians
        """
        ra, dec = self.getCoordinates(ra, dec)
        return str(ra), str(dec)

    def str2rad(self, ra, dec):
        ra, dec = self.getCoordinates(ra, dec)
        return ra.real, dec.real

    def getCoordinates(self, ra, dec):
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