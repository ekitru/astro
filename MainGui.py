#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
from wx.lib.inspection import InspectionTool
from dialogs import SelectObjectDiag
from ids import *
from panels import TimeDatePanel, ObjectPanel, PositioningPanel, TelescopePanel

class MainGui(wx.Frame):
    def __init__(self, parent, title, controller):
        super(MainGui, self).__init__(parent, title=title,
                                      size=(706, 388))
#        InspectionTool().Show()
        self.controller = controller
        self.trans = self.controller.trans

        menuBar = AstroMenu(self.trans)
        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.OnSelectObject, id=ID_SELOBJ)
        self.Bind(wx.EVT_MENU, self.OnEditObject, id=ID_EDITOBJ)
        self.Bind(wx.EVT_MENU, self.OnSettings, id=ID_SETTINGS)

        self.CreateStatusBar()
        self.SetStatusText('Program starts')

        grid = wx.GridSizer(2, 2, 10, 10)

        panelArgs = {"parent": self, "codes": self.trans}
        self.objectPanel = ObjectPanel(ID=ID_OBJPANEL, **panelArgs)
        self.timeDatePanel = TimeDatePanel(ID=ID_TIMEPANEL, **panelArgs)
        self.positioningPanel = PositioningPanel(ID=ID_POSITIONING, **panelArgs)
        self.telescopePanel = TelescopePanel(ID=ID_TELESCOPE, **panelArgs)

        grid.Add(self.objectPanel, flag=wx.ALL | wx.EXPAND)
        grid.Add(self.timeDatePanel, flag=wx.ALL | wx.EXPAND)
        grid.Add(self.positioningPanel, flag=wx.ALL | wx.EXPAND)
        grid.Add(self.telescopePanel, flag=wx.ALL | wx.EXPAND)

        canvas = wx.BoxSizer(wx.VERTICAL)
        canvas.Add(grid, flag=wx.ALL, border=10)
        self.SetSizer(canvas)
        self.Centre()
        self.Show()

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)
        self.timer.Start(500)

    def OnSelectObject(self, event):
        selObj = SelectObjectDiag(None, wx.ID_ANY, self.controller)
        selObj.ShowModal()
        selObj.Destroy()


    def OnEditObject(self, event):
        print('Edit object')

    def OnSettings(self, event):
        print('Settings')

    def update(self, event):
        self.objectPanel.update('Sirius', ('10:10:10', '45:00:00'), ('12:00:00', '48:32:32'))
        self.timeDatePanel.update(self.controller.mechanics.getCurrentTimeDate())
        self.positioningPanel.update()
        self.Fit()
#        self.Show()


class AstroMenu(wx.MenuBar):
    def __init__(self, trans):
        wx.MenuBar.__init__(self)

        objMenu = self.CreateObjectMenu(trans)
        toolsMenu = self.CreateToolsMenu(trans)

        self.Append(menu=objMenu, title=trans.get('mObj'))
        self.Append(menu=toolsMenu, title=trans.get('mTools'))

    def CreateObjectMenu(self, trans):
        menu = wx.Menu()
        self.selectObj = wx.MenuItem(menu, ID_SELOBJ, text=trans.get('smSelObj') + '\tctrl+o', help=trans.get('smSelObjHelp'))
        self.editObj = wx.MenuItem(menu, ID_EDITOBJ, text=trans.get('smEditObj') + '\tctrl+e', help=trans.get('smEditObjHelp'))
        menu.AppendItem(self.selectObj)
        menu.AppendItem(self.editObj)
        return menu

    def CreateToolsMenu(self, trans):
        menu = wx.Menu()
        self.settings = wx.MenuItem(menu, ID_SETTINGS, text=trans.get('smSettings') + '\tctrl+s', help=trans.get('smSettingsHelp'))
        menu.AppendItem(self.settings)
        return menu
