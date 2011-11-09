import wx
from gui.panels.SimplePanel import SimplePanel

__author__ = 'kitru'

class AlarmDialog(wx.Dialog, SimplePanel):
    """ Very simple dialog to set up logging time and select languages """

    def __init__(self, parent, resources):
        codes = resources.getCodes()
        wx.Dialog.__init__(self, parent, title=codes.get('dAlarm_title'),
                           style=wx.CAPTION | wx.YES_NO | wx.YES_DEFAULT)

        alarmSizer = wx.GridSizer(0, 2, 5, 5)
        status = resources.getPLCManager().readAlarms()
        self._statuses = dict()
        for key in status:
            field = self.CreateField()
            alarmSizer.Add(self.CreateCaption(codes.get(key)), flag=wx.ALL | wx.CENTER | wx.ALIGN_RIGHT)
            alarmSizer.Add(field, flag = wx.ALL | wx.CENTER | wx.ALIGN_CENTER)
            self._statuses[key]=field

        buttons = wx.FlexGridSizer(1, 1, 5, 10)
        buttons.Add(wx.Button(self, wx.ID_CANCEL, label=codes.get('tAlarm_cancel')), flag=wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(alarmSizer)
        sizer.Add(buttons)
        self.SetSizer(sizer)
        self.SetFocus()
        self.Fit()
        self.update(resources)

    def update(self, resources):
        status = resources.getPLCManager().readAlarms()
        for key in status:
            field  =self._statuses[key]
            field.SetLabel(status[key])


