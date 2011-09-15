import wx
from panels.SimplePanel import SimplePanel
import astronomy

__author__ = 'kitru'

class ManualSetpointPanel(SimplePanel):
    """This panel presents means to change manually setpoints for telescope and focus end positions
    Attributes:
        codes - Translation codes
    """

    def __init__(self, parent, controller, ID=wx.ID_ANY, codes=None):
        SimplePanel.__init__(self,parent,ID)

        self.controller = controller
        self.setpoint = controller.setpoint
        self.focus = controller.focus
        self.trans = codes

        self.controlMode = False
        self.setpointSpeed = 1

        #Positioning panel control sizer
        pControlSizer = wx.BoxSizer(wx.HORIZONTAL)
        pControlCol1 = wx.BoxSizer(wx.VERTICAL)
        pControlCol2 = wx.BoxSizer(wx.VERTICAL)
        pControlCol3 = wx.GridSizer(4,3,5,5)

        self.inFieldRA = self.CreateInputField(size=self.sizeLarge())
        self.inFieldDEC = self.CreateInputField(size=self.sizeLarge())
        self.inFieldFoc = self.CreateInputField(size=self.sizeLarge())
        self.butMovUpRA = self.CreateBitmapButton("bitmaps/arrow_up.ico", file_type=self.bitmapType(), size = self.sizeSmall())
        self.butMovLftDEC = self.CreateBitmapButton("bitmaps/arrow_left.ico", file_type=self.bitmapType(), size = self.sizeSmall())
        self.butMovRhtDEC = self.CreateBitmapButton("bitmaps/arrow_right.ico", file_type=self.bitmapType(), size = self.sizeSmall())
        self.butMovDwnRA =  self.CreateBitmapButton("bitmaps/arrow_down.ico", file_type=self.bitmapType(), size = self.sizeSmall())
        self.butSelHour = self.CreateToggleButton(label=codes.get('pCtrlHour'),font=self.fontBold(), size=self.sizeSmall())
        self.butSelMin = self.CreateToggleButton(label=codes.get('pCtrlMin'),font=self.fontBold(), size=self.sizeSmall())
        self.butSelSec = self.CreateToggleButton(label=codes.get('pCtrlSec'),font=self.fontBold(), size=self.sizeSmall())
        self.butIncFoc = self.CreateButton(label="+", size=self.sizeSmall())
        self.butDecFoc = self.CreateButton(label="-", size=self.sizeSmall())

        pControlCol1.AddSpacer(5)
        pControlCol1.Add(self.CreateCaption(codes.get('pCtrlRA')), flag= wx.ALIGN_RIGHT)
        pControlCol1.AddSpacer(11)
        pControlCol1.Add(self.CreateCaption(codes.get('pCtrlDEC')), flag=wx.ALIGN_RIGHT)
        pControlCol1.AddSpacer(12)
        pControlCol1.Add(self.CreateCaption(codes.get('pCtrlFoc')), flag=wx.ALIGN_RIGHT)
        pControlCol1.AddSpacer(12)
#        pControlCol1.Add(self.butAutoManual, flag=wx.ALIGN_RIGHT)

        pControlCol2.Add(self.inFieldRA)
        pControlCol2.AddSpacer(1)
        pControlCol2.Add(self.inFieldDEC)
        pControlCol2.AddSpacer(2)
        pControlCol2.Add(self.inFieldFoc)
        pControlCol2.AddSpacer(4)
