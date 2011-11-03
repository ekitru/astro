import wx
from gui.panels.SimplePanel import SimplePanel

__author__ = 'kitru'

class StatusPanel(SimplePanel):
    """This panel represents current telescope status
    Attributes:
        codes - Translation codes
    """
    def __init__(self, parent, resources):
        SimplePanel.__init__(self, parent)

        codes = resources.getCodes()
        sizer = wx.GridSizer(0, 2, 5, 5)

        status = resources.getPLCManager().readTelescopeStatus()
        self._statuses = dict()
        for key in status:
            field = self.CreateField()
            sizer.Add(self.CreateCaption(codes.get(key)), flag=wx.ALL | wx.CENTER | wx.ALIGN_RIGHT)
            sizer.Add(field, flag = wx.ALL | wx.CENTER | wx.ALIGN_CENTER)
            self._statuses[key]=field

        comSizer = wx.StaticBoxSizer(wx.StaticBox(self, label=codes.get('pStatus')), wx.VERTICAL)
        comSizer.Add(sizer, flag=wx.ALL | wx.EXPAND, border=10)
        self.SetSizer(comSizer)

    def update(self, resources):
        status = resources.getPLCManager().readTelescopeStatus()
        for key in status:
            field  =self._statuses[key]
            field.SetLabel(status[key])