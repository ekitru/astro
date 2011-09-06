import wx

__author__ = 'kitru'

class SimplePanel(wx.Panel):
    def __init__(self, parent=None, ID=wx.ID_ANY):
        wx.Panel.__init__(self, parent, ID)

        #Sizes and Fonts
        self.BUTTON_SIZE_SMALL = (30,25)
        self.BUTTON_FONT_BOLD = wx.Font(10, wx.SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.IN_FIELD_SIZE_NORMAL = (85,27)
        self.BUTTON_SIZE_LARGE = (85,27)
        self.BUTTON_FONT_NORMAL = wx.Font(10, wx.SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)

    def CreateHeader(self, name):
        return self.CreateElement(name, wx.Font(10, wx.SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

    def CreateCaption(self, name):
        return self.CreateElement(name, wx.Font(10, wx.SWISS, wx.FONTSTYLE_SLANT, wx.FONTWEIGHT_LIGHT))

    def CreateField(self):
        return self.CreateElement()

    def CreateCoordField(self):
        element = self.CreateElement()
        element.SetMinSize(wx.Size(80, 20))
        return element

    def CreateElement(self, name="", font=None):
        element = wx.StaticText(self, wx.ID_ANY, name)
        if font:
            element.SetFont(font)
        return element

    def CreateInputField(self, size=wx.DefaultSize):
        return wx.TextCtrl(self, id=wx.ID_ANY, size=size)

    def CreateButton(self, label="",font=None, size=wx.DefaultSize):
        speedSelButton = wx.Button(self, id=wx.ID_ANY, label=label, size=size)
        if font:
            speedSelButton.SetFont(font)
        return speedSelButton

    def CreateBitmapButton(self, rel_path, file_type, size=wx.DefaultSize):
        bitmap = wx.Bitmap(rel_path, file_type)
        return wx.BitmapButton(self, id=wx.ID_ANY, bitmap=bitmap,size=size)

    def CreateToggleButton(self, label="", font=None ,size=wx.DefaultSize):
        toggleButton = wx.ToggleButton(self, id=wx.ID_ANY, label=label, size=size)
        if font:
            toggleButton.SetFont(font)
        return toggleButton


class ObjectPanel(SimplePanel):
    """This panel represents selected object data (name and positions)
    Attributes:
        codes - Translation codes
    """

    def __init__(self, parent, ID=wx.ID_ANY, codes=None):
        SimplePanel.__init__(self, parent, ID)

        comSizer = wx.StaticBoxSizer(wx.StaticBox(self, label=codes.get("pObject")), wx.VERTICAL)
        comSizer.Add(self.CreateCoordinatesGrid(codes), flag=wx.ALL, border=10)
        comSizer.Add(wx.StaticLine(self, wx.ID_ANY, style=wx.LI_HORIZONTAL), flag=wx.ALL | wx.EXPAND)
        comSizer.Add(self.CreateBottomPanel(codes), flag=wx.ALL | wx.EXPAND)
        self.SetSizer(comSizer)

    def CreateCoordinatesGrid(self, codes):
        sizer = wx.GridSizer(4, 3, 5, 10)

        self.objectName = self.CreateField()
        self.objectOrigRA = self.CreateCoordField()
        self.objectCurrRA = self.CreateCoordField()
        self.objectOrigDEC = self.CreateCoordField()
        self.objectCurrDEC = self.CreateCoordField()

        sizer.Add(self.CreateCaption(codes.get('pObjName')), flag=wx.ALL | wx.ALIGN_RIGHT)
        sizer.Add(self.objectName, flag=wx.ALL | wx.EXPAND | wx.CENTER)
        sizer.Add(self.CreateField())

        sizer.Add(self.CreateField())
        sizer.Add(self.CreateCaption(codes.get('pObjEpoch')), flag=wx.ALL | wx.ALIGN_CENTER_HORIZONTAL)
        sizer.Add(self.CreateCaption(codes.get('pObjNow')), flag=wx.ALL | wx.ALIGN_CENTER_HORIZONTAL)
        sizer.Add(self.CreateCaption(codes.get('pObjRA')), flag=wx.ALL | wx.ALIGN_RIGHT)
        sizer.Add(self.objectOrigRA, flag=wx.ALL | wx.ALIGN_CENTER)
        sizer.Add(self.objectCurrRA, flag=wx.ALL | wx.ALIGN_CENTER)

        sizer.Add(self.CreateCaption(codes.get('pObjDEC')), flag=wx.ALL | wx.ALIGN_RIGHT)
        sizer.Add(self.objectOrigDEC, flag=wx.ALL | wx.ALIGN_CENTER)
        sizer.Add(self.objectCurrDEC, flag=wx.ALL | wx.ALIGN_CENTER)
        return sizer

    def CreateBottomPanel(self, codes):
        sizer = wx.BoxSizer(wx.VERTICAL)

        objPos = self.CreateObjectPosition(codes)
        sizer.Add(objPos, flag=wx.ALL, border=10)

        return sizer

    def CreateObjectPosition(self, codes):
        self.objAltitude = self.CreateCoordField()
        self.objHourAngle = self.CreateCoordField()
        self.objRisingTime = self.CreateField()
        self.objSettingTime = self.CreateField()

        sizer = wx.FlexGridSizer(2, 4, 5, 10)
        sizer.Add(self.CreateCaption(codes.get('pObjALT')), flag=wx.ALL | wx.ALIGN_RIGHT)
        sizer.Add(self.objAltitude, flag=wx.ALL | wx.ALIGN_CENTER)
        sizer.Add(self.CreateCaption(codes.get('pObjRise')), flag=wx.ALL | wx.ALIGN_RIGHT)
        sizer.Add(self.objRisingTime, flag=wx.ALL | wx.ALIGN_CENTER)
        sizer.Add(self.CreateCaption(codes.get('pObjHA')), flag=wx.ALL | wx.ALIGN_RIGHT)
        sizer.Add(self.objHourAngle, flag=wx.ALL | wx.ALIGN_CENTER)
        sizer.Add(self.CreateCaption(codes.get('pObjSet')), flag=wx.ALL | wx.ALIGN_RIGHT)
        sizer.Add(self.objSettingTime, flag=wx.ALL | wx.ALIGN_CENTER)
        return sizer

    def update(self, controller):
        """Updates Objects name and coordinates
        """

        object = controller.getObject()
        data = object.getData()

        self.objectName.SetLabel(data['name'])
        self.objectOrigRA.SetLabel(data['ra'])
        self.objectOrigDEC.SetLabel(data['dec'])

        position = object.getCurrentPosition()
        self.objectCurrRA.SetLabel(position['ra'])
        self.objectCurrDEC.SetLabel(position['dec'])
        self.objAltitude.SetLabel(position['alt'])
        self.objHourAngle.SetLabel(position['ha'])
        self.objRisingTime.SetLabel(position['rise'])
        self.objSettingTime.SetLabel(position['set'])


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


class PositioningPanel(SimplePanel):
    """This panel represents telescope position: current and end coordinates
    Attributes:
        codes - Translation codes
    """
    def __init__(self, parent, ID=wx.ID_ANY, codes=None):
        SimplePanel.__init__(self, parent, ID)

        #Positioning panel view sizer
        pPosViewSizer = wx.GridSizer(4, 3, 5, 10)

        self.curRA = self.CreateField()
        self.taskRA = self.CreateField()
        self.curDEC = self.CreateField()
        self.taskDEC = self.CreateField()
        self.curFocus = self.CreateField()
        self.taskFocus = self.CreateField()

        pPosViewSizer.Add(self.CreateField())
        pPosViewSizer.Add(self.CreateCaption(codes.get('pPosCur')), flag=wx.ALL | wx.ALIGN_CENTER_HORIZONTAL)
        pPosViewSizer.Add(self.CreateCaption(codes.get('pPosEnd')), flag=wx.ALL | wx.ALIGN_CENTER_HORIZONTAL)

        pPosViewSizer.Add(self.CreateCaption(codes.get('pPosRA')), flag=wx.ALL | wx.ALIGN_RIGHT)
        pPosViewSizer.Add(self.curRA, flag=wx.ALL | wx.ALIGN_CENTER)
        pPosViewSizer.Add(self.taskRA, flag=wx.ALL | wx.ALIGN_CENTER)

        pPosViewSizer.Add(self.CreateCaption(codes.get('pPosDEC')), flag=wx.ALL | wx.ALIGN_RIGHT)
        pPosViewSizer.Add(self.curDEC, flag=wx.ALL | wx.ALIGN_CENTER)
        pPosViewSizer.Add(self.taskDEC, flag=wx.ALL | wx.ALIGN_CENTER)

        pPosViewSizer.Add(self.CreateCaption(codes.get('pPosFoc')), flag=wx.ALL | wx.ALIGN_RIGHT)
        pPosViewSizer.Add(self.curFocus, flag=wx.ALL | wx.ALIGN_CENTER)
        pPosViewSizer.Add(self.taskFocus, flag=wx.ALL | wx.ALIGN_CENTER)

        #Positioning panel sizer
        pPosSizer = wx.StaticBoxSizer(wx.StaticBox(self, label=codes.get('pPos')), wx.VERTICAL)
        pPosSizer.Add(pPosViewSizer, flag=wx.ALL, border=10)

        self.SetSizer(pPosSizer)

    def update(self, controller):
        position = controller.getTelescopePosition()
        focus = controller.getTelescopeFocus()

        self.curRA.SetLabel(position['cur'][0])
        self.curDEC.SetLabel(position['cur'][1])
        self.curFocus.SetLabel(focus['cur'])

        self.taskRA.SetLabel(position['end'][0])
        self.taskDEC.SetLabel(position['end'][1])
        self.taskFocus.SetLabel(focus['end'])

class ControlPanel(SimplePanel):
    """This panel represents manual control of the telescope. Auto or Manual control modes can be selected.
    Attributes:
        codes - Translation codes
    """
    def __init__(self, parent, ID=wx.ID_ANY, codes=None):
        SimplePanel.__init__(self,parent,ID)

        #Positioning panel control sizer
        pControlSizer = wx.BoxSizer(wx.HORIZONTAL)
        pControlCol1 = wx.BoxSizer(wx.VERTICAL)
        pControlCol2 = wx.BoxSizer(wx.VERTICAL)
        pControlCol3 = wx.GridSizer(4,3,5,5)

        self.inFieldRA = self.CreateInputField(size=self.IN_FIELD_SIZE_NORMAL)
        self.inFieldDEC = self.CreateInputField(size=self.IN_FIELD_SIZE_NORMAL)
        self.inFieldFoc = self.CreateInputField(size=self.IN_FIELD_SIZE_NORMAL)
        self.autoManBut = self.CreateButton(codes.get('pCtrlMan'),font=self.BUTTON_FONT_NORMAL,size=self.BUTTON_SIZE_LARGE)
        self.butManMove = self.CreateButton(label=codes.get('pCtrlMov'))
        self.butMovUpRA = self.CreateBitmapButton("bitmaps/arrow_up.ico", file_type=wx.BITMAP_TYPE_ICO, size = self.BUTTON_SIZE_SMALL)
        self.butMovLftDEC = self.CreateBitmapButton("bitmaps/arrow_left.ico", file_type=wx.BITMAP_TYPE_ICO, size = self.BUTTON_SIZE_SMALL)
        self.butMovRhtDEC = self.CreateBitmapButton("bitmaps/arrow_right.ico", file_type=wx.BITMAP_TYPE_ICO, size = self.BUTTON_SIZE_SMALL)
        self.butMovDwnRA =  self.CreateBitmapButton("bitmaps/arrow_down.ico", file_type=wx.BITMAP_TYPE_ICO, size = self.BUTTON_SIZE_SMALL)
        self.butSelHour = self.CreateToggleButton(label=codes.get('pCtrlHour'),font=self.BUTTON_FONT_BOLD, size=self.BUTTON_SIZE_SMALL)
        self.butSelMin = self.CreateToggleButton(label=codes.get('pCtrlMin'),font=self.BUTTON_FONT_BOLD, size=self.BUTTON_SIZE_SMALL)
        self.butSelSec = self.CreateToggleButton(label=codes.get('pCtrlSec'),font=self.BUTTON_FONT_BOLD, size=self.BUTTON_SIZE_SMALL)
        self.butIncFoc = self.CreateButton(label="+", size=self.BUTTON_SIZE_SMALL)
        self.butDecFoc = self.CreateButton(label="-", size=self.BUTTON_SIZE_SMALL)

        pControlCol1.AddSpacer(5)
        pControlCol1.Add(self.CreateCaption(codes.get('pCtrlRA')), flag=wx.ALIGN_RIGHT)
        pControlCol1.AddSpacer(11)
        pControlCol1.Add(self.CreateCaption(codes.get('pCtrlDEC')), flag=wx.ALIGN_RIGHT)
        pControlCol1.AddSpacer(12)
        pControlCol1.Add(self.CreateCaption(codes.get('pCtrlFoc')), flag=wx.ALIGN_RIGHT)
        pControlCol1.AddSpacer(12)
        pControlCol1.Add(self.autoManBut, flag=wx.ALIGN_RIGHT)

        pControlCol2.Add(self.inFieldRA)
        pControlCol2.AddSpacer(1)
        pControlCol2.Add(self.inFieldDEC)
        pControlCol2.AddSpacer(2)
        pControlCol2.Add(self.inFieldFoc)
        pControlCol2.AddSpacer(4)
        pControlCol2.Add(self.butManMove)
        #self.moveBut.Enable(controller.scopeCanMove())

        pControlCol3.AddSpacer(5)
        pControlCol3.Add(self.butMovUpRA)
        pControlCol3.AddSpacer(5)
        pControlCol3.Add(self.butMovLftDEC)
        pControlCol3.Add(self.butMovDwnRA)
        pControlCol3.Add(self.butMovRhtDEC)
        pControlCol3.Add(self.butDecFoc)
        pControlCol3.AddSpacer(5)
        pControlCol3.Add(self.butIncFoc)
        pControlCol3.Add(self.butSelHour)
        pControlCol3.Add(self.butSelMin)
        pControlCol3.Add(self.butSelSec)

        pControlSizer.AddSpacer(10)
        pControlSizer.Add(pControlCol1)
        pControlSizer.AddSpacer(25)
        pControlSizer.Add(pControlCol2)
        pControlSizer.AddSpacer(20)
        pControlSizer.Add(pControlCol3)

        comSizer = wx.StaticBoxSizer(wx.StaticBox(self, label=codes.get('pCtrl')), wx.VERTICAL)
        comSizer.Add(pControlSizer, flag=wx.ALL, border=10)

        self.SetSizer(comSizer)


class TelescopePanel(SimplePanel):    #TODO decide, what to do with it, temp mock
    def __init__(self, parent, ID=wx.ID_ANY, codes=None):
        SimplePanel.__init__(self, parent, ID)
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




