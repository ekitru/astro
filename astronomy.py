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
        except ephem.NeverUpError as error:
            return 'never'
        except ephem.AlwaysUpError as error:
            return 'always'

    def getSettingTime(self):
        try:
            time = self.observer.observer.next_setting(self.fixedBody)
            return str(time).split(" ")[1]
        except ephem.NeverUpError as error:
            return 'never'
        except ephem.AlwaysUpError as error:
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
        pass  #TODO not very needed, not will be good to add this functionality


def rad2str(ra, dec):
    """ Convert (ra,dec) in radians to more readable form """
    ra, dec = getCoordinates(ra, dec)
    return str(ra), str(dec)


def str2rad(ra, dec):
    """ Convert (ra,dec) strings to radians  """
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