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

    def getLT(self):
        localtime = str(strftime("%Z %H:%M:%S"))
        return localtime

    def getYD(self):
        return ephem.julian_date()

    def getUTC(self):
        self.observer.date = ephem.now()
        return self.observer.date

    def getLST(self):
        return self.observer.sidereal_time()
