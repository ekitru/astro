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

        sizer = wx.GridSizer(5, 3, 5, 10)

        self.objectName = self.CreateField()
        self.objectOrigRA = self.CreateField()
        self.objectCurrRA = self.CreateField()
        self.objectOrigDEC = self.CreateField()
        self.objectCurrDEC = self.CreateField()
        self.moveBut = wx.Button(self,wx.ID_ANY,"Move to object")

        sizer.Add(self.CreateHeader(codes.get('Object')))
        sizer.Add(self.objectName, 0, wx.ALL | wx.CENTER)
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

        sizer.Add(self.CreateField())
        sizer.Add(self.moveBut)

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

        sizer = wx.GridSizer(5, 2, 5, 10)

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

        self.control = wx.Button(self,wx.ID_ANY,"  Take control  ")

        sizer.Add(self.CreateHeader(codes.get('Positioning')))
        sizer.Add(self.CreateCaption(' '), 0, wx.ALL | wx.CENTER)
        sizer.Add(self.CreateField())

        sizer.Add(self.CreateField())
        sizer.Add(self.CreateCaption(codes.get('pos_cur')), 0, wx.ALL | wx.ALIGN_CENTER)
        sizer.Add(self.CreateCaption(codes.get('pos_task')), 0, wx.ALL | wx.ALIGN_CENTER)

        sizer.Add(self.CreateCaption(codes.get('posRA')), 0, wx.ALL | wx.ALIGN_RIGHT)
        sizer.Add(self.curRA, 0, wx.ALL | wx.ALIGN_CENTER)
        sizer.Add(self.taskRA, 0, wx.ALL | wx.ALIGN_CENTER)
        sizer.Add(self.CreateCaption(codes.get('posDEC')), 0, wx.ALL | wx.ALIGN_RIGHT)
        sizer.Add(self.curDEC, 0, wx.ALL | wx.ALIGN_CENTER)
        sizer.Add(self.taskDEC, 0, wx.ALL | wx.ALIGN_CENTER)
        sizer.Add(self.CreateCaption(codes.get('posFocus')), 0, wx.ALL | wx.ALIGN_RIGHT)
        sizer.Add(self.curFocus, 0, wx.ALL | wx.ALIGN_CENTER)
        sizer.Add(self.taskFocus, 0, wx.ALL | wx.ALIGN_CENTER)
        sizer.Add(self.CreateField())
        sizer.Add(self.control)



        self.SetSizer(sizer)

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




