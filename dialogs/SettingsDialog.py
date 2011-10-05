import wx
from panels.SimplePanel import SimplePanel

__author__ = 'kitru'

class SettingsDialog(wx.Dialog):
    def __init__(self, parent, id, codes, controller):
        wx.Dialog.__init__(self, parent, id, codes.get('dSet_title'), size=(300, 300)) #, style=wx.CAPTION | wx.YES_NO | wx.YES_DEFAULT)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(SettingsNoteBook(self, codes, controller), flag=wx.ALL | wx.EXPAND, border=1)
        sizer.Add(wx.Button(self, wx.ID_CANCEL, label=codes.get('dSet_cancel')), flag=wx.ALL | wx.ALIGN_RIGHT)
        self.SetFocus()
        self.SetSizer(sizer)


class SettingsNoteBook(wx.Notebook):
    def __init__(self, parent, codes, controller):
        wx.Notebook.__init__(self, parent, id=wx.ID_ANY, style=wx.BK_DEFAULT)
        commonTab = CommonTab(self, codes, controller)
        self.AddPage(commonTab, codes.get("tCommon_title"))


class CommonTab(SimplePanel):
    def __init__(self, parent, codes, controller):
        SimplePanel.__init__(self, parent, id=wx.ID_ANY)
        self._config = controller.getConfig()

        commonDict = self._config.getCommonConfigDict()

        langs = commonDict.get('translations').split(',')
        curLang = commonDict.get('default translation')
        self._comboBox = wx.ComboBox(self, size=(50, -1), choices=langs, style=wx.CB_READONLY)
        langIndex = (id for id, value in enumerate(langs) if value == curLang).next()
        self._comboBox.Select(langIndex)

        oldPeriod = commonDict.get('logging time')
        self._logTime = self.CreateInputField()
        self._logTime.SetWindowStyleFlag(wx.TE_RIGHT)
        self._logTime.SetValue(str(oldPeriod))

        sizer = wx.FlexGridSizer(2, 2, 5, 10)
        sizer.Add(self.CreateCaption(codes.get('tCommon_lang')), flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        sizer.Add(self._comboBox, flag=wx.ALL | wx.EXPAND | wx.CENTER)
        sizer.Add(self.CreateCaption(codes.get('tCommon_logtime')), flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        sizer.Add(self._logTime, flag=wx.ALL | wx.EXPAND | wx.CENTER)

        canvas = wx.GridSizer(2, 1, 5, 5)
        canvas.Add(sizer, flag=wx.ALL | wx.EXPAND, border=10)
        canvas.Add(wx.Button(self, wx.ID_APPLY, label=codes.get('tCommon_apply')), flag=wx.ALIGN_LEFT | wx.ALIGN_BOTTOM)
        self.SetSizer(canvas)

        self.Bind(wx.EVT_BUTTON, self.OnApplyClicked, id=wx.ID_APPLY)

    def OnApplyClicked(self, event):
        event.Skip()
        time = self._logTime.GetValue()
        time = self.checkLimits(time)
        lang = self._comboBox.GetValue()
        lang = lang.strip()
        print(time, lang)

    def checkLimits(self, time):
        if not time.isnumeric():
            return 1
        elif  int(time) > 30:
            return 30
        elif int(time) < 1:
            return 1
        else:
            return time


