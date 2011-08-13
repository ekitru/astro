import wx

__author__ = 'kitru'

class SimplePanel(wx.Panel):
    def __init__(self, parent=None, ID=wx.ID_ANY):
        wx.Panel.__init__(self, parent, ID)

    def addLine(self, layout, key="",value="", keyFont=None, valueFont=None, keyFlag=None, valueFlag=None):
        keyField = wx.StaticText(self, wx.ID_ANY, key)
        valueField = wx.StaticText(self, wx.ID_ANY, value)

        if keyFont:
            keyField.SetFont(keyFont)
        if valueFont:
            valueField.SetFont(valueFont)

        self.__addElement(layout, keyField, keyFlag)
        self.__addElement(layout, valueField, valueFlag)

        return keyField, valueField

    def __addElement(self, layout, element, flag):
        if flag is None:
            flag = wx.ALL | wx.EXPAND | wx.CENTER
        layout.Add(element, 0, flag)


class TimeDatePanel(SimplePanel):
    def __init__(self, parent, ID=wx.ID_ANY, codes=None):
        SimplePanel.__init__(self, parent, ID)

        sizer = wx.GridSizer(5, 2, 0, 20)
        self.addLine(sizer, codes.get("Time & Date"), keyFont=wx.Font(11, wx.SWISS, wx.NORMAL, wx.BOLD))
        caption, self.LT = self.addLine(sizer, codes.get("Local Time"), keyFlag=wx.wx.ALL | wx.ALIGN_RIGHT)
        caption, self.UTC = self.addLine(sizer, codes.get("UTC"), keyFlag=wx.wx.ALL | wx.ALIGN_RIGHT)
        caption, self.JD = self.addLine(sizer, codes.get("Julian day"), keyFlag=wx.wx.ALL | wx.ALIGN_RIGHT)
        caption, self.LST = self.addLine(sizer, codes.get("Local sidereal time"), keyFlag=wx.wx.ALL | wx.ALIGN_RIGHT)
        self.SetSizer(sizer)

    def update(self, mechanics):
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


class ObjectPanel(SimplePanel):
    def __init__(self, parent, ID=wx.ID_ANY, codes=None):
        SimplePanel.__init__(self, parent, ID)

        sizer = wx.GridSizer(4,4,0,20)

        caption, self.objectName = self.addLine(sizer, key=codes.get("Object"), keyFont=wx.Font(11, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.addLine(sizer, keyFont=wx.Font(11, wx.SWISS, wx.NORMAL, wx.BOLD)) # dummy line
        self.addLine(sizer, value = codes.get('absoluteRADEC'), valueFont=wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.addLine(sizer, value = codes.get('currentRADEC'), valueFont=wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))



        self.SetSizer(sizer)
