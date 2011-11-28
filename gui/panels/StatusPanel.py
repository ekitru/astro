import wx
from gui.panels.SimplePanel import SimplePanel

__author__ = 'kitru'

class StatusPanel(SimplePanel):
    """This panel represents current telescope status
    Attributes:
        codes - Translation codes
    """

    def __init__(self, parent, codes, statuses):
        SimplePanel.__init__(self, parent)

        sizer = wx.GridSizer(0, 2, 5, 5)

        self._codes = codes
        self._statuses = statuses
        labels = self._statuses.getLabels()
        self._fields = self._addFields(sizer, labels)

        comSizer = wx.StaticBoxSizer(wx.StaticBox(self, label=self._codes.get('pStatus')), wx.VERTICAL)
        comSizer.Add(sizer, flag=wx.ALL | wx.EXPAND, border=10)
        self.SetSizer(comSizer)

    def _addFields(self, sizer, labels):
        fields = dict()
        for label in labels:
            field = self.CreateField()
            sizer.Add(self.CreateCaption(self._codes.get(label)), flag=wx.ALL | wx.ALIGN_RIGHT)
            sizer.Add(field, flag=wx.ALL | wx.EXPAND | wx.ALIGN_CENTER)
            fields[label] = field
        return fields


    def update(self):
        statuses = self._statuses.readStatus()
        for key in statuses:
            field = self._fields[key]
            field.SetLabel(statuses[key])