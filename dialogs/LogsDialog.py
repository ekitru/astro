import wx

__author__ = 'kitru'

class LogsDialog(wx.Dialog):
    def __init__(self, parent, id, controller):
        wx.Dialog.__init__(self, parent, id, controller.getResourceKeeper().getCodes().get('dLogs_title'),
                           style=wx.CAPTION | wx.YES_NO | wx.YES_DEFAULT)
        codes = controller.getResourceKeeper().getCodes()

        self.list = self.CreateLists(codes)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.list, flag=wx.ALL | wx.EXPAND, border=10)
        sizer.Add(wx.Button(self, wx.ID_CANCEL, label=codes.get('dLogs_close')), flag=wx.ALL | wx.ALIGN_RIGHT)

        self.SetSizer(sizer)
        self.Fit()

    def CreateLists(self, codes):
        list = wx.ListCtrl(self, id=wx.ID_ANY, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        list.SetMinSize((950, 300))
        list.InsertColumn(col=0, heading=codes.get('dLogs_ID'), format=wx.LIST_FORMAT_LEFT)
        list.InsertColumn(col=1, heading=codes.get('dLogs_star_id'), format=wx.LIST_FORMAT_LEFT)
        list.InsertColumn(col=2, heading=codes.get('dLogs_star_name'), format=wx.LIST_FORMAT_LEFT)
        list.InsertColumn(col=3, heading=codes.get('dLogs_star_ra'), format=wx.LIST_FORMAT_LEFT)
        list.InsertColumn(col=4, heading=codes.get('dLogs_star_dec'), format=wx.LIST_FORMAT_LEFT)
        list.InsertColumn(col=5, heading=codes.get('dLogs_text'), format=wx.LIST_FORMAT_LEFT)
        list.InsertColumn(col=6, heading=codes.get('dLogs_ra'), format=wx.LIST_FORMAT_LEFT)
        list.InsertColumn(col=7, heading=codes.get('dLogs_dec'), format=wx.LIST_FORMAT_LEFT)
        list.InsertColumn(col=8, heading=codes.get('dLogs_focus'), format=wx.LIST_FORMAT_LEFT)
        list.InsertColumn(col=9, heading=codes.get('dLogs_temp_in'), format=wx.LIST_FORMAT_LEFT)
        list.InsertColumn(col=10, heading=codes.get('dLogs_temp_out'), format=wx.LIST_FORMAT_LEFT)
        list.InsertColumn(col=11, heading=codes.get('dLogs_status'), format=wx.LIST_FORMAT_LEFT)
        return list

  