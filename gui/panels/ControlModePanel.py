import wx
from core.astronomy import str2rad
from gui.panels.SimplePanel import SimplePanel

__author__ = 'anisand'

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
        self.butMove = self.CreateButton(label=codes.get('pCtrlMov'))

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        column1 = wx.BoxSizer(wx.VERTICAL)
        column1.Add(self.rbObjectSetpoint)
        column1.Add(self.rbManualSetpoint)
        column1.Add(self.rbRemoteControl)

        column2 = wx.BoxSizer(wx.VERTICAL)
        column2.Add(self.butMove)

        sizer.Add(column1)
        sizer.AddSpacer(40)
        sizer.Add(column2)
        self.SetSizer(sizer)

        self.Bind(wx.EVT_RADIOBUTTON, self.OnObjSetpointRadBut, id=self.rbObjectSetpoint.GetId())
        self.Bind(wx.EVT_RADIOBUTTON, self.OnManSetpointRadBut, id=self.rbManualSetpoint.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnButtonMove, self.butMove)

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

    def OnButtonMove(self, event):
        event.Skip()
        data = self._resources.getSetPoint().getRawData()
        plc = self._resources.getPLCManager()
        plc.setSetpointPosition(data['ra'], data['dec'])
        if data['focus']:
            plc.setFocus(data['focus'])

        plc.startMoving()

    def update(self, controller):
        mode = self._resources.getPLCManager().readControlMode()
        self.rbRemoteControl.SetValue(self._isRemoveControl(mode))

        if self.rbObjectSetpoint.GetValue():
            self._resources.updateSetPoint()

        if self.rbManualSetpoint.GetValue():
            self._controls.updateSetPoint()

    def _isRemoveControl(self, mode):
        return mode != 1
