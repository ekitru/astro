import wx
from core import astronomy
from gui.panels.SimplePanel import SimplePanel

__author__ = 'kitru'

class ManualSetpointPanel(SimplePanel):
    """This panel presents means to change manually setpoints for telescope and focus end positions
    Attributes:
        codes - Translation codes
    """
    _setpointSpeed = 1

    def __init__(self, parent, id, codes, resources):
        SimplePanel.__init__(self, parent, id)

        self._setpoint = resources.getSetPoint()
        self._focus = 0

        captions = self.CreateCaptionPanel(codes)
        fields = self.CreateFieldsPanel()
        controls = self.CreateControlPanel(codes)

        sizer = wx.FlexGridSizer(1, 3, 5, 5)
        sizer.Add(captions, flag=wx.EXPAND | wx.RIGHT, border=10)
        sizer.Add(fields, flag=wx.EXPAND | wx.RIGHT, border=20)
        sizer.Add(controls, flag=wx.EXPAND)

        comSizer = wx.StaticBoxSizer(wx.StaticBox(self, label=codes.get('pSetpoint')), wx.VERTICAL)
        comSizer.Add(sizer, flag=wx.EXPAND | wx.ALL, border=10)
        self.SetSizer(comSizer)
        self.Hide()

        self.Bind(wx.EVT_SHOW, self.OnShow)
        self.Bind(wx.EVT_BUTTON, self.OnButtonUp, self.butIncRA)
        self.Bind(wx.EVT_BUTTON, self.OnButtonDown, self.butDecRA)
        self.Bind(wx.EVT_BUTTON, self.OnButtonLeft, self.butDecDEC)
        self.Bind(wx.EVT_BUTTON, self.OnButtonRight, self.butIncDEC)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.OnButtonSelHour, self.butSelHour)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.OnButtonSelMin, self.butSelMin)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.OnButtonSelSec, self.butSelSec)

    def CreateCaptionPanel(self, codes):
        captions = wx.GridSizer(4, 1, 5, 5)
        captions.Add(self.CreateCaption(codes.get('pSetpointRA')), flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTRE_VERTICAL)
        captions.Add(self.CreateCaption(codes.get('pSetpointDEC')), flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTRE_VERTICAL)
        captions.Add(self.CreateElement())
        return captions

    def CreateFieldsPanel(self):
        self.inFieldRA = self.CreateInputField(size=self.sizeLarge())
        self.inFieldDEC = self.CreateInputField(size=self.sizeLarge())

        fields = wx.GridSizer(4, 1, 5, 5)
        fields.AddMany([self.inFieldRA, self.inFieldDEC, self.CreateElement()])
        return fields

    def CreateControlPanel(self, codes):
        #Positioning panel control sizer
        self.butIncRA = self.CreateButton('+', size=self.sizeSmall())
        self.butDecRA = self.CreateButton('-', size=self.sizeSmall())
        self.butIncDEC = self.CreateButton('+', size=self.sizeSmall())
        self.butDecDEC = self.CreateButton('-', size=self.sizeSmall())

        self.butSelHour = self.CreateToggleButton(label=codes.get('pSetpointHour'), font=self.fontBold(), size=self.sizeSmall())
        self.butSelMin = self.CreateToggleButton(label=codes.get('pSetpointMin'), font=self.fontBold(), size=self.sizeSmall())
        self.butSelSec = self.CreateToggleButton(label=codes.get('pSetpointSec'), font=self.fontBold(), size=self.sizeSmall())
        self.butSelSec.SetValue(True)

        buttons = wx.FlexGridSizer(4, 3, 5, 5)
        buttons.AddMany([self.CreateElement(), self.butIncRA, self.butDecRA])
        buttons.AddMany([self.CreateElement(), self.butIncDEC, self.butDecDEC])
        buttons.AddMany([self.butSelHour, self.butSelMin, self.butSelSec])
        return buttons

    def OnShow(self, event):
        if event.GetShow():
            data = self._setpoint.getData()
            self.inFieldRA.SetValue(data['ra'])
            self.inFieldDEC.SetValue(data['dec'])

    def OnButtonUp(self, event):
        sign = 1
        speed = self.__getSetpointSpeed()
        self.__changeInputFieldValue(self._incrementRa, self.inFieldRA, speed, sign)

    def OnButtonDown(self, event):
        sign = -1
        speed = self.__getSetpointSpeed()
        self.__changeInputFieldValue(self._incrementRa, self.inFieldRA, speed, sign)

    def OnButtonLeft(self, event):
        sign = -1
        speed = self.__getSetpointSpeed()
        self.__changeInputFieldValue(self._incrementDec, self.inFieldDEC, speed, sign)

    def OnButtonRight(self, event):
        sign = 1
        speed = self.__getSetpointSpeed()
        self.__changeInputFieldValue(self._incrementDec, self.inFieldDEC, speed, sign)

    def OnButtonSelHour(self, event):
        butSelHour = self.butSelHour
        butSelMin = self.butSelMin
        butSelSec = self.butSelSec
        self.__handleToggleLogic(butSelHour, butSelMin, butSelSec)
        self.__setSetpointSpeed(3)

    def OnButtonSelMin(self, event):
        butSelHour = self.butSelHour
        butSelMin = self.butSelMin
        butSelSec = self.butSelSec
        self.__handleToggleLogic(butSelMin, butSelHour, butSelSec)
        self.__setSetpointSpeed(2)

    def OnButtonSelSec(self, event):
        butSelHour = self.butSelHour
        butSelMin = self.butSelMin
        butSelSec = self.butSelSec
        self.__handleToggleLogic(butSelSec, butSelHour, butSelMin)
        self.__setSetpointSpeed(1)

    def update(self, controller):
        data = self._setpoint.getRawData()
        #print(data)

    def updateSetPoint(self):
        if self._checkCoordinates():  #if coordinates are correct
            ra, dec = self.inFieldRA.GetValue(), self.inFieldDEC.GetValue()
            print(ra,dec)
            self._setpoint.setPosition(ra, dec)

    def __handleToggleLogic(self, but1, but2, but3):
        if but1.GetValue():
            but2.SetValue(False)
            but3.SetValue(False)
        else:
            but1.SetValue(True)

    def __getSetpointSpeed(self):
        return self._setpointSpeed

    def __setSetpointSpeed(self, speed):
        self._setpointSpeed = speed

    def __changeInputFieldValue(self, incrementFunction, inputField, speed, sign):
        coordinate = str(inputField.GetValue())
        coordinate = incrementFunction(coordinate, speed, sign)
        return inputField.SetValue(coordinate)

    def _incrementRa(self, ra, speed, sign):
        ra = astronomy.getHours(ra)
        if speed == 1:
            ra = astronomy.getHours(ra + astronomy.RA_SECOND * sign)
        if speed == 2:
            ra = astronomy.getHours(ra + astronomy.RA_MINUTE * sign)
        if speed == 3:
            ra = astronomy.getHours(ra + astronomy.RA_HOUR * sign)
        if ra > astronomy.normRa(ra) or ra < astronomy.normRa(ra):
            ra = astronomy.normRa(ra)
        return str(ra)

    def _incrementDec(self, dec, speed, sign):
        dec = astronomy.getDegrees(dec)
        if speed == 1:
            dec = astronomy.getDegrees(dec + astronomy.DEC_SECOND * sign)
        if speed == 2:
            dec = astronomy.getDegrees(dec + astronomy.DEC_MINUTE * sign)
        if speed == 3:
            dec = astronomy.getDegrees(dec + astronomy.DEC_DEGREE * sign)
        if dec > astronomy.normDec(dec) or dec < astronomy.normDec(dec):
            dec = astronomy.normDec(dec)
        return str(dec)

    def _checkCoordinates(self):
        ra, dec = self.inFieldRA.GetValue(), self.inFieldDEC.GetValue()
        return astronomy.checkCoordinates(ra, dec)