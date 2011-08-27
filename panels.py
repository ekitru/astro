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

        sizer = wx.GridSizer(4, 3, 5, 10)

        self.objectName = self.CreateField()
        self.objectOrigRA = self.CreateField()
        self.objectCurrRA = self.CreateField()
        self.objectOrigDEC = self.CreateField()
        self.objectCurrDEC = self.CreateField()
        self.moveBut = wx.Button(self, wx.ID_ANY, codes.get('moveToObj'))

        sizer.Add(self.CreateCaption(codes.get('starName')), flag=wx.ALL | wx.ALIGN_RIGHT)
        sizer.Add(self.objectName, flag=wx.ALL | wx.EXPAND | wx.CENTER)
        sizer.Add(self.CreateField())

        sizer.Add(self.CreateField())
        sizer.Add(self.CreateCaption(codes.get('absoluteRADEC')), flag=wx.ALL | wx.ALIGN_CENTER_HORIZONTAL)
        sizer.Add(self.CreateCaption(codes.get('currentRADEC')), flag=wx.ALL | wx.ALIGN_CENTER_HORIZONTAL)

        sizer.Add(self.CreateCaption(codes.get('objectRA')), flag=wx.ALL | wx.ALIGN_RIGHT)
        sizer.Add(self.objectOrigRA, flag=wx.ALL | wx.ALIGN_CENTER)
        sizer.Add(self.objectCurrRA, flag=wx.ALL | wx.ALIGN_CENTER)

        sizer.Add(self.CreateCaption(codes.get('objectDEC')), flag=wx.ALL | wx.ALIGN_RIGHT)
        sizer.Add(self.objectOrigDEC, flag=wx.ALL | wx.ALIGN_CENTER)
        sizer.Add(self.objectCurrDEC, flag=wx.ALL | wx.ALIGN_CENTER)

        vert = wx.StaticBoxSizer(wx.StaticBox(self, label=codes.get("Object")), wx.VERTICAL)
        vert.Add(sizer, flag=wx.ALL, border=10)
        vert.Add(self.moveBut, flag=wx.ALIGN_RIGHT)

        self.SetSizer(vert)

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

        sizer = wx.GridSizer(4, 2, 5, 10)

        self.LT = self.CreateField()
        self.UTC = self.CreateField()
        self.JD = self.CreateField()
        self.LST = self.CreateField()

        sizer.Add(self.CreateCaption(codes.get('LT')), flag=wx.ALL | wx.ALIGN_RIGHT)
        sizer.Add(self.LT, flag=wx.ALL | wx.CENTER)
        sizer.Add(self.CreateCaption(codes.get('UTC')), flag=wx.ALL | wx.ALIGN_RIGHT)
        sizer.Add(self.UTC, flag=wx.ALL | wx.CENTER)
        sizer.Add(self.CreateCaption(codes.get('JD')), flag=wx.ALL | wx.ALIGN_RIGHT)
        sizer.Add(self.JD, flag=wx.ALL | wx.CENTER)
        sizer.Add(self.CreateCaption(codes.get('LST')), flag=wx.ALL | wx.ALIGN_RIGHT)
        sizer.Add(self.LST, flag=wx.ALL | wx.CENTER)

        vert = wx.StaticBoxSizer(wx.StaticBox(self, label=codes.get('TimeDate')), wx.VERTICAL)
        vert.Add(sizer, flag=wx.ALL, border=10)
        self.SetSizer(vert)

    def update(self, times):
        """Updates local time, sidereal time, julian day and UTC time
        Attributes:
            tuple(LT, UTC, JD, LST)
        """
        self.LT.SetLabel(times[0])
        self.UTC.SetLabel(times[1])
        self.JD.SetLabel(times[2])
        self.LST.SetLabel(times[3])


