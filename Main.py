#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import wx
from AstroGui import AstroGui
from astroCore import AstroController, InitializationException, ClosingException

__author__ = 'kitru'

if __name__ == '__main__':
    try:
        controller = AstroController()
    except InitializationException as exception:
        print("Unexcepted error occur during initialization: " + exception.__str__())
        raise exception

    app = wx.App()
    AstroGui(None, title='AstroLab', controller=controller)
    app.MainLoop()

    try:
        controller.freeResources()
    except ClosingException as exception:
        print("Unexcepted error occur during closing resources: " + exception.__str__())
        raise exception