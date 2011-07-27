#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from astroCore import AstroController, InitializationException

__author__ = 'kitru'

if __name__ == '__main__':
    try:
        controller = AstroController()
        controller.dbManager.saveNewStar('test3','123','123')
        star = controller.dbManager.getStar('test2')
        print(star)
        controller.freeResources()
    except InitializationException as e:
        print("Unexcepted error occur:" + e.__str__())
        raise e

    pass
  