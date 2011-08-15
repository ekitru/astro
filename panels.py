import wx

__author__ = 'kitru'

class SimplePanel(wx.Panel):
    def __init__(self, parent=None, ID=wx.ID_ANY):
        wx.Panel.__init__(self, parent, ID)

    def CreateHeader(self, name):
        return self.CreateElement(name, wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))

    def CreateCaption(self, name):
        return self.CreateElement(name)

    def CreateField(self):
        return self.CreateElement()

    def CreateElement(self, name="", font=None):
        element = wx.StaticText(self, wx.ID_ANY, name)
        if font:
            element.SetFont(font)
        return element

    def addKeyValuePair(self, layout, key="", value="", keyFlag=None, valueFlag=None, keyFont=None, valueFont=None):
        keyField = self.addElement(layout, key, flag=keyFlag, font=keyFont)
        valueField = self.addElement(layout, value, flag=valueFlag, font=valueFont)
        return keyField, valueField

    def addElement(self, layout, caption="", flag=None, font=None):
        element = wx.StaticText(self, wx.ID_ANY, caption)
        if font:
            element.SetFont(font)
        if flag is None:
            flag = wx.ALL | wx.EXPAND | wx.CENTER
        layout.Add(element, 0, flag)
        return element


class ObjectPanel(SimplePanel):
    """This panel represents selected object data (name and positions)
    Attributes:
        codes - Translation codes
    """

    def __init__(self, parent, ID=wx.ID_ANY, codes=None):
        SimplePanel.__init__(self, parent, ID)

        sizer = wx.FlexGridSizer(4, 4, 5, 20)

        caption, self.objectName = self.addKeyValuePair(sizer, key=codes.get("Object"),
                                                        keyFont=wx.Font(11, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.addKeyValuePair(sizer)
        self.addKeyValuePair(sizer, value=codes.get('absoluteRADEC'), valueFont=wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD)
                             ,
                             valueFlag=wx.ALL | wx.ALIGN_RIGHT)
        self.addKeyValuePair(sizer, value=codes.get('currentRADEC'), valueFont=wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD),
                             valueFlag=wx.ALL | wx.ALIGN_RIGHT)
        caption, self.objectOrigRA = self.addKeyValuePair(sizer, key=codes.get("objectRA"),
                                                          keyFlag=wx.ALL | wx.ALIGN_RIGHT)
        caption, self.objectCurrRA = self.addKeyValuePair(sizer, key=codes.get("objectRA"),
                                                          keyFlag=wx.ALL | wx.ALIGN_RIGHT)
        caption, self.objectOrigDEC = self.addKeyValuePair(sizer, key=codes.get("objectDEC"),
                                                           keyFlag=wx.ALL | wx.ALIGN_RIGHT)
        caption, self.objectCurrDEC = self.addKeyValuePair(sizer, key=codes.get("objectDEC"),
                                                           keyFlag=wx.ALL | wx.ALIGN_RIGHT)

        sizer.Add(self.CreateHeader(codes.get("Object")))
        sizer.Add(self.CreateField())
        sizer.Add(self.CreateField())



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
        caption, self.objectName = self.addKeyValuePair(sizer, key=codes.get("Positioning"),
                                                        keyFont=wx.Font(11, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.addKeyValuePair(sizer, keyFont=wx.Font(11, wx.SWISS, wx.NORMAL, wx.BOLD)) # dummy line

        self.SetSizer(sizer)

    def update(self):
        pass


