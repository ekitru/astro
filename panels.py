import wx

__author__ = 'kitru'

class SimplePanel(wx.Panel):
    def __init__(self, parent=None, ID=wx.ID_ANY):
        wx.Panel.__init__(self, parent, ID)

    def CreateHeader(self, name):
        return self.CreateElement(name, wx.Font(10, wx.SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

    def CreateCaption(self, name):
        return self.CreateElement(name, wx.Font(10, wx.SWISS, wx.FONTSTYLE_SLANT, wx.FONTWEIGHT_LIGHT))

    def CreateField(self):
        return self.CreateElement()

    def CreateElement(self, name="", font=None):
        element = wx.StaticText(self, wx.ID_ANY, name)
        if font:
            element.SetFont(font)
        return element


class ObjectPanel(SimplePanel):
    """This panel represents selected object data (name and positions)
    Attributes:
        codes - Translation codes
    """

    def __init__(self, parent, ID=wx.ID_ANY, codes=None):
        SimplePanel.__init__(self, parent, ID)

        sizer = wx.GridSizer(4, 3, 5, 20)

        self.objectName = self.CreateField()
        self.objectOrigRA = self.CreateField()
        self.objectCurrRA = self.CreateField()
        self.objectOrigDEC = self.CreateField()
        self.objectCurrDEC = self.CreateField()

        sizer.Add(self.CreateHeader(codes.get('Object')))
        sizer.Add(self.objectName, 0, wx.ALL | wx.CENTER | wx.EXPAND)
        sizer.Add(self.CreateField())
        sizer.Add(self.CreateField())
        sizer.Add(self.CreateCaption(codes.get('absoluteRADEC')), 0, wx.ALL | wx.ALIGN_CENTER)
        sizer.Add(self.CreateCaption(codes.get('currentRADEC')), 0, wx.ALL | wx.ALIGN_CENTER)
        sizer.Add(self.CreateCaption(codes.get('objectRA')), 0, wx.ALL | wx.ALIGN_RIGHT)
        sizer.Add(self.objectOrigRA, 0, wx.ALL | wx.ALIGN_CENTER)
        sizer.Add(self.objectCurrRA, 0, wx.ALL | wx.ALIGN_CENTER)
        sizer.Add(self.CreateCaption(codes.get('objectDEC')), 0, wx.ALL | wx.ALIGN_RIGHT)
        sizer.Add(self.objectOrigDEC, 0, wx.ALL | wx.ALIGN_CENTER)
        sizer.Add(self.objectCurrDEC, 0, wx.ALL | wx.ALIGN_CENTER)

        self.SetSizer(sizer)

    def update(self, name, origRADEC, currRADEC):
        """Updates Objects name and coordinates
        Attributes are tuple(RA,DEC) with string types
            origRADEC - Epoch coordinates
            urrRADEC - Current coordinates for observer
        """
        self.objectName.SetLabel(name)
        self.objectOrigRA.SetLabel(origRADEC[0])
        self.objectOrigDEC.SetLabel(origRADEC[1])
        self.objectCurrRA.SetLabel(currRADEC[0])
        self.objectCurrDEC.SetLabel(currRADEC[1])


class TimeDatePanel(SimplePanel):
    """This panel represents current system time and  astronomic times for telescope location.
    Attributes:
        codes - Translation codes
    """

    def __init__(self, parent, ID=wx.ID_ANY, codes=None):
        SimplePanel.__init__(self, parent, ID)

        sizer = wx.GridSizer(5, 2, 0, 20)

        self.LT = self.CreateField()
        self.UTC = self.CreateField()
        self.JD = self.CreateField()
        self.LST = self.CreateField()

        sizer.Add(self.CreateHeader(codes.get("Time & Date")))
        sizer.Add(self.CreateField())

        sizer.Add(self.CreateCaption(codes.get("LT")), 0, wx.ALL | wx.ALIGN_RIGHT)
        sizer.Add(self.LT, 0, wx.ALL | wx.EXPAND | wx.CENTER)
        sizer.Add(self.CreateCaption(codes.get("UTC")), 0, wx.ALL | wx.ALIGN_RIGHT)
        sizer.Add(self.UTC, 0, wx.ALL | wx.EXPAND | wx.CENTER)
        sizer.Add(self.CreateCaption(codes.get("JD")), 0, wx.ALL | wx.ALIGN_RIGHT)
        sizer.Add(self.JD, 0, wx.ALL | wx.EXPAND | wx.CENTER)
        sizer.Add(self.CreateCaption(codes.get("LST")), 0, wx.ALL | wx.ALIGN_RIGHT)
        sizer.Add(self.LST, 0, wx.ALL | wx.EXPAND | wx.CENTER)

        self.SetSizer(sizer)

    def update(self, times):
        """Updates local time, sidereal time, julian day and UTC time
        Attributes:
            tuple(LT, UTC, JD, LST)
        """
        self.LT.SetLabel(times[0])
        self.UTC.SetLabel(times[1])
        self.JD.SetLabel(times[2])
        self.LST.SetLabel(times[3])
        self.Fit()


class PositioningPanel(SimplePanel):
    """This panel represents telescope position with manual positioning opportunities
    Attributes:
        codes - Translation codes
    """

    def __init__(self, parent, ID=wx.ID_ANY, codes=None):
        SimplePanel.__init__(self, parent, ID)

        sizer = wx.FlexGridSizer(4, 4, 5, 20)
        sizer.Add(self.CreateHeader('Positioning'))

        self.SetSizer(sizer)

    def update(self):
        pass


