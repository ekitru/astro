#!/usr/bin/python
# -*- coding: utf-8 -*-

# absolute.py

import wx
from astroCore import ClosingException, InitializationException, AstroController

ID_TIMEDATE = 1001

class TimeDatePanel(wx.Panel):
    def __init__(self, parent, ID=ID_TIMEDATE, pos=wx.DefaultPosition, size=(50, 50), controller=None):
        wx.Panel.__init__(self, parent, ID, pos, size, wx.RAISED_BORDER)
        self.controller = controller
        transCoded = controller.transCodes
        layout = wx.GridSizer(5,2,0,10)
        layout.Add(wx.StaticText(self, wx.ID_ANY, transCoded.get("Time & Date")))
        layout.Add(wx.StaticText(self, wx.ID_ANY, ""), 0,flag=wx.ALL)
        layout.Add(wx.StaticText(self, wx.ID_ANY, transCoded.get("Local time")), 0,flag=wx.ALL|wx.ALIGN_RIGHT)
        self.LT = wx.StaticText(self, wx.ID_ANY, "")
        layout.Add(self.LT)
        layout.Add(wx.StaticText(self, wx.ID_ANY, transCoded.get("UTC")), 0,flag=wx.ALL|wx.ALIGN_RIGHT)
        self.UTC = wx.StaticText(self, wx.ID_ANY, "")
        layout.Add(self.UTC)
        layout.Add(wx.StaticText(self, wx.ID_ANY, transCoded.get("Julian day")), 0,flag=wx.ALL|wx.ALIGN_RIGHT)
        self.JD = wx.StaticText(self, wx.ID_ANY, "")
        layout.Add(self.JD)
        layout.Add(wx.StaticText(self, wx.ID_ANY, transCoded.get("Local sidereal time")), 0,flag=wx.ALL|wx.ALIGN_RIGHT)
        self.LST = wx.StaticText(self, wx.ID_ANY, "")
        layout.Add(self.LST)
        self.SetSizer(layout)
        self.updateTimeDate()
        self.Fit()

        wx.EVT_PAINT(self, self.onPaint)

    def onPaint(self, event=None):
        self.updateTimeDate()

    def updateTimeDate(self):
        mechanics = self.controller.mechanics
        self.LT.SetLabel(str(mechanics.getLT()))
        self.UTC.SetLabel(str(mechanics.getUTC()))
        self.JD.SetLabel(str(mechanics.getYD()))
        self.LST.SetLabel(str(mechanics.getLST()))



class AstroGui(wx.Frame):
    def __init__(self, parent, title, controller):
        super(AstroGui, self).__init__(parent, title=title,
                                       size=(600, 600))
        self.controller = controller
        mainLayout = wx.GridSizer(2, 2, 1, 1)
        self.timeDatePanel = TimeDatePanel(self, controller = self.controller)
        self.timeDatePanel.SetBackgroundColour("green")

        mainLayout.Add(self.timeDatePanel)
        self.SetSizer(mainLayout)
        self.Centre()
        self.Show()
