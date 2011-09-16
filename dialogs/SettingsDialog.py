import wx

__author__ = 'kitru'

class SettingsDialog(wx.Dialog):
    def __init__(self, parent, id, controller):
        wx.Dialog.__init__(self, parent, id, controller.getResourceKeeper().getCodes().get('dSet_title'), style=wx.CAPTION | wx.YES_NO | wx.YES_DEFAULT)