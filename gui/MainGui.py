# -*- coding: utf-8 -*-

import wx
from gui.AstroMenu import AstroMenu
from panels import *
from ids import *

class MainGui(wx.Frame):
    """ Main GUI class, includes all panels and dialogs with Binding for calls  """

    def __init__(self, parent, title, controller):
        super(MainGui, self).__init__(parent, title=title, size=(706, 388))
        #        InspectionTool().Show()
        trans = controller.codes
        self.controller = controller
        self.resources = controller.resources

        self.objectPanel = ObjectPanel(self, ID_OBJECT_PANEL, trans)
        self.positioningPanel = PositionPanel(self, codes=trans)
        self.controlModePanel = ControlModePanel(self, trans, control=controller.tsControl)
        self.manualSetpointPanel = ManualSetpointPanel(self, ID_MANUAL_PANEL, codes=trans, resources=self.resources)

        self.timeDatePanel = TimeDatePanel(parent=self, codes=trans)
        self.telescopeModePanel = TelescopeModePanel(parent=self, codes=trans, mode=controller.tsMode)
        self.statusPanel = StatusPanel(parent=self, codes=trans, tsStatus=controller.tsStatus)

        leftColon = wx.BoxSizer(wx.VERTICAL)
        leftColon.Add(self.objectPanel, flag=wx.DOWN | wx.EXPAND, border=5)
        leftColon.Add(self.positioningPanel, flag=wx.DOWN | wx.EXPAND, border=5)
        leftColon.Add(self.controlModePanel, flag=wx.DOWN | wx.EXPAND, border=5)
        leftColon.Add(self.manualSetpointPanel, flag=wx.DOWN | wx.EXPAND, border=5)

        rightColon = wx.BoxSizer(wx.VERTICAL)
        rightColon.Add(self.timeDatePanel, flag=wx.ALL | wx.EXPAND)
        rightColon.Add(self.telescopeModePanel, flag=wx.ALL | wx.EXPAND)
        rightColon.Add(self.statusPanel, flag=wx.ALL | wx.EXPAND)
        rightColon.SetMinSize((320, -1))

        grid = wx.FlexGridSizer(1, 2, 10, 10)
        grid.Add(leftColon, flag=wx.ALL | wx.EXPAND)
        grid.Add(rightColon, flag=wx.ALL | wx.EXPAND)

        commonSizer = wx.BoxSizer(wx.VERTICAL)
        commonSizer.Add(grid, flag=wx.ALL | wx.EXPAND, border=10)

        self.timer = wx.Timer(self)

        self.Bind(wx.EVT_TIMER, self.update, self.timer)
        self.timer.Start(2000)

        menu = AstroMenu(self.controller)
        self.SetMenuBar(menu)
        self.Bind(wx.EVT_MENU, menu.OnSelectObject, id=ID_SELOBJ_DIALOG)
        self.Bind(wx.EVT_MENU, menu.OnEditObject, id=ID_EDITOBJ_DIALOG)
        self.Bind(wx.EVT_MENU, menu.OnMessage, id=ID_MSG_DIALOG)
        self.Bind(wx.EVT_MENU, menu.OnLogs, id=ID_LOGS_DIALOG)
        self.Bind(wx.EVT_MENU, menu.OnSettings, id=ID_SETTINGS_DIALOG)
        self.Bind(wx.EVT_MENU, menu.OnAlarms, id=ID_ALARMS_DIALOG)
        self.CreateStatusBar()

        self.SetStatusText(trans.get('mainSuccStart'))

        self.SetSizer(commonSizer)
        self.Layout()
        self.Centre()


    def update(self, event):
        """ Updates panels view """
        self.objectPanel.update(self.controller)
        self.timeDatePanel.update(self.controller)

        if self.controller.isConnected():
            self.telescopeModePanel.update()
            self.statusPanel.update()
            self.controlModePanel.update()
            self.positioningPanel.update(self.controller)

        self.manualSetpointPanel.update(self.controller)

        self.Layout()
        self.Fit()
        self.Show()