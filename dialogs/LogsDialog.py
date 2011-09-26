import wx
import sys
from astronomy import rad2str
from db import Log
from panels.SimplePanel import SimplePanel

__author__ = 'kitru'

class LogsDialog(wx.Dialog, SimplePanel):
    def __init__(self, parent, id, controller):
        wx.Dialog.__init__(self, parent, id, 'dLogs_title',
                           style=wx.CAPTION | wx.YES_NO | wx.YES_DEFAULT)
        resources = controller.getResourceKeeper()
        codes = resources.getCodes()
        self._log = Log(resources.getDbManager())
        self._list = self.CreateLists(codes)
        searchPanel = self.CreateSearchPanel(codes)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(searchPanel, flag=wx.ALL | wx.EXPAND, border=10)
        sizer.Add(self._list, flag=wx.EXPAND)
        sizer.Add(wx.Button(self, wx.ID_CANCEL, label=codes.get('dLogs_close')), flag=wx.ALL | wx.ALIGN_RIGHT, border =10)

        self.SetSizer(sizer)
        self.Fit()

        self.Bind(wx.EVT_BUTTON, self.OnFind, id=wx.ID_FIND)
        self.Bind(wx.EVT_BUTTON, self.OnCancel, id=wx.ID_CANCEL)

    def CreateLists(self, codes):
        list = wx.ListCtrl(self, id=wx.ID_ANY, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        list.SetMinSize((1200, 300))
        list.InsertColumn(col=0, heading=codes.get('dLogs_ID'), format=wx.LIST_FORMAT_LEFT, width=40)
        list.InsertColumn(col=1, heading=codes.get('dLogs_time'), format=wx.LIST_FORMAT_LEFT, width=200)
        list.InsertColumn(col=2, heading=codes.get('dLogs_star_name'), format=wx.LIST_FORMAT_LEFT, width=120)
        list.InsertColumn(col=3, heading=codes.get('dLogs_star_ra'), format=wx.LIST_FORMAT_LEFT, width=80)
        list.InsertColumn(col=4, heading=codes.get('dLogs_star_dec'), format=wx.LIST_FORMAT_LEFT, width=80)
        list.InsertColumn(col=5, heading=codes.get('dLogs_text'), format=wx.LIST_FORMAT_LEFT, width=200)
        list.InsertColumn(col=6, heading=codes.get('dLogs_ra'), format=wx.LIST_FORMAT_LEFT, width=80)
        list.InsertColumn(col=7, heading=codes.get('dLogs_dec'), format=wx.LIST_FORMAT_LEFT, width=80)
        list.InsertColumn(col=8, heading=codes.get('dLogs_focus'), format=wx.LIST_FORMAT_LEFT)
        list.InsertColumn(col=9, heading=codes.get('dLogs_temp_in'), format=wx.LIST_FORMAT_LEFT)
        list.InsertColumn(col=10, heading=codes.get('dLogs_temp_out'), format=wx.LIST_FORMAT_LEFT)
        list.InsertColumn(col=11, heading=codes.get('dLogs_status'), format=wx.LIST_FORMAT_LEFT)
        return list

    def CreateSearchPanel(self, codes):
        sizer = wx.FlexGridSizer(1, 12, 5, 5)

        self.name = wx.TextCtrl(self, size=(120, -1))
        self.startDate = wx.TextCtrl(self, size=(120, -1))
        self.endDate = wx.TextCtrl(self, size=(120, -1))

        sizer.Add(self.CreateCaption(codes.get('dLogs_name')), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        sizer.Add(self.name)
        sizer.AddSpacer((40,-1))
        sizer.Add(self.CreateCaption(codes.get('dLogs_from')), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        sizer.Add(self.startDate)
        sizer.AddSpacer((40,-1))
        sizer.Add(self.CreateCaption(codes.get('dLogs_to')), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        sizer.Add(self.endDate)
        sizer.AddSpacer((20,-1))
        sizer.Add(wx.Button(self, wx.ID_FIND, label=codes.get('dLogs_find')), proportion=2,
                  flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)

        return sizer


    def FillList(self, logs):
        self._list.DeleteAllItems()
        for log in logs:
            index = self._list.InsertStringItem(sys.maxint, str(log['id']) )
            self._list.SetStringItem(index, 1, str(log['time']))
            self._list.SetStringItem(index, 2, str(log['name']))
            self._list.SetStringItem(index, 3, str(log['sRa']))
            self._list.SetStringItem(index, 4, str(log['sDec']))
            self._list.SetStringItem(index, 5, str(log['msg']))
            self._list.SetStringItem(index, 6, str(log['ra']))
            self._list.SetStringItem(index, 7, str(log['dec']))
            self._list.SetStringItem(index, 8, str(log['temp_in']))
            self._list.SetStringItem(index, 9, str(log['temp_out']))
            self._list.SetStringItem(index, 10, str(log['status']))

    def OnFind(self, event):
        name = self.name.GetValue();
        start = self.startDate.GetValue();
        end= self.endDate.GetValue();
        logs = self._log.readLog(starName=name, startDate=start, endDate=end)
        self.FillList(logs)

    def OnCancel(self, event):
       self.EndModal(wx.ID_CANCEL)



  