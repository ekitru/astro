import wx
import os

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

    def CreateCoordField(self):
        element = self.CreateElement()
        element.SetMinSize(wx.Size(80, 20))
        return element

    def CreateElement(self, name="", font=None):
        element = wx.StaticText(self, wx.ID_ANY, name)
        if font:
            element.SetFont(font)
        return element

    def CreateInputField(self):
        return wx.TextCtrl(self, id=wx.ID_ANY)

    def CreateButton(self, label="",font=None, size=wx.DefaultSize):
        speedSelButton = wx.Button(self, wx.ID_ANY, label=label, size=size)
        if font:
            speedSelButton.SetFont(font)
        return speedSelButton

    def CreateBitmapButton(self, rel_path, file_type, size=wx.DefaultSize):
        bitmap = self.__gifBitmapWhiteBGToTransparent(rel_path, file_type)
        return wx.BitmapButton(self, id=wx.ID_ANY, bitmap=bitmap,size=size)

    def __gifBitmapWhiteBGToTransparent(self,path,type):
        """Turns bitmap with white backgrount into
        bitmap with transparent background.
        path - relative path to bitmap file.
        type - type of bitmap file (.gif)"""
        absPath = os.path.abspath(path)
        bitmap = wx.Bitmap(absPath, type=type)
        mask = wx.MaskColour(bitmap, wx.WHITE)
        bitmap.SetMask(mask)
        return bitmap

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

        self.moveBut = wx.Button(self, wx.ID_ANY, codes.get('pObjMove'))
        sizer.Add(self.moveBut, flag=wx.ALIGN_RIGHT)
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

        self.moveBut.Enable(controller.scopeCanMove())

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
    """This panel represents telescope position with manual positioning opportunities
    Attributes:
        codes - Translation codes
    """

    def __init__(self, parent, ID=wx.ID_ANY, codes=None):
        SimplePanel.__init__(self, parent, ID)

        bitmapButtonSize = (30,23)
        speedButtonSize = (30,23)
        speedButtonFont = wx.Font(18, wx.SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        speedHourButtonFont = wx.Font(10, wx.SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        bitmapType = wx.BITMAP_TYPE_GIF

        posSizer = wx.GridSizer(4, 3, 5, 10)

        self.curRA = self.CreateField()
        self.taskRA = self.CreateField()
        self.curDEC = self.CreateField()
        self.taskDEC = self.CreateField()
        self.curFocus = self.CreateField()
        self.taskFocus = self.CreateField()
        self.control = wx.Button(self, wx.ID_ANY, codes.get('pPosCtrl'),size=(90,23))

        posSizer.Add(self.CreateField())
        posSizer.Add(self.CreateCaption(codes.get('pPosCur')), flag=wx.ALL | wx.ALIGN_CENTER_HORIZONTAL)
        posSizer.Add(self.CreateCaption(codes.get('pPosEnd')), flag=wx.ALL | wx.ALIGN_CENTER_HORIZONTAL)

        posSizer.Add(self.CreateCaption(codes.get('pPosRA')), flag=wx.ALL | wx.ALIGN_RIGHT)
        posSizer.Add(self.curRA, flag=wx.ALL | wx.ALIGN_CENTER)
        posSizer.Add(self.taskRA, flag=wx.ALL | wx.ALIGN_CENTER)

        posSizer.Add(self.CreateCaption(codes.get('pPosDEC')), flag=wx.ALL | wx.ALIGN_RIGHT)
        posSizer.Add(self.curDEC, flag=wx.ALL | wx.ALIGN_CENTER)
        posSizer.Add(self.taskDEC, flag=wx.ALL | wx.ALIGN_CENTER)

        posSizer.Add(self.CreateCaption(codes.get('pPosFoc')), flag=wx.ALL | wx.ALIGN_RIGHT)
        posSizer.Add(self.curFocus, flag=wx.ALL | wx.ALIGN_CENTER)
        posSizer.Add(self.taskFocus, flag=wx.ALL | wx.ALIGN_CENTER)


        plcSizer = wx.FlexGridSizer(4, 5, 5, 5)
        RAspeedSelSizer = wx.BoxSizer(wx.HORIZONTAL)
        DECspeedSelSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.manSetPointRA = self.CreateInputField()
        self.movLeftRA = self.CreateBitmapButton('bitmaps/arrow_left.gif', wx.BITMAP_TYPE_GIF, size=bitmapButtonSize)
        self.movRightRA = self.CreateBitmapButton('bitmaps/arrow_right.gif', wx.BITMAP_TYPE_GIF, size=bitmapButtonSize)
        self.speedSecRA = self.CreateButton(label=codes.get('pPosSpeedSec'), font=speedButtonFont, size=speedButtonSize)
        self.speedMinRA = self.CreateButton(label=codes.get('pPosSpeedMin'), font=speedButtonFont, size=speedButtonSize)
        self.speedHourRA = self.CreateButton(label=codes.get('pPosSpeedHour'),size=speedButtonSize,
                                             font=speedHourButtonFont)

        RAspeedSelSizer.Add(self.speedHourRA)
        RAspeedSelSizer.Add(self.speedMinRA)
        RAspeedSelSizer.Add(self.speedSecRA)

        plcSizer.Add(self.CreateCaption(codes.get('pPosRA')), flag=wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border=10)
        plcSizer.Add(self.manSetPointRA, border= 10)
        plcSizer.Add(self.movLeftRA)
        plcSizer.Add(self.movRightRA)
        plcSizer.Add(RAspeedSelSizer)


        comSizer = wx.StaticBoxSizer(wx.StaticBox(self, label=codes.get('pPos')), wx.VERTICAL)
        comSizer.Add(posSizer, flag=wx.ALL, border=10)
        comSizer.Add(self.control, flag=wx.ALIGN_RIGHT)
        comSizer.Add(plcSizer, flag = wx.TOP, border=10)

        self.SetSizer(comSizer)

    def update(self, controller):
        position = controller.getTelescopePosition()
        focus = controller.getTelescopeFocus()

        self.curRA.SetLabel(position['cur'][0])
        self.curDEC.SetLabel(position['cur'][1])
        self.curFocus.SetLabel(focus['cur'])

        self.taskRA.SetLabel(position['end'][0])
        self.taskDEC.SetLabel(position['end'][1])
        self.taskFocus.SetLabel(focus['end'])


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




