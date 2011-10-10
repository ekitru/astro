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
    def __init__(self, parent, controller, id=wx.ID_ANY, codes=None):
        SimplePanel.__init__(self,parent,id)

        self.controller = controller
        self.setpoint = controller.setpointCoordinates
        self.focus = controller.setpointFocus
        self.trans = codes

        #Positioning panel control sizer
        pControlSizer = wx.BoxSizer(wx.HORIZONTAL)
        pControlCol1 = wx.BoxSizer(wx.VERTICAL)
        pControlCol2 = wx.BoxSizer(wx.VERTICAL)
        pControlCol3 = wx.GridSizer(4,3,5,5)

        self.inFieldRA = self.CreateInputField(size=self.sizeLarge())
        self.inFieldDEC = self.CreateInputField(size=self.sizeLarge())
        self.inFieldFoc = self.CreateInputField(size=self.sizeLarge())
        self.butMovUpRA = self.CreateBitmapButton("arrow_up.ico", file_type=self.bitmapType(), size = self.sizeSmall())
        self.butMovLftDEC = self.CreateBitmapButton("arrow_left.ico", file_type=self.bitmapType(), size = self.sizeSmall())
        self.butMovRhtDEC = self.CreateBitmapButton("arrow_right.ico", file_type=self.bitmapType(), size = self.sizeSmall())
        self.butMovDwnRA =  self.CreateBitmapButton("arrow_down.ico", file_type=self.bitmapType(), size = self.sizeSmall())
        self.butSelHour = self.CreateToggleButton(label=codes.get('pSetpointHour'),font=self.fontBold(), size=self.sizeSmall())
        self.butSelMin = self.CreateToggleButton(label=codes.get('pSetpointMin'),font=self.fontBold(), size=self.sizeSmall())
        self.butSelSec = self.CreateToggleButton(label=codes.get('pSetpointSec'),font=self.fontBold(), size=self.sizeSmall())
        self.butIncFoc = self.CreateButton(label="+", size=self.sizeSmall())
        self.butDecFoc = self.CreateButton(label="-", size=self.sizeSmall())
        self.butSetCoords = self.CreateButton(label='Set', size=self.sizeLarge())

        pControlCol1.AddSpacer(5)
        pControlCol1.Add(self.CreateCaption(codes.get('pSetpointRA')), flag= wx.ALIGN_RIGHT)
        pControlCol1.AddSpacer(11)
        pControlCol1.Add(self.CreateCaption(codes.get('pSetpointDEC')), flag=wx.ALIGN_RIGHT)
        pControlCol1.AddSpacer(12)
        pControlCol1.Add(self.CreateCaption(codes.get('pSetpointFoc')), flag=wx.ALIGN_RIGHT)
        pControlCol1.AddSpacer(12)
