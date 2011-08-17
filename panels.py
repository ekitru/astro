import wx
import ephem

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
        self.moveBut = wx.Button(self, wx.ID_ANY, "Move to object")

        sizer.Add(self.CreateHeader(codes.get('Object')))
        sizer.Add(self.objectName, flag=wx.ALL | wx.CENTER)
        sizer.Add(self.CreateField())

        sizer.Add(self.CreateField())
        sizer.Add(self.CreateCaption(codes.get('absoluteRADEC')), flag=wx.ALL | wx.ALIGN_CENTER)
        sizer.Add(self.CreateCaption(codes.get('currentRADEC')), flag=wx.ALL | wx.ALIGN_CENTER)

        sizer.Add(self.CreateCaption(codes.get('objectRA')), flag=wx.ALL | wx.ALIGN_RIGHT)
        sizer.Add(self.objectOrigRA, flag=wx.ALL | wx.ALIGN_CENTER)
        sizer.Add(self.objectCurrRA, flag=wx.ALL | wx.ALIGN_CENTER)

        sizer.Add(self.CreateCaption(codes.get('objectDEC')), flag=wx.ALL | wx.ALIGN_RIGHT)
        sizer.Add(self.objectOrigDEC, flag=wx.ALL | wx.ALIGN_CENTER)
        sizer.Add(self.objectCurrDEC, flag=wx.ALL | wx.ALIGN_CENTER)

        vert = wx.BoxSizer(wx.VERTICAL)
        vert.Add(sizer)
        vert.Add(self.moveBut, flag=wx.ALIGN_CENTER_HORIZONTAL)

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

        sizer = wx.GridSizer(5, 2, 5, 10)

        self.LT = self.CreateField()
        self.UTC = self.CreateField()
        self.JD = self.CreateField()
        self.LST = self.CreateField()

        sizer.Add(self.CreateHeader(codes.get("Time & Date")))
        sizer.Add(self.CreateField())

        sizer.Add(self.CreateCaption(codes.get("LT")), flag=wx.ALL | wx.ALIGN_RIGHT)
        sizer.Add(self.LT, flag=wx.ALL | wx.CENTER)
        sizer.Add(self.CreateCaption(codes.get("UTC")), flag=wx.ALL | wx.ALIGN_RIGHT)
        sizer.Add(self.UTC, flag=wx.ALL | wx.CENTER)
        sizer.Add(self.CreateCaption(codes.get("JD")), flag=wx.ALL | wx.ALIGN_RIGHT)
        sizer.Add(self.JD, flag=wx.ALL | wx.CENTER)
        sizer.Add(self.CreateCaption(codes.get("LST")), flag=wx.ALL | wx.ALIGN_RIGHT)
        sizer.Add(self.LST, flag=wx.ALL | wx.CENTER)

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


class PositioningPanel(SimplePanel):
    def __init__(self, parent, ID=wx.ID_ANY, codes=None):
        SimplePanel.__init__(self, parent, ID)

        sizer = wx.GridSizer(5, 3, 5, 10)

        self.curRA = self.CreateField()
        self.taskRA = self.CreateField()
        self.curDEC = self.CreateField()
        self.taskDEC = self.CreateField()
        self.curFocus = self.CreateField()
        self.taskFocus = self.CreateField()

        self.control = wx.Button(self, wx.ID_ANY, "Take control")

        sizer.Add(self.CreateHeader(codes.get('Positioning')))
        sizer.Add(self.CreateCaption(' '), flag=wx.ALL | wx.CENTER)
        sizer.Add(self.CreateField())

        sizer.Add(self.CreateField())
        sizer.Add(self.CreateCaption(codes.get('pos_cur')), flag=wx.ALL | wx.ALIGN_CENTER)
        sizer.Add(self.CreateCaption(codes.get('pos_task')), flag=wx.ALL | wx.ALIGN_CENTER)

        sizer.Add(self.CreateCaption(codes.get('posRA')), flag=wx.ALL | wx.ALIGN_RIGHT)
        sizer.Add(self.curRA, flag=wx.ALL | wx.ALIGN_CENTER)
        sizer.Add(self.taskRA, flag=wx.ALL | wx.ALIGN_CENTER)

        sizer.Add(self.CreateCaption(codes.get('posDEC')), flag=wx.ALL | wx.ALIGN_RIGHT)
        sizer.Add(self.curDEC, flag=wx.ALL | wx.ALIGN_CENTER)
        sizer.Add(self.taskDEC, flag=wx.ALL | wx.ALIGN_CENTER)

        sizer.Add(self.CreateCaption(codes.get('posFocus')), flag=wx.ALL | wx.ALIGN_RIGHT)
        sizer.Add(self.curFocus, flag=wx.ALL | wx.ALIGN_CENTER)
        sizer.Add(self.taskFocus, flag=wx.ALL | wx.ALIGN_CENTER)

        vert = wx.BoxSizer(wx.VERTICAL)
        vert.Add(sizer)
        vert.Add(self.control, flag=wx.ALIGN_CENTER_HORIZONTAL)

        self.SetSizer(vert)

    """This panel represents telescope position with manual positioning opportunities
    Attributes:
        codes - Translation codes
    """

    def update(self):
        self.curRA.SetLabel('10:10:10')
        self.curDEC.SetLabel('22:22:22')
        self.curFocus.SetLabel('23.23')

        self.taskRA.SetLabel('10:10:10')
        self.taskDEC.SetLabel('22:22:22')
        self.taskFocus.SetLabel('23.23')




