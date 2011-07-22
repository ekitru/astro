#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import logging

from configuration import Configuration, ConfigurationException
from dbManager import getDbConnection
from translations import Translate

__author__ = 'kitru'

if __name__ == '__main__':
    try:

        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                            datefmt='%m-%d %H:%M',
                            filename='astroFull.log',
                            filemode='w')

        logging.info('Program initialization')
        #Read configuration file
        configuration = Configuration('default.cnf')

        #Establish connection to DB
        dbConfig = configuration.getDbConfigDict()
        db = getDbConnection(dbConfig)
        cursor = db.cursor()
        cursor.execute('select version()')
        row = cursor.fetchone()
        if row is not None:
            print("Db connection established")
        else:
            print("Dd failed")

#        Read selected language translation
        codes = configuration.getCodes()
        translate = Translate(codes)
        if translate.get("help"):
            print("Translation page loaded")
        else:
            print("Translation failed")

        translate.get('sfasdf')
    except ConfigurationException as ce:
        print("Error during configuration occure:"+ce.__str__())
    except Exception as e:
        print(e.message)
        print("Unexcepted error occur:" + e.__str__())

    pass
  