import wx
from panels.SimplePanel import SimplePanel

__author__ = 'kitru'

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
        pControlCol1.Add(self.CreateCaption(codes.get('pCtrlRA')), flag= wx.ALIGN_RIGHT)
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
  