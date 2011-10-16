import os
from posixpath import join
import logging
from core.Resources import Resources

from Exceptions import ConfigurationException, InitializationException, ClosingException
import astronomy
from LogThread import LogThread

__author__ = 'kitru'

class Controller(object):
    _controlMode = True

    def __init__(self):
        self.__initLogger()
        self.currentCoordinates = Coordinates()  #read from PLC
        self.setpointCoordinates = Coordinates() #sent to PLC
        self.currentFocus = Focus()     #read from PLC
        self.setpointFocus = Focus()    #sent to PLC
        self.manPosition = None
        self.manFocus = None

    def __initLogger(self):
        logPath = join('resources', 'logs')
        if not os.path.exists(logPath):
            os.makedirs(logPath, mode=0711)
        logging.basicConfig(level=logging.NOTSET,
                            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                            datefmt='%m-%d %H:%M',
                            filename=join(logPath, 'common.log'),
                            filemode='w')

    def initialization(self, resources):
        """ Initialization for all components
        Opens DB connection and connection with PLCm also reads translation codes """
        try:
            logging.info('======= Program initialization =======')
            self._resourceKeeper = resources
            self._logThread = LogThread(self)
#        except ConfigurationException as ce:
#            raise InitializationException(ce)
#        except Exception as e:
#            raise InitializationException(e)
        except ImportError:
            pass


    def freeResources(self):
        try:
            logging.info('======= Free all resources: DB, MODBUS =======')
            # close database connections
            self._logThread.stop()
            del self._resourceKeeper
        except Exception as e:
            raise ClosingException(e)

    def getConfig(self):
        """ needed for settings dialog """
        return self.getResourceKeeper().getConfig()

    def getResourceKeeper(self):
        return self._resourceKeeper

    def getObserver(self):
        return self.getResourceKeeper().getObserver()

    def setObject(self, name):
        """ Stores new object for observer
        Attr:
            name - star name
        """
        self.getResourceKeeper().setObject(name)

    def getObject(self):
        return self.getResourceKeeper().getObject()

    def updateSetPoint(self):
        #TODO depend on mode (pc or plc, manual or auto) the coordinate source should change
        #source selection
        if self.objSetpointControlSelected():
            position = self.getObject().getCurrentPosition()
            ra, dec = position['ra'], position['dec']
            self.setpointCoordinates.setValue(ra, dec)

    def logNow(self):
        print('forse log to write')
        self._logThread.force()


    def pcControlSelected(self):
        """  Returns True if status flag read from PLC equals "1" (PC control selected)
             Returns False if status flag read from PLC equals "0" (REMOTE control selected)"""
        return self._resourceKeeper.getPLCManager().isPCControl()

    def remoteControlSelected(self):
        """  Returns True if status flag read from PLC equals "0" (REMOTE control selected)
             Returns False if status flag read from PLC equals "1" (PC control selected)"""
        return not self._resourceKeeper.getPLCManager().isPCControl()

    def objSetpointControlSelected(self):
        """ Returns True if AUTO control selected
            Returns False if MANUAL control selected
        """
        return self._controlMode

    def selObjSetpointControl(self):
        self._controlMode = True

    def selManSetpointControl(self):
        self._controlMode = False

    def scopeCanMove(self):
        canMove = True
        if not self.getObject().selected():
            canMove = False
        return canMove


class SetPoint(object):
    def __init__(self, ra=0, dec=0):
        self.setCoordinates(ra, dec)

    def setCoordinates(self, ra, dec):
        """ can take coordinates in RAD or string (HH:MIN:SEC) """
        ra, dec = astronomy.getCoordinates(ra, dec)
        self.ra, self.dec = astronomy.normCoordinates(ra, dec)

    def getCoordinates(self):
        return self.ra, self.dec

    def getCoordinatesAsString(self):
        return astronomy.rad2str(self.ra, self.dec)


class Focus(object):
    def __init__(self, focus=0.0):
        self.setValue(focus)

    def setValue(self, focus):
        """setValue(float)"""
        self.focus = focus

    def getValue(self):
        return self.focus

    def getAsString(self):
        return str(self.focus)


class Coordinates(object):
    def __init__(self, ra=0, dec=0):
        self.setValue(ra, dec)

    def setValue(self, ra, dec):
        """ can take coordinates in RAD or string (HH:MIN:SEC) """
        ra, dec = astronomy.getCoordinates(ra, dec)
        self.ra, self.dec = astronomy.normCoordinates(ra, dec)

    def getValue(self):
        return self.ra, self.dec

    def getAsString(self):
        return astronomy.rad2str(self.ra, self.dec)







