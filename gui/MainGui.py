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
        self._controller = controller

        codes = controller.getResourceKeeper().getCodes()
        panelArgs = {"parent": self, "codes": codes}

        self.objectPanel = ObjectPanel(**panelArgs)
        self.timeDatePanel = TimeDatePanel(**panelArgs)
        self.positioningPanel = PositionPanel(**panelArgs)
        self.telescopePanel = TelescopePanel(**panelArgs)
        self.manualSetpointPanel = ManualSetpointPanel(controller=self._controller, **panelArgs)
        self.controlModePanel = ControlModePanel(**panelArgs)

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

        grid = wx.FlexGridSizer(1, 2, 10, 10)
        grid.Add(leftColon, flag=wx.ALL | wx.EXPAND)
        grid.Add(rightColon, flag=wx.ALL | wx.EXPAND)

        commonSizer = wx.BoxSizer(wx.VERTICAL)
        commonSizer.Add(grid, flag=wx.ALL | wx.EXPAND, border=10)

        self.timer = wx.Timer(self)

        self.Bind(wx.EVT_TIMER, self.update, self.timer)
        self.timer.Start(500)
        menu = AstroMenu(self._controller)

        self.SetMenuBar(menu)
        self.Bind(wx.EVT_MENU, menu.OnSelectObject, id=ID_SELOBJ)

        self.Bind(wx.EVT_MENU, menu.OnEditObject, id=ID_EDITOBJ)
        self.Bind(wx.EVT_MENU, menu.OnMessage, id=ID_MESSAGE)

        self.Bind(wx.EVT_MENU, menu.OnLogs, id=ID_LOGS)
        self.Bind(wx.EVT_MENU, menu.OnSettings, id=ID_SETTINGS)
        self.CreateStatusBar()

        self.SetStatusText(codes.get('mainSuccStart'))

        self.SetSizer(commonSizer)
        self.Layout()
        self.Centre()


    def update(self, event):
        """ Updates panels view """
        self._controller.updateSetPoint()
        self.objectPanel.update(self._controller)
        self.timeDatePanel.update(self._controller)
        self.positioningPanel.update(self._controller)
        self.manualSetpointPanel.update(self._controller)
        self.controlModePanel.update(self._controller)
        self.Fit()
        self.Show()
        event.Skip(False)