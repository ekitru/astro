import os
from posixpath import join
import logging
from core.Resources import Resources

from Exceptions import ConfigurationException, InitializationException, ClosingException
import astronomy
from LogThread import LogThread
from core.logger import getLogPath

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
        logPath = getLogPath()
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
            self._resources = resources
            self._logThread = LogThread(resources)
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
            del self._resources
        except Exception as e:
            raise ClosingException(e)

    def getResourceKeeper(self):
        return self._resources

    def updateSetPoint(self):
        #TODO depend on mode (pc or plc, manual or auto) the coordinate source should change
        #source selection
        if self.objSetpointControlSelected():
            position = self._resources.getObject().getCurrentPosition()
            ra, dec = position['ra'], position['dec']
            self.setpointCoordinates.setValue(ra, dec)

    def logNow(self):
        """ Force to log message and start new timer  """
        self._logThread.force()


    def pcControlSelected(self):
        """  Returns True if status flag read from PLC equals "1" (PC control selected)
             Returns False if status flag read from PLC equals "0" (REMOTE control selected)"""
        return self._resources.getPLCManager().isPCControl()

    def remoteControlSelected(self):
        """  Returns True if status flag read from PLC equals "0" (REMOTE control selected)
             Returns False if status flag read from PLC equals "1" (PC control selected)"""
        return not self._resources.getPLCManager().isPCControl()

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
        return True #TODO add more complex logic here


class SetPoint(object):
    def __init__(self, ra=0, dec=0):
        self.set(ra, dec)

    def set(self, ra, dec):
        """ can take coordinates in RAD or string (HH:MIN:SEC) """
        ra, dec = astronomy.getCoordinates(ra, dec)
        self._ra, self._dec = astronomy.normCoordinates(ra, dec)

    def get(self):
        return self._ra, self._dec

    def getCoordinatesAsString(self):
        return astronomy.rad2str(self._ra, self._dec)


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







