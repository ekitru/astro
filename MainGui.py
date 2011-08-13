#!/usr/bin/python
# -*- coding: utf-8 -*-

# absolute.py

import wx
import time
from panels import TimeDatePanel, ObjectPanel

class MainGui(wx.Frame):
    def __init__(self, parent, title, controller):
        super(MainGui, self).__init__(parent, title=title,
                                       size=(800, 400))
        self.controller = controller
        mainLayout = wx.GridSizer(2, 2, 10, 10)
        self.objectPanel = ObjectPanel(parent=self, codes=self.controller.transCodes)
        self.timeDatePanel = TimeDatePanel(parent=self, codes=self.controller.transCodes)

        mainLayout.Add(self.objectPanel)
        mainLayout.Add(self.timeDatePanel)
        self.SetSizer(mainLayout)
#        self.Fit()
        self.Centre()
#        self.Show()

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)
        self.timer.Start(500)

    def update(self, event):
        print(time.ctime())
        self.timeDatePanel.update(self.controller.mechanics)

        self.Fit()
        self.Show()