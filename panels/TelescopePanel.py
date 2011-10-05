import wx
from panels.SimplePanel import SimplePanel

__author__ = 'kitru'


class TelescopePanel(SimplePanel):    #TODO decide, what to do with it, temp mock
    def __init__(self, parent, id=wx.ID_ANY, codes=None):
        SimplePanel.__init__(self, parent, id)
        sizer = wx.GridSizer(4, 2, 5, 10)

        sizer.Add(self.CreateCaption(codes.get("Temp in tube")), flag=wx.ALL | wx.ALIGN_RIGHT)
        sizer.Add(self.CreateCaption("25.2"), flag=wx.ALL | wx.CENTER)
        sizer.Add(self.CreateCaption("Temp under tube"), flag=wx.ALL | wx.ALIGN_RIGHT)
        sizer.Add(self.CreateCaption("21.2"), flag=wx.ALL | wx.CENTER)
        sizer.Add(self.CreateCaption("chair pos"), flag=wx.ALL | wx.ALIGN_RIGHT)
        sizer.Add(self.CreateCaption("home"), flag=wx.ALL | wx.CENTER)
        sizer.Add(self.CreateCaption("Kupol"), flag=wx.ALL | wx.ALIGN_RIGHT)
        sizer.Add(self.CreateCaption("somewhere"), flag=wx.ALL | wx.CENTER)

        comSizer = wx.StaticBoxSizer(wx.StaticBox(self, label='Telescope'), wx.VERTICAL)
        comSizer.Add(sizer, flag=wx.ALL, border=10)
        self.SetSizer(comSizer)

  