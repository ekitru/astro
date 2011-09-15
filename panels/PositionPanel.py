import wx
from panels.SimplePanel import SimplePanel

__author__ = 'kitru'

class PositionPanel(SimplePanel):
    """This panel represents telescope position: current and end coordinates
    Attributes:
        codes - Translation codes
    """
    def __init__(self, parent, ID=wx.ID_ANY, codes=None):
        SimplePanel.__init__(self, parent, ID)

        #Positioning panel view sizer
        pPosSizer = wx.GridSizer(4, 3, 5, 10)

        self.curRA = self.CreateField()
        self.taskRA = self.CreateField()
        self.curDEC = self.CreateField()
        self.taskDEC = self.CreateField()
        self.curFocus = self.CreateField()
        self.taskFocus = self.CreateField()

        pPosSizer.Add(self.CreateField())
        pPosSizer.Add(self.CreateCaption(codes.get('pPosCur')), flag=wx.ALL | wx.ALIGN_CENTER_HORIZONTAL)
        pPosSizer.Add(self.CreateCaption(codes.get('pPosEnd')), flag=wx.ALL | wx.ALIGN_CENTER_HORIZONTAL)

        pPosSizer.Add(self.CreateCaption(codes.get('pPosRA')), flag=wx.ALL | wx.ALIGN_RIGHT)
        pPosSizer.Add(self.curRA, flag=wx.ALL | wx.ALIGN_CENTER)
        pPosSizer.Add(self.taskRA, flag=wx.ALL | wx.ALIGN_CENTER)

        pPosSizer.Add(self.CreateCaption(codes.get('pPosDEC')), flag=wx.ALL | wx.ALIGN_RIGHT)
        pPosSizer.Add(self.curDEC, flag=wx.ALL | wx.ALIGN_CENTER)
        pPosSizer.Add(self.taskDEC, flag=wx.ALL | wx.ALIGN_CENTER)

        pPosSizer.Add(self.CreateCaption(codes.get('pPosFoc')), flag=wx.ALL | wx.ALIGN_RIGHT)
        pPosSizer.Add(self.curFocus, flag=wx.ALL | wx.ALIGN_CENTER)
        pPosSizer.Add(self.taskFocus, flag=wx.ALL | wx.ALIGN_CENTER)

        #Positioning panel sizer
        comSizer = wx.StaticBoxSizer(wx.StaticBox(self, label=codes.get('pPos')), wx.VERTICAL)
        comSizer.Add(pPosSizer, flag=wx.ALL, border=10)

        self.SetSizer(comSizer)

    def update(self, controller):
        position = controller.getTelescopePosition()
        focus = controller.getTelescopeFocus()

        self.curRA.SetLabel(position['cur'][0])
        self.curDEC.SetLabel(position['cur'][1])
        self.curFocus.SetLabel(focus['cur'])

#        self.taskRA.SetLabel(position['end'][0])
#        self.taskDEC.SetLabel(position['end'][1])
        self.taskRA.SetLabel(controller.getSetpointCoordinates()[0])
        self.taskDEC.SetLabel(controller.getSetpointCoordinates()[1])
        self.taskFocus.SetLabel(controller.getSetpointFocus())
  