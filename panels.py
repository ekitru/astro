import wx

__author__ = 'kitru'

class TimeDatePanel(wx.Panel):
    def __init__(self, parent, ID=wx.ID_ANY, pos=wx.DefaultPosition, size=(200, 200), codes=None):
        wx.Panel.__init__(self, parent, ID, pos, size)

        layout = wx.FlexGridSizer(5, 2, 0, 20)
        self.addLine(layout, codes.get("Time & Date"), wx.Font(11, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.LT = self.addLine(layout, codes.get("Local Time"))
        self.UTC = self.addLine(layout, codes.get("UTC"))
        self.JD = self.addLine(layout, codes.get("Julian day"))
        self.LST = self.addLine(layout, codes.get("Local sidereal time"))

        self.SetSizer(layout)
        self.Fit()

    def addLine(self, layout, name, font=None):
        keyField = wx.StaticText(self, wx.ID_ANY, name)
        if font:
            keyField.SetFont(font)
        element = wx.StaticText(self, wx.ID_ANY, "                                              ")
        layout.Add(keyField, 0, flag=wx.ALL | wx.ALIGN_RIGHT)
        layout.Add(element)
        return element

    def updateTimeDate(self, mechanics):
        """ Updates local time, sidereal time, julian day and UTC time
        Attributes:
           mechanics - AstroMechanics class instance
        """
        lt, utc, jd, lst = mechanics.getCurrentTimeDate()
        self.LT.SetLabel(lt)
        self.UTC.SetLabel(utc)
        self.JD.SetLabel(jd)
        self.LST.SetLabel(lst)
        self.Fit()
