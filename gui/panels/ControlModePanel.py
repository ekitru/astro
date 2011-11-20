import wx
import ephem
from core.astronomy import getHours, getDegrees
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
        event.Skip()
        self.takeControl()
        self._controls.Hide()
        self.GetParent().Fit()
        self._resources.updateSetPoint()

    def OnManSetpointRadBut(self, event):
        event.Skip()
        self.takeControl()
        self._controls.Show()
        self.GetParent().Fit()

    def takeControl(self):
        plc = self._resources.plcManager
        plc.takeControl()

    def OnBtnStart(self, event):
        event.Skip()
        data = self._resources.getSetPoint().getRawData()
        data['st'] = ephem.hours(self._resources.getObserver().getLST()).real
        data['ha'] = data['st']-data['ra']
        print('=====  send ha and lst', data['ha'], data['st'])
        print('RA',getHours(data['ra']), 'DEC', getDegrees(data['dec']), 'HA', getHours(data['ha']), 'ST', getHours(data['st']))
        plc = self._resources.plcManager
        plc.setSetpointPosition(ra=data['ra'], dec=data['dec'], ha=data['ha'], st=data['st'])
        if data['focus']:
            plc.setFocus(data['focus'])

        plc.startMoving()

    def OnBtnStop(self, event):
        event.Skip()
        plc = self._resources.plcManager
        plc.stopMoving()


    def update(self):
        mode = self._resources.plcManager.readControlMode()
        self.rbRemoteControl.SetValue(self._isRemoveControl(mode))

        if self.rbObjectSetpoint.GetValue():
            self._resources.updateSetPoint()

        if self.rbManualSetpoint.GetValue():
            self._controls.updateSetPoint()

        if self._resources.plcManager.readTelescopeMovingStatus()['pMoveable'] != 'pMoveableTrue':
            self.butStart.Disable()
        else:
            self.butStart.Enable()

    def _isRemoveControl(self, mode):
        return mode is not 'pState_PC'
