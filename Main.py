#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import wx
from AstroController import AstroController, InitializationException, ClosingException
from MainGui import MainGui

__author__ = 'kitru'

if __name__ == '__main__':
    try:
        controller = AstroController()
    except InitializationException as exception:
        print("Unexcepted error occur during initialization: " + exception.__str__())
        raise exception

    app = wx.App()
    MainGui(None, title='AstroLab', controller=controller)
    app.MainLoop()

    try:
        controller.freeResources()
    except ClosingException as exception:
        print("Unexcepted error occur during closing resources: " + exception.__str__())
        raise exception