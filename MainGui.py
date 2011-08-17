#!/usr/bin/python
# -*- coding: utf-8 -*-

# absolute.py

import wx
import time
from panels import TimeDatePanel, ObjectPanel, PositioningPanel

class MainGui(wx.Frame):
    def __init__(self, parent, title, controller):
        super(MainGui, self).__init__(parent, title=title,
                                       size=(800, 400))
        self.controller = controller
        trans=self.controller.trans

        menuBar = wx.MenuBar()
        objMenu = self.CreateObjectMenu(trans)
        toolsMenu = self.CreateToolsMenu(trans)

        menuBar.Append(objMenu, trans.get('menu Object'))
        menuBar.Append(toolsMenu, trans.get('menu Tools'))
        self.SetMenuBar(menuBar)

        self.CreateStatusBar()
        self.SetStatusText('Program starts')

        sizer = wx.FlexGridSizer(2, 2, 10, 10)
        self.objectPanel = ObjectPanel(parent=self, codes=trans)
        self.timeDatePanel = TimeDatePanel(parent=self, codes=trans)
        self.positioningPanel = PositioningPanel(parent=self, codes=trans)

        sizer.Add(self.objectPanel)
        sizer.Add(self.timeDatePanel)
        sizer.Add(self.positioningPanel)
        self.SetSizer(sizer)
#        self.Fit()
        self.Centre()
#        self.Show()

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)
        self.timer.Start(500)

    def CreateObjectMenu(self, codes):
        menu = wx.Menu()
        self.selectObj = wx.MenuItem(menu, wx.ID_ANY,text=codes.get("&Select object")+"\tctrl+s", help="Select object from database or add new one")
        self.editObj = wx.MenuItem(menu, wx.ID_ANY, text=codes.get("&Edit objects")+"\tctrl+e", help="Add, Delete, Edit object properties")
        menu.AppendItem(self.selectObj)
        menu.AppendItem(self.editObj)
        return menu

    def CreateToolsMenu(self, codes):
        menu = wx.Menu()
        self.settings = wx.MenuItem(menu, wx.ID_ANY,text=codes.get("Settings"), help="System setup")
        menu.AppendItem(self.settings)
        return menu

    def update(self, event):
        print(time.ctime())
        self.objectPanel.update('Sirius', ('10:10:10','45:00:00'), ('12:00:00','48:32:32'))
        self.timeDatePanel.update(self.controller.mechanics.getCurrentTimeDate())
        self.positioningPanel.update()
        self.Fit()
        self.Show()
