import wx
from core.config.ProgramConfig import ProgramConfig
from gui.panels.SimplePanel import SimplePanel

__author__ = 'kitru'

class SettingsDialog(wx.Dialog, SimplePanel):
    """ Very simple dialog to set up logging time and select languages """

    def __init__(self, parent, codes, controller):
        wx.Dialog.__init__(self, parent, title=codes.get('dSet_title'),
                           style=wx.CAPTION | wx.YES_NO | wx.YES_DEFAULT)

        self._controller = controller
        self._config = self.getConfig()

        commonDict = self._config.getCommonConfigDict()

        self._langBox = self.CreateLangBox(commonDict)
        self._logTime = self.CreateLogTime(commonDict)

        controls = wx.FlexGridSizer(2, 2, 5, 10)
        controls.Add(self.CreateCaption(codes.get('dSet_lang')), flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        controls.Add(self._langBox, flag=wx.ALL | wx.EXPAND | wx.CENTER)
        controls.Add(self.CreateCaption(codes.get('dSet_logtime')), flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        controls.Add(self._logTime, flag=wx.ALL | wx.EXPAND | wx.CENTER)

        buttons = wx.FlexGridSizer(1, 2, 5, 10)
        buttons.Add(wx.Button(self, wx.ID_APPLY, label=codes.get('dSet_apply')), flag=wx.ALIGN_LEFT | wx.ALIGN_BOTTOM)
        buttons.Add(wx.Button(self, wx.ID_CANCEL, label=codes.get('dSet_cancel')), flag=wx.ALIGN_LEFT | wx.ALIGN_BOTTOM)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(controls, flag=wx.ALL, border = 10)
        sizer.Add(buttons, flag = wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10)
        self.SetSizer(sizer)
        self.SetFocus()
        self.Fit()

        self.Bind(wx.EVT_BUTTON, self.OnApplyClicked, id=wx.ID_APPLY)

    def CreateLangBox(self, commonDict):
        langs = commonDict.get('translations').split(',')
        curLang = commonDict.get('default translation')
        comboBox = wx.ComboBox(self, size=(50, -1), choices=langs, style=wx.CB_READONLY)
        langIndex = (id for id, value in enumerate(langs) if value == curLang).next()
        comboBox.Select(langIndex)
        return comboBox


    def CreateLogTime(self, commonDict):
        oldPeriod = commonDict.get('logging time')
        logTime = self.CreateInputField()
        logTime.SetWindowStyleFlag(wx.TE_RIGHT)
        logTime.SetValue(str(oldPeriod))
        return logTime

    def getConfig(self):
        config = ProgramConfig()
        config.readConfiguration('default')
        return config

    def OnApplyClicked(self, event):
        event.Skip()
        time = self._logTime.GetValue()
        time = self.checkLimits(time)
        lang = self._langBox.GetValue()
        lang = lang.strip()

        self._config.setDefaultLanguage(lang)
        self._config.setLoggingTime(time)
        self._controller.updateLogTime(time)
        self._config.saveConfig()
        self.EndModal(wx.ID_OK)

    def checkLimits(self, time):
        if not time.isnumeric():
            return 1
        elif  int(time) > 30:
            return 30
        elif int(time) < 1:
            return 1
        else:
            return time
