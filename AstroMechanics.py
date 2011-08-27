from time import strftime
import ephem

__author__ = 'kitru'

class AstroMechanics(object):
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

    def getStarPosition(self, ra, dec):
        self.updateObserverTime()

        star = ephem.FixedBody()
        star._ra = ephem.hours(ra)
        star._dec = ephem.degrees(dec)
        star.compute(self.observer)
        return {'ra': star.ra, 'dec': star.dec, 'alt':star.alt}

    def getCurrentTimeDate(self):
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

    def convCoordRad2Str(self, ra, dec):
        """ Convert (ra,dec) in radians to more readable form
        Attr:
          ra - right ascension in radians
          dec - declination in radians
        """
        ra, dec = self.getCoordinates(ra, dec)
        return str(ra), str(dec)

    def convCoordStr2Rad(self, ra, dec):
        ra, dec = self.getCoordinates(ra, dec)
        return ra.real, dec.real

    def getCoordinates(self, ra, dec):
        """ Return angles RA,DEC (topocentric position)
        Attr:
           ra - radians or string (hour:min:sec)
           dec - radians or string (deg:min:sec)
        return:
           tuple(ephem,hours, ephem.degrees)
        """
        ra = ephem.hours(ra)
        dec = ephem.degrees(dec)
        return ra, dec