#        pControlCol2.Add(self.butMove)
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

        self.Bind(wx.EVT_BUTTON, self.OnButtonUp, self.butMovUpRA)
        self.Bind(wx.EVT_BUTTON, self.OnButtonDown, self.butMovDwnRA)
        self.Bind(wx.EVT_BUTTON, self.OnButtonLeft, self.butMovLftDEC)
        self.Bind(wx.EVT_BUTTON, self.OnButtonRight, self.butMovRhtDEC)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.OnButtonSelHour, self.butSelHour)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.OnButtonSelMin, self.butSelMin)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.OnButtonSelSec, self.butSelSec)
        self.Bind(wx.EVT_BUTTON, self.OnButtonIncFoc, self.butIncFoc)
        self.Bind(wx.EVT_BUTTON, self.OnButtonDecFoc, self.butDecFoc)

        self.butSelSec.SetValue(True)


    def OnButtonUp(self, event):
        incStep = 1
        spSpeed = self.getSetpointSpeed()
        ra = self.setpoint.getCoordinates()[0]
        dec = self.setpoint.getCoordinates()[1]
        ra = self.incRAPosition(ra,spSpeed,incStep)
        self.setpoint.setCoordinates(ra,dec)

    def OnButtonDown(self, event):
        incStep = -1
        spSpeed = self.getSetpointSpeed()
        ra = self.setpoint.getCoordinates()[0]
        dec = self.setpoint.getCoordinates()[1]
        ra = self.incRAPosition(ra,spSpeed,incStep)
        self.setpoint.setCoordinates(ra,dec)

    def OnButtonLeft(self, event):
        incStep = -1
        spSpeed = self.getSetpointSpeed()
        ra = self.setpoint.getCoordinates()[0]
        dec = self.setpoint.getCoordinates()[1]
        dec = self.incDECPosition(dec,spSpeed,incStep)
        self.setpoint.setCoordinates(ra,dec)

    def OnButtonRight(self, event):
        incStep = 1
        spSpeed = self.getSetpointSpeed()
        ra = self.setpoint.getCoordinates()[0]
        dec = self.setpoint.getCoordinates()[1]
        dec = self.incDECPosition(dec,spSpeed,incStep)
        self.setpoint.setCoordinates(ra,dec)

    def OnButtonIncFoc(self, event):
        incStep = 0.1
        f = self.focus.getFocus()
        f = self.incFocus(f,incStep)
        self.focus.setFocus(f)

    def OnButtonDecFoc(self, event):
        incStep = -0.1
        f = self.focus.getFocus()
        f = self.incFocus(f,incStep)
        self.focus.setFocus(f)

    def OnButtonSelHour(self, event):
        butSelHour = self.butSelHour
        butSelMin = self.butSelMin
        butSelSec = self.butSelSec
        self.__handleToggleLogic(butSelHour, butSelMin, butSelSec)
        self.setSetpointSpeed(3)

    def OnButtonSelMin(self, event):
        butSelHour = self.butSelHour
        butSelMin = self.butSelMin
        butSelSec = self.butSelSec
        self.__handleToggleLogic(butSelMin, butSelHour, butSelSec)
        self.setSetpointSpeed(2)

    def OnButtonSelSec(self, event):
        butSelHour = self.butSelHour
        butSelMin = self.butSelMin
        butSelSec = self.butSelSec
        self.__handleToggleLogic(butSelSec, butSelHour, butSelMin)
        self.setSetpointSpeed(1)

    def __handleToggleLogic(self,but1,but2,but3):
        if but1.GetValue():
            but2.SetValue(False)
            but3.SetValue(False)
        else:
            but1.SetValue(True)

    def update(self, controller):
        autoControl = controller.autoControlSelected()
        if autoControl:
            self.Hide()
        else:
            self.Show()



    def getSetpointSpeed(self):
        return self.setpointSpeed

    def setSetpointSpeed(self, spSpeed):
        self.setpointSpeed = spSpeed


    def incRAPosition(self, ra, spSpeed, step):
        if spSpeed == 1:
            ra += astronomy.getHour()/60/60*step
        if spSpeed == 2:
            ra += astronomy.getHour()/60*step
        if spSpeed == 3:
            ra += astronomy.getHour()*step
            if ra > astronomy.getHour()*24:
                ra -= astronomy.getHour()*step
        if ra >= astronomy.RA_235959():
            ra = astronomy.RA_235959()
        if ra < 0.0:
            ra = 0.0
        return ra

    def incDECPosition(self, dec, spSpeed, step):
        if spSpeed == 1:
            dec += astronomy.getDegree()/60/60*step
        if spSpeed == 2:
            dec += astronomy.getDegree()/60*step
        if spSpeed == 3:
            dec += astronomy.getDegree()*step
        if dec > astronomy.getDegree()*90:
            dec = astronomy.getDegree()*90
        if dec < -astronomy.getDegree()*90:
            dec = -astronomy.getDegree()*90
        return dec

    def incFocus(self, foc, step):
        min = 0.0
        max = 2.0
        f = foc + step
        if f < min:
            f = 0.0
        elif f > max:
            f = max
        return f
