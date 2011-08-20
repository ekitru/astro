import os
from posixpath import join
import logging

from Exceptions import ConfigurationException, InitializationException, ClosingException
from Configs import ProgramConfig

__author__ = 'kitru'

class Controller(object):
    def __init__(self):
        self.__initLogger()
        self.object = {}


    def __initLogger(self):
        if not os.path.exists('logs'):
            os.makedirs('logs', mode=0711)
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                            datefmt='%m-%d %H:%M',
                            filename=join('logs', 'common.log'),
                            filemode='w')

    def initialization(self):
        """ Initialization for all components
        Opens DB connection and connection with PLCm also reads translation codes
        """
        try:
            logging.info('======= Program initialization =======')
            config = ProgramConfig('default.conf')
            self.mechanics = config.openAstroMechanics()
            self.dbManager = config.getDbManager()
            self.commManager = config.getPLCManager()
            self.trans = config.getTranslationConf()
        except ConfigurationException as ce:
            logging.error('Erron during initialization occure: ' + ce.__str__())
            raise InitializationException(ce)

    def freeResources(self):
        try:
            logging.info('======= Free all resources: DB, MODBUS =======')
            self.dbManager.close()
            self.commManager.close()
        except Exception as e:
            raise ClosingException(e)


    def getStarById(self, id):
        """ Take star from database by index ID  """
        star = self.dbManager.getStarById(id)
        return self.parseStar(star)

    def getStars(self, name):
        """ Returns list of star objects(id, name,ra,dec)
        Fetchs all rows with similar star name like name%
        """
        stars = self.dbManager.getStarsByPartName(name)

        resp = []
        for star in stars:
            resp.append(self.parseStar(star))
        return resp

    def parseStar(self, star):
        """ Convert database resultset into dictionary(id,name,ra,dec)
        Attr:
          star - one record fron DB
        """
        id = long(star[0])
        name = str(star[1])
        ra, dec = self.mechanics.convCoord(star[2], star[3])
        return {'id': id, 'name': name, 'ra': ra, 'dec': dec}

    def setObject(self, name, RA, DEC):
        """ Stores new object for observer and current position in the sky
        Attr:
            name - star name
            RA - epoch2000 position right ascension
            DEC - epoch2000 position declination
        """
        print('set object', name, RA, DEC)
        self.object['name'] = name
        self.object['orig'] = self.mechanics.convCoord(str(RA), str(DEC))
        self.object['curr'] = self.computePosition(self.object['orig'])

    def computePosition(self, orig):
        return ('10', '10') #TODO

    def getObject(self):
        return self.object