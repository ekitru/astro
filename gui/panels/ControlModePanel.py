import wx
from gui.ids import    ID_MANUAL_PANEL
from gui.panels.SimplePanel import SimplePanel

class ControlModePanel(SimplePanel):
    """This panel represents control mode and some control functions  """
    _setpointControlMode = 1

    def __init__(self, parent, codes, control):
        SimplePanel.__init__(self, parent)

        self.controlRepr = control

        self.butStart = self.CreateButton(label=codes.get('pCtrlStart'))
        self.butStop = self.CreateButton(label=codes.get('pCtrlStop'))

        self.rbObjectSetpoint = wx.RadioButton(self, wx.ID_ANY, codes.get('pCtrlObjSP'))
        self.rbManualSetpoint = wx.RadioButton(self, wx.ID_ANY, codes.get('pCtrlManSP'))
        self.rbRemoteControl = wx.RadioButton(self, wx.ID_ANY, codes.get('pCtrlRemCtrl'))
        self.rbRemoteControl.Disable()

        column1 = wx.BoxSizer(wx.VERTICAL)
        column1.Add(self.rbObjectSetpoint)
        column1.Add(self.rbManualSetpoint)
        column1.Add(self.rbRemoteControl)
        column2 = wx.BoxSizer(wx.HORIZONTAL)
        column2.Add(self.butStart)
        column2.Add(self.butStop)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(column1)
        sizer.AddSpacer(40)
        sizer.Add(column2)

        comSizer = wx.StaticBoxSizer(wx.StaticBox(self, label=codes.get('pCtrlTitle')), wx.VERTICAL)
        comSizer.Add(sizer, flag=wx.EXPAND | wx.ALL, border=10)
        self.SetSizer(comSizer)

        self.Bind(wx.EVT_RADIOBUTTON, self.OnObjSetpointRadBut, id=self.rbObjectSetpoint.GetId())
        self.Bind(wx.EVT_RADIOBUTTON, self.OnManSetpointRadBut, id=self.rbManualSetpoint.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnBtnStart, self.butStart)
        self.Bind(wx.EVT_BUTTON, self.OnBtnStop, self.butStop)

    def OnObjSetpointRadBut(self, event):
        event.Skip()
        self._showManualControl(False)
        self.controlRepr.takeControl()


    def OnManSetpointRadBut(self, event):
        event.Skip()
        self._showManualControl(True)
        self.controlRepr.takeControl()

    def _showManualControl(self, visible):
        panel = self._getManualControlPanel()
        panel.Show(visible)
        self.GetParent().Fit()

    def _getManualControlPanel(self):
        return wx.FindWindowById(ID_MANUAL_PANEL)

    def OnBtnStart(self, event):
        event.Skip()
        self.controlRepr.setNewSetPoint()
        self.controlRepr.startMoving()

    def OnBtnStop(self, event):
        event.Skip()
        self.controlRepr.stopMoving()


    def update(self):
#        print('Setpoint: ', self.controlRepr._res.setPoint.getData())
        self.controlRepr.sendTimes()
        self._switchStartButton()

        if not self.butStart.Enabled:
            self.rbObjectSetpoint.SetValue(True)
            self._showManualControl(False)


        if self.controlRepr.isRemoveControl():
            self.rbRemoteControl.SetValue(True) #switch to remove control
            self._showManualControl(False)

        if self.rbObjectSetpoint.GetValue():
            self.controlRepr.updateSetPointByObjectCoordinates()

        if self.rbManualSetpoint.GetValue(): #continously update setpoint from manual control
            self._getManualControlPanel().updateSetPointCoordinates()

    def _switchStartButton(self):
        if self.controlRepr.isMovable() and  not self.controlRepr.isMoving(): #if movable and not started yet
            self.butStart.Enable()
        else:
            self.butStart.Disable()

