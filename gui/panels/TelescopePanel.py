import wx
from gui.panels.SimplePanel import SimplePanel

__author__ = 'kitru'

class TelescopePanel(SimplePanel):
    def __init__(self, parent, resources):
        SimplePanel.__init__(self, parent)

        codes = resources.getCodes()
        sizer = wx.GridSizer(0, 2, 5, 10)
        self._statuses = dict()

        status = resources.getPLCManager().readTelescopeConnStatus()
        self.addFields(codes, sizer, status)

        status = resources.getPLCManager().readTelescopeMovingStatus()
        self.addFields(codes, sizer, status)

        status = resources.getPLCManager().readTelescopeMode()
        self.addFields(codes, sizer, status)

        status = resources.getPLCManager().readTemperature()
        self.addFields(codes, sizer, status)

        comSizer = wx.StaticBoxSizer(wx.StaticBox(self, label=codes.get('pTelescope')), wx.VERTICAL)
        comSizer.Add(sizer, flag=wx.ALL | wx.EXPAND, border=10)
        self.SetSizer(comSizer)

    def addFields(self, codes, sizer, status):
        for key in status:
            field = self.CreateField()
            sizer.Add(self.CreateCaption(codes.get(key)), flag=wx.ALL | wx.ALIGN_RIGHT)
            sizer.Add(field, flag=wx.ALL | wx.EXPAND | wx.ALIGN_CENTER)
            self._statuses[key] = field

    def _readStatuses(self, codes, status):
        for key in status:
            field = self._statuses[key]
            field.SetLabel(codes.get(status[key]))

    def update(self, resources):
        codes = resources.getCodes()

        status = resources.getPLCManager().readTelescopeConnStatus()
        self._readStatuses(codes, status)

        status = resources.getPLCManager().readTelescopeMovingStatus()
        self._readStatuses(codes, status)

        status = resources.getPLCManager().readTelescopeMode()
        self._readStatuses(codes, status)

        status = resources.getPLCManager().readTemperature()
        self._readStatuses(codes, status)
  