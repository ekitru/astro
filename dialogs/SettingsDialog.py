import wx
from panels.SimplePanel import SimplePanel

__author__ = 'kitru'

class SettingsDialog(wx.Dialog):
    def __init__(self, parent, id, codes, controller):
        wx.Dialog.__init__(self, parent, id, codes.get('dSet_title'), size=(300,300)) #, style=wx.CAPTION | wx.YES_NO | wx.YES_DEFAULT)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(SettingsNoteBook(self, codes, controller), flag=wx.ALL | wx.EXPAND, border=10)
        self.SetSizer(sizer)

class CommonTab(SimplePanel):
   def __init__(self, parent, codes, controller):
       SimplePanel.__init__(self, parent, id=wx.ID_ANY)
       self.config = controller.getConfig()

       sizer = wx.FlexGridSizer(2,2,5,5)
       sizer.Add(self.CreateCaption(codes.get('tCommon_lang')), flag = wx.ALL | wx.ALIGN_RIGHT)

       self.SetSizer(sizer)





class SettingsNoteBook(wx.Notebook):
    def __init__(self, parent, codes, controller):
        wx.Notebook.__init__(self, parent, id=wx.ID_ANY, style=wx.BK_DEFAULT)
        commonTab = CommonTab(self, codes, controller)
        self.AddPage(commonTab, codes.get("tCommon_title"))