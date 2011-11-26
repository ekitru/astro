import wx
from gui.panels.SimplePanel import SimplePanel

__author__ = 'kitru'

class StatusPanel(SimplePanel):
    """This panel represents current telescope status
    Attributes:
        codes - Translation codes
    """

    def __init__(self, parent, controller):
        SimplePanel.__init__(self, parent)

        codes = controller.codes
        sizer = wx.GridSizer(0, 2, 5, 5)

        status = controller.resources.plcManager.readTelescopeStatus()
        self._statuses = dict()
        for key in status:
            field = self.CreateField()
            sizer.Add(self.CreateCaption(codes.get(key)), flag=wx.ALL | wx.CENTER | wx.ALIGN_RIGHT)
            sizer.Add(field, flag=wx.ALL | wx.CENTER | wx.ALIGN_CENTER)
            self._statuses[key] = field

        comSizer = wx.StaticBoxSizer(wx.StaticBox(self, label=codes.get('pStatus')), wx.VERTICAL)
        comSizer.Add(sizer, flag=wx.ALL | wx.EXPAND, border=10)
        self.SetSizer(comSizer)

    def update(self, resources):
        statuses = resources.plcManager.readTelescopeStatus()
        for key in statuses:
            field = self._statuses[key]
            field.SetLabel(statuses[key])