import wx
from gui.panels.SimplePanel import SimplePanel

class ControlModePanel(SimplePanel):
    """This panel presents means to control the telescope and change its control mode.
    Attributes:
        codes - Translation codes
    """
    _setpointControlMode = 1

    def __init__(self, parent, codes, resources, controls):
        """ Attr:
            codes - translation codes
            resouces - program resources
            controls - ManualSetPointPanel """
        SimplePanel.__init__(self, parent)

        self._resources = resources
        self._controls = controls

        self.rbObjectSetpoint = wx.RadioButton(self, wx.ID_ANY, codes.get('pCtrlObjSP'))
        self.rbManualSetpoint = wx.RadioButton(self, wx.ID_ANY, codes.get('pCtrlManSP'))
        self.rbRemoteControl = wx.RadioButton(self, wx.ID_ANY, codes.get('pCtrlRemCtrl'))
        self.rbRemoteControl.Disable()
        self.butStart = self.CreateButton(label=codes.get('pCtrlStart'))
        self.butStop = self.CreateButton(label=codes.get('pCtrlStop'))

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        column1 = wx.BoxSizer(wx.VERTICAL)
        column1.Add(self.rbObjectSetpoint)
        column1.Add(self.rbManualSetpoint)
        column1.Add(self.rbRemoteControl)

        column2 = wx.BoxSizer(wx.HORIZONTAL)
        column2.Add(self.butStart)
        column2.Add(self.butStop)

        sizer.Add(column1)
        sizer.AddSpacer(40)
        sizer.Add(column2)
        self.SetSizer(sizer)

        self.Bind(wx.EVT_RADIOBUTTON, self.OnObjSetpointRadBut, id=self.rbObjectSetpoint.GetId())
        self.Bind(wx.EVT_RADIOBUTTON, self.OnManSetpointRadBut, id=self.rbManualSetpoint.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnBtnStart, self.butStart)
        self.Bind(wx.EVT_BUTTON, self.OnBtnStop, self.butStop)

    def OnObjSetpointRadBut(self, event):
        self.takeControl()
        self._controls.Hide()
        self.GetParent().Fit()
        self._resources.updateSetPoint()

    def OnManSetpointRadBut(self, event):
        self.takeControl()
        self._controls.Show()
        self.GetParent().Fit()

    def takeControl(self):
        plc = self._resources.getPLCManager()
        plc.takeControl()

    def OnBtnStart(self, event):
        event.Skip()
        data = self._resources.getSetPoint().getRawData()
        plc = self._resources.getPLCManager()
        plc.setSetpointPosition(data['ra'], data['dec'])
        if data['focus']:
            plc.setFocus(data['focus'])

        plc.startMoving()

    def OnBtnStop(self, event):
        event.Skip()
        plc = self._resources.getPLCManager()
        plc.stopMoving()


    def update(self, controller):
        mode = self._resources.getPLCManager().readControlMode()
        self.rbRemoteControl.SetValue(self._isRemoveControl(mode))

        if self.rbObjectSetpoint.GetValue():
            self._resources.updateSetPoint()

        if self.rbManualSetpoint.GetValue():
            self._controls.updateSetPoint()

        if self._resources.getPLCManager().readTelescopeMovingStatus()['pMoveable'] != 'pMoveableTrue':
            self.butStart.Disable()
        else:
            self.butStart.Enable()

    def _isRemoveControl(self, mode):
        return mode != 1
