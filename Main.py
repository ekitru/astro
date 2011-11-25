#!/usr/bin/python2.6 -B
# -*- coding: UTF-8 -*-
from core.Controller import Controller
from core.Exceptions import InitializationException, ClosingException, GuiException

import wx
from gui.MainGui import MainGui

__author__ = 'kitru'



if __name__ == '__main__':
    try:
        app = wx.App(False)
        controller = Controller()
        MainGui(None, 'AstroLab', controller)
        controller.initialization()
        app.MainLoop()

        controller.freeResources()
    except InitializationException as exception:
        print("Unexcepted error occured during resources initialization: " + exception.__str__())
        raise exception
    except GuiException as exception:
        print("GUI finished by exception: " + exception.__str__())
        raise exception
    except ClosingException as exception:
        print("Unexcepted error occured during resources closing: " + exception.__str__())
        raise exception