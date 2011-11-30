import wx
from gui.panels.SimplePanel import SimplePanel

__author__ = 'kitru'

class PositionPanel(SimplePanel):
    """This panel represents telescope position: current and end coordinates
    Attributes:
        codes - Translation codes
    """
    def __init__(self, parent, id=wx.ID_ANY, codes=None):
        SimplePanel.__init__(self, parent, id)

        pPosSizer = wx.GridSizer(4, 3, 5, 10)

        self.curRA = self.CreateField()
        self.taskRA = self.CreateField()
        self.curDEC = self.CreateField()
        self.taskDEC = self.CreateField()
        self.curFocus = self.CreateField()

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

        #Positioning panel sizer
        comSizer = wx.StaticBoxSizer(wx.StaticBox(self, label=codes.get('pPos')), wx.VERTICAL)
        comSizer.Add(pPosSizer, flag=wx.ALL, border=10)

        self.SetSizer(comSizer)

    def update(self, controller):
        posRepr = controller.tsPosition

        position = posRepr.getCurrentPosition()
        self.curRA.SetLabel(position['ra'])
        self.curDEC.SetLabel(position['dec'])

        position = posRepr.getSetpointPosition()
        self.taskRA.SetLabel(position['ra'])
        self.taskDEC.SetLabel(position['dec'])

        focus = posRepr.getFocus()
        self.curFocus.SetLabel(focus)
