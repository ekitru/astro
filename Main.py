#!/usr/bin/python -B
# -*- coding: UTF-8 -*-
from core.Controller import Controller
from core.Exceptions import InitializationException, ClosingException, GuiException

import wx
from gui.MainGui import MainGui

__author__ = 'kitru'



if __name__ == '__main__':
    app = wx.App(False)
    controller = Controller()
    MainGui(None, 'AstroLab', controller)
    controller.initialization()
    app.MainLoop()




    controller.freeResources()
