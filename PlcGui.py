# -*- coding: utf-8 -*-
__author__ = 'anisand'

import wx

class PlcGui(wx.MiniFrame):
    def __init__(self,parent,title):
        super(PlcGui,self).__init__(parent,title=title)
        self.Bind(wx.EVT_CLOSE, self.OnPlcGuiClose)

    def OnPlcGuiClose(self,event):
        app = wx.GetApp()
        mainGui = app.GetTopWindow()
        mainGui.resetStateOfPositioningPanel()
        self.Destroy()