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

        self.butAutoManual = self.CreateButton(self.codes.get('pCtrlAuto'),font=self.fontNorm(),size=self.sizeLarge())
        self.butMove = self.CreateButton(label=self.codes.get('pCtrlMov'))

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.butAutoManual)
        sizer.AddSpacer(10)
        sizer.Add(self.butMove)
        self.SetSizer(sizer)

        self.Bind(wx.EVT_BUTTON, self.OnButtonAutoManual, self.butAutoManual)
        self.Bind(wx.EVT_BUTTON, self.OnButtonMove, self.butMove)

    def OnButtonAutoManual(self, event):
        button = event.GetEventObject()
        if self.controller.autoControlSelected():
            self.controller.selectManualControl()
            button.SetLabel(self.codes.get('pCtrlMan'))
        else:
            self.controller.selectAutoControl()
            button.SetLabel(self.codes.get('pCtrlAuto'))

    def OnButtonMove(self, event):
        print('butMove')


    def update(self, controller):
        return #TODO real implementation