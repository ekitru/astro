import re
from time import strftime
import ephem

__author__ = 'kitru'

class AstroMechanics(object):
    def __init__(self, confDict):
        self.observer = self.getObserver(confDict)

    def getObserver(self, confDict):
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

    def updateObserverTime(self):
        self.observer.date = ephem.now()

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