#        pControlCol1.Add(self.butAutoManual, flag=wx.ALIGN_RIGHT)

        pControlCol2.Add(self.inFieldRA)
        pControlCol2.AddSpacer(1)
        pControlCol2.Add(self.inFieldDEC)
        pControlCol2.AddSpacer(2)
        pControlCol2.Add(self.inFieldFoc)
        pControlCol2.AddSpacer(4)
        pControlCol2.AddSpacer(self.butSetCoords)
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

        pControlSizer.AddSpacer(4)
        pControlSizer.Add(pControlCol1)
        pControlSizer.AddSpacer(18)
        pControlSizer.Add(pControlCol2)
        pControlSizer.AddSpacer(18)
        pControlSizer.Add(pControlCol3)

        comSizer = wx.StaticBoxSizer(wx.StaticBox(self, label=codes.get('pSetpoint')), wx.VERTICAL)
        comSizer.Add(pControlSizer, flag=wx.ALL, border=10)

        self.SetSizer(comSizer)

        self.Bind(wx.EVT_SHOW, self.OnShow)
        self.Bind(wx.EVT_BUTTON, self.OnButtonUp, self.butMovUpRA)
        self.Bind(wx.EVT_BUTTON, self.OnButtonDown, self.butMovDwnRA)
        self.Bind(wx.EVT_BUTTON, self.OnButtonLeft, self.butMovLftDEC)
        self.Bind(wx.EVT_BUTTON, self.OnButtonRight, self.butMovRhtDEC)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.OnButtonSelHour, self.butSelHour)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.OnButtonSelMin, self.butSelMin)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.OnButtonSelSec, self.butSelSec)
        self.Bind(wx.EVT_BUTTON, self.OnButtonIncFoc, self.butIncFoc)
        self.Bind(wx.EVT_BUTTON, self.OnButtonDecFoc, self.butDecFoc)
        self.Bind(wx.EVT_BUTTON, self.OnButtonSet, self.butSetCoords)

        self.butSelSec.SetValue(True)


    def OnShow(self, event):
        if event.GetShow():
            self.inFieldRA.SetValue(self.setpoint.getAsString()[0])
            self.inFieldDEC.SetValue(self.setpoint.getAsString()[1])
            self.inFieldFoc.SetValue(self.focus.getAsString())

    def OnButtonSet(self, event):
        if self.__checkCoordinatesAndFocus():
            ra, dec, foc = self.inFieldRA.GetValue(), self.inFieldDEC.GetValue(),self.inFieldFoc.GetValue()
            self.controller.setpointCoordinates.setValue(str(ra),str(dec))
            self.controller.setpointFocus.setValue(float(foc))

    def OnButtonUp(self, event):
        sign = 1
        speed = self.__getSetpointSpeed()
        self.__changeInputFieldValue(self.__incrementRa, self.inFieldRA, speed, sign)

    def OnButtonDown(self, event):
        sign = -1
        speed = self.__getSetpointSpeed()
        self.__changeInputFieldValue(self.__incrementRa, self.inFieldRA, speed, sign)

    def OnButtonLeft(self, event):
        sign = -1
        speed = self.__getSetpointSpeed()
        self.__changeInputFieldValue(self.__incrementDec, self.inFieldDEC, speed, sign)

    def OnButtonRight(self, event):
        sign = 1
        speed = self.__getSetpointSpeed()
        self.__changeInputFieldValue(self.__incrementDec, self.inFieldDEC, speed, sign)

    def OnButtonIncFoc(self, event):
        sign = 1
        speed = None
        self.__changeInputFieldValue(self.__incrementFocus, self.inFieldFoc, speed, sign)

    def OnButtonDecFoc(self, event):
        sign = -1
        speed = None
        self.__changeInputFieldValue(self.__incrementFocus, self.inFieldFoc, speed, sign)

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
        autoControl = controller.objSetpointControlSelected()
        if autoControl:
            self.Hide()
        else:
            self.Show()
        if self.__checkCoordinatesAndFocus():
           self.butSetCoords.Enable()
        else:
           self.butSetCoords.Disable()


    def __handleToggleLogic(self,but1,but2,but3):
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
        coordinate = incrementFunction(coordinate,speed,sign)
        return inputField.SetValue(coordinate)

    def __incrementRa(self, ra, speed, sign):
        ra = astronomy.hours(ra)
        if speed == 1:
            ra = astronomy.hours(ra + astronomy.RA_SECOND*sign)
        if speed == 2:
            ra = astronomy.hours(ra + astronomy.RA_MINUTE*sign)
        if speed == 3:
            ra = astronomy.hours(ra + astronomy.RA_HOUR*sign)
        if ra > astronomy.normRa(ra) or ra < astronomy.normRa(ra):
            ra = astronomy.normRa(ra)
        return str(ra)

    def __incrementDec(self, dec, speed, sign):
        dec = astronomy.degrees(dec)
        if speed == 1:
            dec = astronomy.degrees(dec + astronomy.DEC_SECOND*sign)
        if speed == 2:
            dec = astronomy.degrees(dec + astronomy.DEC_MINUTE*sign)
        if speed == 3:
            dec = astronomy.degrees(dec + astronomy.DEC_DEGREE*sign)
        if dec > astronomy.normDec(dec) or dec < astronomy.normDec(dec):
            dec = astronomy.normDec(dec)
        return str(dec)

    def __incrementFocus(self, focus, speed, sign):
        if self.__checkFocus(focus):
            focus = float(focus) + 0.1*sign
            focus = self.__normFocus(focus)
            return str(focus)
        else:
            #temp solution TODO: real implementation
            print('check focus')
            return focus

    def __normFocus(self, focus):
        """(float)
            Checks that focus distance is within limits. If not, then it's value is set to the closest limit
        """
        if focus < 0.0:
            return 0.0
        if focus > 2.0:
            return 2.0
        else:
            return focus

    def __checkFocus(self, focus):
        try:
            focus = float(focus)
            if focus >= 0.0 and focus <= 2.0:
                return True
            else:
                return False
        except Exception:
            return False

    def __checkCoordinatesAndFocus(self):
        ra, dec, foc = self.inFieldRA.GetValue(), self.inFieldDEC.GetValue(),self.inFieldFoc.GetValue()
        return astronomy.checkCoordinates(ra, dec) and self.__checkFocus(foc)