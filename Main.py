#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from astroCore import AstroController, InitializationException

__author__ = 'kitru'

if __name__ == '__main__':
    try:
        controller = AstroController()
        star = controller.dbManager.getStar('sirius3')
        print(star)
        controller.freeResources()

    except InitializationException as e:
        print("Unexcepted error occur:" + e.__str__())
        raise e

    pass
  