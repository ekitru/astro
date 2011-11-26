import wx
from gui.panels.SimplePanel import SimplePanel

__author__ = 'kitru'

class TelescopePanel(SimplePanel):
    def __init__(self, parent, controller):
        SimplePanel.__init__(self, parent)

        codes = controller.codes
        sizer = wx.GridSizer(0, 2, 5, 10)
        self._statuses = dict()

        status = controller.resources.plcManager.readTelescopeConnStatus()
        self.addFields(codes, sizer, status)

        status = controller.resources.plcManager.readTelescopeMovingStatus()
        self.addFields(codes, sizer, status)

        status = controller.resources.plcManager.readTelescopeMode()
        self.addFields(codes, sizer, status)

        status = controller.resources.plcManager.readTemperature()
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

    def update(self, controller):
        codes = controller.codes

        status = []
        status.append(controller.resources.plcManager.readTelescopeConnStatus())
        status.append(controller.resources.plcManager.readTelescopeMovingStatus())
        status.append(controller.resources.plcManager.readTelescopeMode())
        status.append(controller.resources.plcManager.readTemperature())
        for st in status:
            self._readStatuses(codes, st)

    def _readStatuses(self, codes, status):
        for key in status:
            field = self._statuses[key]
            field.SetLabel(codes.get(status[key]))
