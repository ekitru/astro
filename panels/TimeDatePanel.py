import wx
from panels.SimplePanel import SimplePanel

__author__ = 'kitru'

class TimeDatePanel(SimplePanel):
    """This panel represents current system time and  astronomic times for telescope location.
    Attributes:
        codes - Translation codes
    """

    def __init__(self, parent, ID=wx.ID_ANY, codes=None):
        SimplePanel.__init__(self, parent, ID)

        sizer = wx.GridSizer(4, 2, 5, 10)

        self.LT = self.CreateField()
        self.UTC = self.CreateField()
        self.JD = self.CreateField()
        self.LST = self.CreateField()

        sizer.Add(self.CreateCaption(codes.get('pTimeLT')), flag=wx.ALL | wx.ALIGN_RIGHT)
        sizer.Add(self.LT, flag=wx.ALL | wx.CENTER)
        sizer.Add(self.CreateCaption(codes.get('pTimeUTC')), flag=wx.ALL | wx.ALIGN_RIGHT)
        sizer.Add(self.UTC, flag=wx.ALL | wx.CENTER)
        sizer.Add(self.CreateCaption(codes.get('pTimeJD')), flag=wx.ALL | wx.ALIGN_RIGHT)
        sizer.Add(self.JD, flag=wx.ALL | wx.CENTER)
        sizer.Add(self.CreateCaption(codes.get('pTimeLST')), flag=wx.ALL | wx.ALIGN_RIGHT)
        sizer.Add(self.LST, flag=wx.ALL | wx.CENTER)

        comSizer = wx.StaticBoxSizer(wx.StaticBox(self, label=codes.get('pTime')), wx.VERTICAL)
        comSizer.Add(sizer, flag=wx.ALL, border=10)
        self.SetSizer(comSizer)

    def update(self, controller):
        """Updates local time, sidereal time, julian day and UTC time """
        times = controller.observer.getCurrentTimes()
        self.LT.SetLabel(times[0])
        self.UTC.SetLabel(times[1])
        self.JD.SetLabel(times[2])
        self.LST.SetLabel(times[3])
  