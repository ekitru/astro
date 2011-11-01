import wx
from gui.panels.SimplePanel import SimplePanel

__author__ = 'kitru'


class TelescopePanel(SimplePanel):
    def __init__(self, parent, resources):
        SimplePanel.__init__(self, parent)

        codes = resources.getCodes()
        status = resources.getPLCManager().readTelescopeMode()
        self._statuses = dict()
        sizer = wx.GridSizer(0, 2, 5, 5)
        for key in status:
            field = self.CreateField()
            sizer.Add(self.CreateCaption(codes.get(key)), flag=wx.ALL | wx.CENTER | wx.ALIGN_RIGHT)
            sizer.Add(field, flag = wx.ALL | wx.CENTER | wx.ALIGN_CENTER)
            self._statuses[key]=field

        comSizer = wx.StaticBoxSizer(wx.StaticBox(self, label=codes.get('pTelescope')), wx.VERTICAL)
        comSizer.Add(sizer, flag=wx.ALL, border=10)
        self.SetSizer(comSizer)

    def update(self, resources):
        codes = resources.getCodes()
        status = resources.getPLCManager().readTelescopeMode()
        for key in status:
            field  = self._statuses[key]
            field.SetLabel(codes.get(status[key]))

  