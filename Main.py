#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import wx
from Controller import Controller, InitializationException, ClosingException, SetPoint
from MainGui import MainGui

__author__ = 'kitru'

def check(controller):
    pass

if __name__ == '__main__':
    try:
        controller = Controller()
        controller.initialization()
        check(controller)
        app = wx.App(False)
        MainGui(None, 'AstroLab', controller)
        app.MainLoop()

        controller.freeResources()
    except InitializationException as exception:
        print("Unexcepted error occur during initialization: " + exception.__str__())
        raise exception
    except ClosingException as exception:
        print("Unexcepted error occur during closing resources: " + exception.__str__())
        raise exception