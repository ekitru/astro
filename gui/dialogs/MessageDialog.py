import wx

__author__ = 'kitru'

class MessageDialog(wx.Dialog):
    def __init__(self, parent, id, controller):
        codes = controller.getResources().getCodes()
        wx.Dialog.__init__(self, parent, id, codes.get('dMsg_title'), style=wx.CAPTION | wx.YES_NO | wx.YES_DEFAULT)

        self.message = controller.getResources().getMessageHolder()
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.text = wx.TextCtrl(self, size=(250, 70), style=wx.MULTIPLE)
        self.text.SetValue(self.message.getLastMsg())
        self.text.SetFocus()
        sizer.Add(self.text, flag=wx.LEFT | wx.RIGHT | wx.TOP | wx.EXPAND, border=10)

        buttons = wx.GridSizer(1, 2, 10, 10)
        buttons.Add(wx.Button(self, wx.ID_OK, label=codes.get('dMsg_select')), flag=wx.ALL | wx.ALIGN_LEFT)
        buttons.Add(wx.Button(self, wx.ID_CANCEL, label=codes.get('dMsg_cancel')), flag=wx.ALL | wx.ALIGN_RIGHT)
        sizer.Add(buttons, flag=wx.ALL | wx.EXPAND, border=10)

        self.SetSizer(sizer)
        self.Fit()

        self.Bind(wx.EVT_BUTTON, self.OnSelect, id=wx.ID_OK)


    def OnSelect(self, event):
        event.Skip()
        text = self.text.GetValue()
        last = self.message.getLastMsg()
        if  last != text:
            self.message.setNew(text)
        self.EndModal(wx.ID_OK)

  