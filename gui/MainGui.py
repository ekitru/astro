# -*- coding: utf-8 -*-

import wx
from gui.AstroMenu import AstroMenu
from panels import *
from ids import *

class MainGui(wx.Frame):
    """ Main GUI class, includes all panels and dialogs with Binding for calls  """

    def __init__(self, parent, title, controller):
        super(MainGui, self).__init__(parent, title=title,
                                      size=(706, 388))
        #        InspectionTool().Show()
        self.controller = controller
        self.resources = controller.resources

        codes = controller.resources.codes
        panelArgs = {"parent": self, "codes": codes}

        self.objectPanel = ObjectPanel(**panelArgs)
        self.positioningPanel = PositionPanel(**panelArgs)
        self.manualSetpointPanel = ManualSetpointPanel(resources=self.resources, **panelArgs)
        self.controlModePanel = ControlModePanel(self, codes, self.resources, self.manualSetpointPanel)

        self.timeDatePanel = TimeDatePanel(**panelArgs)
        self.telescopePanel = TelescopePanel(self, self.resources)
        self.statusPanel = StatusPanel(self, self.resources)

        leftColon = wx.BoxSizer(wx.VERTICAL)
        leftColon.Add(self.objectPanel, flag=wx.ALL | wx.EXPAND)
        leftColon.Add(self.positioningPanel, flag=wx.ALL | wx.EXPAND)
        leftColon.AddSpacer(10)
        leftColon.Add(self.controlModePanel, flag=wx.ALL | wx.EXPAND)
        leftColon.AddSpacer(5)
        leftColon.Add(self.manualSetpointPanel, flag=wx.ALL | wx.EXPAND)

        rightColon = wx.BoxSizer(wx.VERTICAL)
        rightColon.Add(self.timeDatePanel, flag=wx.ALL | wx.EXPAND)
        rightColon.Add(self.telescopePanel, flag=wx.ALL | wx.EXPAND)
        rightColon.Add(self.statusPanel, flag=wx.ALL | wx.EXPAND)
        rightColon.SetMinSize((300, -1))

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

        self.SetStatusText(codes.get('mainSuccStart'))

        self.SetSizer(commonSizer)
        self.Layout()
        self.Centre()


    def update(self, event):
        """ Updates panels view """
        self.objectPanel.update(self.resources)
        self.timeDatePanel.update(self.resources)
        self.positioningPanel.update(self.resources)
        self.manualSetpointPanel.update(self.controller)
        self.controlModePanel.update(self.controller)
        self.statusPanel.update(self.resources)
        self.telescopePanel.update(self.resources)
        self.Fit()
        self.Show()