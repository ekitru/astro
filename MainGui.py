#!/usr/bin/python
# -*- coding: utf-8 -*-

# absolute.py
from unohelper import inspect

import wx
import time
from wx.lib.inspection import InspectionTool
from panels import TimeDatePanel, ObjectPanel, PositioningPanel, TelescopePanel

class MainGui(wx.Frame):
    def __init__(self, parent, title, controller):
        super(MainGui, self).__init__(parent, title=title,
                                       size=(800, 400))
#        InspectionTool().Show()
        self.controller = controller
        trans=self.controller.trans

        menuBar = wx.MenuBar()
        objMenu = self.CreateObjectMenu(trans)
        toolsMenu = self.CreateToolsMenu(trans)

        menuBar.Append(objMenu, trans.get('mObj'))
        menuBar.Append(toolsMenu, trans.get('mTools'))
        self.SetMenuBar(menuBar)

        self.CreateStatusBar()
        self.SetStatusText('Program starts')

        sizer = wx.GridSizer(4, 1, 10, 10)
        self.objectPanel = ObjectPanel(parent=self, codes=trans)
        self.timeDatePanel = TimeDatePanel(parent=self, codes=trans)
        self.positioningPanel = PositioningPanel(parent=self, codes=trans)

        sizer.Add(self.objectPanel )
        sizer.Add(self.timeDatePanel, flag = wx.ALL | wx.EXPAND)
        sizer.Add(self.positioningPanel)
        sizer.Add(TelescopePanel(parent=self), flag = wx.ALL | wx.EXPAND)
        self.SetSizer(sizer)
#        self.Fit()
        self.Centre()
#        self.Show()

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)
        self.timer.Start(500)

    def CreateObjectMenu(self, codes):
        menu = wx.Menu()
        self.selectObj = wx.MenuItem(menu, wx.ID_ANY,text=codes.get("smSelObj")+"\tctrl+s", help="Select object from database or add new one")
        self.editObj = wx.MenuItem(menu, wx.ID_ANY, text=codes.get("smEditObj")+"\tctrl+e", help="Add, Delete, Edit object properties")
        menu.AppendItem(self.selectObj)
        menu.AppendItem(self.editObj)
        return menu

    def CreateToolsMenu(self, codes):
        menu = wx.Menu()
        self.settings = wx.MenuItem(menu, wx.ID_ANY,text=codes.get('mSettings'), help="System setup")
        menu.AppendItem(self.settings)
        return menu

    def update(self, event):
        print(time.ctime())
        self.objectPanel.update('Sirius', ('10:10:10','45:00:00'), ('12:00:00','48:32:32'))
        self.timeDatePanel.update(self.controller.mechanics.getCurrentTimeDate())
        self.positioningPanel.update()
        self.Fit()
        self.Show()
