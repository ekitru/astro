import wx
from panels.SimplePanel import SimplePanel

__author__ = 'anisand'

class ControlModePanel(SimplePanel):
    """This panel presents means to control the telescope and change its control mode.
    Attributes:
        codes - Translation codes
    """
    def __init__(self, parent, controller, ID=wx.ID_ANY, codes=None):
        SimplePanel.__init__(self,parent,ID)

        self.controller = controller
        self.codes = codes

        self.rbObjectSetpoint = wx.RadioButton(self, wx.ID_ANY, self.codes.get('pCtrlObjSP'))
        self.rbManualSetpoint = wx.RadioButton(self, wx.ID_ANY, self.codes.get('pCtrlManSP'))
        self.rbRemoteControl = wx.RadioButton(self, wx.ID_ANY, self.codes.get('pCtrlRemCtrl'))
        self.butMove = self.CreateButton(label=self.codes.get('pCtrlMov'))

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        column1 = wx.BoxSizer(wx.VERTICAL)
        column2 = wx.BoxSizer(wx.VERTICAL)
        column1.Add(self.rbObjectSetpoint)
        column1.Add(self.rbManualSetpoint)
        column1.Add(self.rbRemoteControl)

        column2.Add(self.butMove)
        sizer.Add(column1)
        sizer.AddSpacer(40)
        sizer.Add(column2)
        self.SetSizer(sizer)

        self.Bind(wx.EVT_RADIOBUTTON, self.OnObjSetpointRadBut, id=self.rbObjectSetpoint.GetId())
        self.Bind(wx.EVT_RADIOBUTTON, self.OnManSetpointRadBut, id=self.rbManualSetpoint.GetId())
        self.Bind(wx.EVT_RADIOBUTTON, self.OnRemoteCtrlRadBut, id=self.rbRemoteControl.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnButtonMove, self.butMove)

    def OnObjSetpointRadBut(self, event):
        self.controller.selectAutoControl()

    def OnManSetpointRadBut(self, event):
        self.controller.selectManualControl()

    def OnRemoteCtrlRadBut(self, event):
        print('remote control')

    def OnButtonMove(self, event):
        print('butMove')


    def update(self, controller):
        return #TODO real implementation