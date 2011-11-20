import os
from posixpath import join
import wx
import sys
import datetime
import time
from db import Log
from gui.panels.SimplePanel import SimplePanel

__author__ = 'kitru'

class LogsDialog(wx.Dialog, SimplePanel):
    ONE_DAY = 24 * 60 * 60 - 1 #23hour 59 minutes 59 seconds

    def __init__(self, parent, id, controller):
        resources = controller.resources
        codes = resources.codes
        wx.Dialog.__init__(self, parent, title=codes.get('dLogs_title'),
                           style=wx.CAPTION | wx.YES_NO | wx.YES_DEFAULT)

        self._log = Log(resources.getDbManager())
        self._list = self.CreateLists(codes)
        searchPanel = self.CreateSearchPanel(codes)

        buttons = wx.BoxSizer(wx.HORIZONTAL)
        buttons.Add(wx.Button(self, wx.ID_FILE, label=codes.get('dLogs_export')), flag=wx.RIGHT, border=10)
        buttons.Add(wx.Button(self, wx.ID_CANCEL, label=codes.get('dLogs_close')))

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(searchPanel, flag=wx.ALL | wx.EXPAND, border=10)
        sizer.Add(self._list, flag=wx.EXPAND)
        sizer.Add(buttons, flag=wx.ALL, border=10)

        self.SetFocus()
        self.SetSizer(sizer)
        self.Fit()

        self.Bind(wx.EVT_BUTTON, self.OnFind, id=wx.ID_FIND)
        self.Bind(wx.EVT_BUTTON, self.OnCancel, id=wx.ID_CANCEL)
        self.Bind(wx.EVT_BUTTON, self.OnExport, id=wx.ID_FILE)
        self.Bind(wx.EVT_KEY_UP, self.OnListCharacter)

    def CreateLists(self, codes):
        list = wx.ListCtrl(self, id=wx.ID_ANY, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        list.SetMinSize((1400, 300))
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
        list.InsertColumn(col=11, heading=codes.get('dLogs_status'), format=wx.LIST_FORMAT_LEFT, width=800)
        return list

    def CreateSearchPanel(self, codes):
        sizer = wx.FlexGridSizer(1, 12, 5, 5)

        self.name = wx.TextCtrl(self, size=(120, -1))
        self.startDate = wx.DatePickerCtrl(self, dt=wx.DateTime().UNow(), size=(120, -1),
                                           style=wx.DP_DEFAULT | wx.DP_ALLOWNONE | wx.DP_SHOWCENTURY)
        self.endDate = wx.DatePickerCtrl(self, dt=wx.DateTime.UNow(), size=(120, -1),
                                         style=wx.DP_DEFAULT | wx.DP_ALLOWNONE | wx.DP_SHOWCENTURY)

        sizer.Add(self.CreateCaption(codes.get('dLogs_name')), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        sizer.Add(self.name)
        sizer.AddSpacer((40, -1))
        sizer.Add(self.CreateCaption(codes.get('dLogs_from')), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        sizer.Add(self.startDate)
        sizer.AddSpacer((40, -1))
        sizer.Add(self.CreateCaption(codes.get('dLogs_to')), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        sizer.Add(self.endDate)
        sizer.AddSpacer((20, -1))
        sizer.Add(wx.Button(self, wx.ID_FIND, label=codes.get('dLogs_find')), proportion=2,
                  flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        return sizer

    def FillList(self, logs):
        self._list.DeleteAllItems()
        for log in logs:
            index = self._list.InsertStringItem(sys.maxint, str(log['id']))
            self._list.SetStringItem(index, 1, str(log['time']))
            self._list.SetStringItem(index, 2, unicode(log['name']))
            self._list.SetStringItem(index, 3, str(log['sRa']))
            self._list.SetStringItem(index, 4, str(log['sDec']))
            self._list.SetStringItem(index, 5, unicode(log['msg']))
            self._list.SetStringItem(index, 6, str(log['ra']))
            self._list.SetStringItem(index, 7, str(log['dec']))
            self._list.SetStringItem(index, 8, str(log['focus']))
            self._list.SetStringItem(index, 9, str(log['temp_in']))
            self._list.SetStringItem(index, 10, str(log['temp_out']))
            self._list.SetStringItem(index, 11, str(log['status']))

    def getStartDay(self, dateTime):
        """ Return first second of the day """
        return self.getUnixTimeStamp(dateTime)


    def getEndDay(self, dateTime):
        """ Return last second of the day """
        return self.getUnixTimeStamp(dateTime) + self.ONE_DAY

    def getUnixTimeStamp(self, dateTime):
        day, month, year = dateTime.GetDay(), dateTime.GetMonth() + 1, dateTime.GetYear()
        date = datetime.date(year, month, day)
        return time.mktime(date.timetuple())


    def OnFind(self, event):
        event.Skip()
        self.findInLog()


    def OnListCharacter (self, event):
        event.Skip()
        if event.GetKeyCode() == wx.WXK_RETURN:
            self.findInLog()

    def getPeriod(self):
        start = self.startDate.GetValue()
        end = self.endDate.GetValue()
        startDate = self.getStartDay(start)
        endDate = self.getEndDay(end)
        return startDate, endDate

    def findInLog(self):
        name = self.name.GetValue()
        startDate, endDate = self.getPeriod()
        logs = self._log.readLog(name, startDate, endDate)
        self.FillList(logs)

    def OnCancel(self, event):
        event.Skip()
        self.EndModal(wx.ID_CANCEL)

    def OnExport(self, event):
        event.Skip()
        path = join(os.getenv('HOME'), 'Desktop')
        dialog = wx.FileDialog(self, message="File select", defaultDir=path, defaultFile="temp.log",
                               style=wx.SAVE | wx.OVERWRITE_PROMPT)
        if dialog.ShowModal() == wx.ID_OK:
            # Open the file for write, write, close
            self.filename = dialog.GetFilename()
            self.dirname = dialog.GetDirectory()
            filehandle = open(os.path.join(self.dirname, self.filename), 'w')
            for data in self._log._log:
                line = self.parseDict(data)
                filehandle.write(';'.join(line))
                filehandle.write('\n')
            filehandle.close()
        dialog.Destroy()

    def parseDict(self, log):
        line = []
        line.append(str(log['id']))
        line.append(str(log['time']))
        line.append(unicode(log['name']))
        line.append(str(log['sRa']))
        line.append(str(log['sDec']))
        line.append(unicode(log['msg']))
        line.append(str(log['ra']))
        line.append(str(log['dec']))
        line.append(str(log['focus']))
        line.append(str(log['temp_in']))
        line.append(str(log['temp_out']))
        line.append(str(log['status']))
        return line
