import codecs
import os
from posixpath import join
import wx
import sys
import datetime
import time
from db.AlarmLog import AlarmLog
from gui.panels.SimplePanel import SimplePanel

__author__ = 'kitru'

class AlarmLogDialog(wx.Dialog, SimplePanel):
    ONE_DAY = 24 * 60 * 60 - 1 #23hour 59 minutes 59 seconds

    def __init__(self, parent, controller):
        resources = controller.resources
        self.codes = controller.codes
        wx.Dialog.__init__(self, parent, title=self.codes.get('dAlarmLogs_title'),
                           style=wx.CAPTION | wx.YES_NO | wx.YES_DEFAULT)

        self._log = AlarmLog(resources.getDbManager())
        self._list = self.CreateLists(self.codes)
        searchPanel = self.CreateSearchPanel(self.codes)

        buttons = wx.BoxSizer(wx.HORIZONTAL)
        buttons.Add(wx.Button(self, wx.ID_FILE, label=self.codes.get('dAlarmLogs_export')), flag=wx.RIGHT, border=10)
        buttons.Add(wx.Button(self, wx.ID_CANCEL, label=self.codes.get('dAlarmLogs_close')))

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
        list.SetMinSize((400, 300))
        list.InsertColumn(col=0, heading=codes.get('dAlarmLogs_code'), format=wx.LIST_FORMAT_LEFT, width=50)
        list.InsertColumn(col=1, heading=codes.get('dAlarmLogs_desc'), format=wx.LIST_FORMAT_LEFT, width=320)
        list.InsertColumn(col=2, heading=codes.get('dAlarmLogs_time'), format=wx.LIST_FORMAT_LEFT, width=180)
        list.InsertColumn(col=3, heading=codes.get('dAlarmLogs_action'), format=wx.LIST_FORMAT_LEFT, width=80)
        return list

    def CreateSearchPanel(self, codes):
        sizer = wx.FlexGridSizer(1, 12, 5, 5)

        self.alarmCode = wx.TextCtrl(self, size=(100, -1))
        self.startDate = wx.DatePickerCtrl(self, dt=wx.DateTime().UNow(), size=(120, -1),
                                           style=wx.DP_DEFAULT | wx.DP_ALLOWNONE | wx.DP_SHOWCENTURY)
        self.endDate = wx.DatePickerCtrl(self, dt=wx.DateTime.UNow(), size=(120, -1),
                                         style=wx.DP_DEFAULT | wx.DP_ALLOWNONE | wx.DP_SHOWCENTURY)

        sizer.Add(self.CreateCaption(codes.get('dAlarmLogs_code')), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        sizer.Add(self.alarmCode)
        sizer.AddSpacer((20, -1))
        sizer.Add(self.CreateCaption(codes.get('dAlarmLogs_from')), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        sizer.Add(self.startDate)
        sizer.AddSpacer((20, -1))
        sizer.Add(self.CreateCaption(codes.get('dAlarmLogs_to')), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        sizer.Add(self.endDate)
        sizer.AddSpacer((20, -1))
        sizer.Add(wx.Button(self, wx.ID_FIND, label=codes.get('dAlarmLogs_find')), proportion=2,
                  flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        return sizer

    def FillList(self, logs):
        self._list.DeleteAllItems()
        for log in logs:
            alarm = self.parseAlarm(log['code'])
            index = self._list.InsertStringItem(sys.maxint, str(log['code']))
            self._list.SetStringItem(index, 1, str(alarm))
            self._list.SetStringItem(index, 2, str(log['time']))
            action = self.parseAction(log['action'])
            self._list.SetStringItem(index, 3, str(action))

    def parseAlarm(self, alarm):
        return self.codes.get('al'+str(alarm))

    def parseAction(self, act):
        if act:
            return self.codes.get('dAlarmLogs_on')
        else:
            return self.codes.get('dAlarmLogs_off')

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
        code = self.alarmCode.GetValue()
        startDate, endDate = self.getPeriod()
        logs = self._log.readLog(code, startDate, endDate)
        self.FillList(logs)

    def OnCancel(self, event):
        event.Skip()
        self.EndModal(wx.ID_CANCEL)

    def OnExport(self, event):
        event.Skip()
        path = join(os.getenv('HOME'), 'Desktop')
        dialog = wx.FileDialog(self, message="File select", defaultDir=path, defaultFile="alarmHistory.log",
                               style=wx.SAVE | wx.OVERWRITE_PROMPT)
        if dialog.ShowModal() == wx.ID_OK:
            # Open the file for write, write, close
            self.filename = dialog.GetFilename()
            self.dirname = dialog.GetDirectory()
            filehandle = codecs.open(os.path.join(self.dirname, self.filename), 'w', 'utf-8')
            for data in self._log._log:
                line = self.parseDict(data)
                filehandle.write(';'.join(line))
                filehandle.write('\n')
            filehandle.close()
        dialog.Destroy()

    def parseDict(self, log):
        print(log)
        line = []
        line.append(str(log['id']))
        line.append(str(log['code']))
        line.append(str(log['time']))
        line.append(str(log['action']))
        return line
