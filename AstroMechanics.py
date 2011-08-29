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
        """ Object{'name','ra','dec'} or None if not """
        if self.object:
            return {'name': self.objectName, 'ra': self.object._ra, 'dec': self.object._dec}
        else:
            return None

    def getObjectPositionNow(self):
        """ return position in radians like {'ra','dec','alt'}. If object is not degined return empty dictionary """
        if self.object:
            self.updateObserverTime()
            self.object.compute(self.observer)
            ra, dec = self.rad2str(self.object.ra, self.object.dec)
            alt = str(self.object.alt)
        else:
            ra,dec,alt = '','',''
        return {'ra': ra, 'dec': dec, 'alt': alt}


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