class PositioningPanel(SimplePanel):
    """This panel represents telescope position with manual positioning opportunities
    Attributes:
        codes - Translation codes
    """

    def __init__(self, parent, ID=wx.ID_ANY, codes=None):
        SimplePanel.__init__(self, parent, ID)

        sizer = wx.GridSizer(4, 3, 5, 10)

        self.curRA = self.CreateField()
        self.taskRA = self.CreateField()
        self.curDEC = self.CreateField()
        self.taskDEC = self.CreateField()
        self.curFocus = self.CreateField()
        self.taskFocus = self.CreateField()
        self.control = wx.Button(self, wx.ID_ANY, codes.get('takeCtrl'))

        sizer.Add(self.CreateField())
        sizer.Add(self.CreateCaption(codes.get('pos_cur')), flag=wx.ALL | wx.ALIGN_CENTER_HORIZONTAL)
        sizer.Add(self.CreateCaption(codes.get('pos_task')), flag=wx.ALL | wx.ALIGN_CENTER_HORIZONTAL)

        sizer.Add(self.CreateCaption(codes.get('posRA')), flag=wx.ALL | wx.ALIGN_RIGHT)
        sizer.Add(self.curRA, flag=wx.ALL | wx.ALIGN_CENTER)
        sizer.Add(self.taskRA, flag=wx.ALL | wx.ALIGN_CENTER)

        sizer.Add(self.CreateCaption(codes.get('posDEC')), flag=wx.ALL | wx.ALIGN_RIGHT)
        sizer.Add(self.curDEC, flag=wx.ALL | wx.ALIGN_CENTER)
        sizer.Add(self.taskDEC, flag=wx.ALL | wx.ALIGN_CENTER)

        sizer.Add(self.CreateCaption(codes.get('posFocus')), flag=wx.ALL | wx.ALIGN_RIGHT)
        sizer.Add(self.curFocus, flag=wx.ALL | wx.ALIGN_CENTER)
        sizer.Add(self.taskFocus, flag=wx.ALL | wx.ALIGN_CENTER)

        vert = wx.StaticBoxSizer(wx.StaticBox(self, label=codes.get('positioning')), wx.VERTICAL)
        vert.Add(sizer, flag=wx.ALL, border=10)
        vert.Add(self.control, flag=wx.ALIGN_RIGHT)

        self.SetSizer(vert)

    def update(self, curPos, curFocus, aimPos, aimFocus):

        self.curRA.SetLabel(curPos[0])
        self.curDEC.SetLabel(curPos[1])
        self.curFocus.SetLabel(curFocus)

        self.taskRA.SetLabel(aimPos[0])
        self.taskDEC.SetLabel(aimPos[1])
        self.taskFocus.SetLabel(aimFocus)


class TelescopePanel(SimplePanel):    #TODO decide, what to do with it, temp mock
    def __init__(self, parent, ID=wx.ID_ANY, codes=None):
        SimplePanel.__init__(self, parent, ID)
        sizer = wx.GridSizer(4, 2, 5, 10)

        sizer.Add(self.CreateCaption("Temp in tube"), flag=wx.ALL | wx.ALIGN_RIGHT)
        sizer.Add(self.CreateCaption("25.2"), flag=wx.ALL | wx.CENTER)
        sizer.Add(self.CreateCaption("Temp under tube"), flag=wx.ALL | wx.ALIGN_RIGHT)
        sizer.Add(self.CreateCaption("21.2"), flag=wx.ALL | wx.CENTER)
        sizer.Add(self.CreateCaption("chair pos"), flag=wx.ALL | wx.ALIGN_RIGHT)
        sizer.Add(self.CreateCaption("home"), flag=wx.ALL | wx.CENTER)
        sizer.Add(self.CreateCaption("Kupol"), flag=wx.ALL | wx.ALIGN_RIGHT)
        sizer.Add(self.CreateCaption("somewhere"), flag=wx.ALL | wx.CENTER)

        vert = wx.StaticBoxSizer(wx.StaticBox(self, label='Telescope'), wx.VERTICAL)
        vert.Add(sizer, flag=wx.ALL, border=10)
        self.SetSizer(vert)




