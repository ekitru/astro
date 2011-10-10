#!/usr/bin/python2.6 -B
# -*- coding: UTF-8 -*-
from core.Controller import Controller
from core.Exceptions import InitializationException, ClosingException

import wx
from gui.MainGui import MainGui

__author__ = 'kitru'

def runGui(controller):
    app = wx.App(False)
    MainGui(None, 'AstroLab', controller)
    app.MainLoop()

if __name__ == '__main__':
    try:
        controller = Controller()
        controller.initialization()
        runGui(controller)
        controller.freeResources()
    except InitializationException as exception:
        print("Unexcepted error occured during resources initialization: " + exception.__str__())
        raise exception
    except ClosingException as exception:
        print("Unexcepted error occured during resources closing: " + exception.__str__())
        raise exception