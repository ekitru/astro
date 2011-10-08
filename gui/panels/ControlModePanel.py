import wx
from gui.panels.SimplePanel import SimplePanel

__author__ = 'anisand'

class ControlModePanel(SimplePanel):
    """This panel presents means to control the telescope and change its control mode.
    Attributes:
        codes - Translation codes
    """
    _setpointControlMode = 1
    def __init__(self, parent, id=wx.ID_ANY, codes=None):
        SimplePanel.__init__(self,parent,id)

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
        self._setpointControlMode = 1

    def OnManSetpointRadBut(self, event):
        self._setpointControlMode = 0

    def OnRemoteCtrlRadBut(self, event):
        return

    def OnButtonMove(self, event):
        #if self.controller.PLCManager.mockPCMode:
        #    self.controller.PLCManager.mockPCMode = False
        #else:
        #    self.controller.PLCManager.mockPCMode = True
        return

    def update(self, controller):
        if self._setpointControlMode == 1:
            controller.selObjSetpointControl()
        else:
            controller.selManSetpointControl()

        if controller.remoteControlSelected():
            self.rbObjectSetpoint.Disable()
            self.rbManualSetpoint.Disable()
            self.rbRemoteControl.Enable()
            self.rbRemoteControl.SetValue(True)
            self._setpointControlMode = 1
        if controller.pcControlSelected():
            self.rbRemoteControl.Disable()
            self.rbObjectSetpoint.Enable()
            self.rbManualSetpoint.Enable()
            self.butMove.Disable()
            if self.rbRemoteControl.GetValue():
                self.rbObjectSetpoint.SetValue(True)
            if controller.scopeCanMove() or not self._setpointControlMode == 1:
                self.butMove.Enable()
