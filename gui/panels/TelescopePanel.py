import wx
from gui.panels.SimplePanel import SimplePanel

__author__ = 'kitru'

class TelescopePanel(SimplePanel):
    def __init__(self, parent, codes, controller):
        SimplePanel.__init__(self, parent)

        self._codes = codes
        self._telescope = controller.telescope

        sizer = wx.GridSizer(0, 2, 5, 10)

        labels = self._telescope.getLabels()
        self._fields = self._addFields(sizer, labels)

        comSizer = wx.StaticBoxSizer(wx.StaticBox(self, label=self._codes.get('pTelescope')), wx.VERTICAL)
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
        statuses = self._telescope.readStatus()
        for status in statuses:
            field = self._fields[status]
            value = statuses[status]
            field.SetLabel(self._codes.get(value))