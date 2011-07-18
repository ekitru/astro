#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import configuration
import modbus_tk
from dbManager import getDbConnection
from translations import *

__author__ = 'kitru'

if __name__ == '__main__':
    try:
        #Read configuration file
        config = configuration.getConfigFromFile("default.cnf")

        #Establish connection to DB
        db = getDbConnection(config)
        cursor = db.cursor()
        cursor.execute('select version()')
        row = cursor.fetchone()
        if row is not None:
            print("Db connection established")
        else:
            print("Dd failed")

        #Read selected language translation
        codes = getSelectedTranslation(config)
        translate = Translate(codes)
        if translate.get("about"):
            print("Translation page loaded")
        else:
            print("Translation failed")



    except configuration.ConfigurationException as ce:
        print("Error during configuration occure:"+ce.__str__())
    except Exception as e:
        print("Unexcepted error occur:"+e.__str__())

    pass
  