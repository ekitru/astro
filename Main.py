#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import configuration
from dbManager import getDbConnection
from translations import *

__author__ = 'kitru'

if __name__ == '__main__':
    try:

        config = configuration.getConfigFromFile("default.cnf")
        db = getDbConnection(config)
        cursor = db.cursor()
        cursor.execute('select version()')
        row = cursor.fetchone()
        print(row)

        translations = getSelectedTranslation(config)
        print(getSelectedTranslation(config))



    except configuration.ConfigurationException as ce:
        print("Error during configuration occure:"+ce.__str__())
#    except Exception as e:
#        print("Unexcepted error occur:"+e.__str__())

    pass
  