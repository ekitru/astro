import wx
from ids import *

__author__ = 'kitru'

class SelectObjectDiag(wx.Dialog):
    def __init__(self, parent, id, controller):
        wx.Dialog.__init__(self, parent, id, controller.trans.get('dSelObj_title'), style=wx.DEFAULT_DIALOG_STYLE)
        trans = controller.trans

        self.name = wx.TextCtrl(self)
        self.RA = wx.TextCtrl(self)
        self.DEC = wx.TextCtrl(self)

        grid = wx.FlexGridSizer(2, 2, 5, 5)
        grid.Add(wx.StaticText(self, wx.ID_ANY, trans.get('dSelObj_name')), flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        grid.Add(self.name, flag=wx.ALL | wx.EXPAND)
        grid.Add(wx.StaticText(self, wx.ID_ANY, trans.get('dSelObj_RA')), flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        grid.Add(self.RA, flag=wx.ALL | wx.EXPAND)
        grid.Add(wx.StaticText(self, wx.ID_ANY, trans.get('dSelObj_DEC')), flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        grid.Add(self.DEC, flag=wx.ALL | wx.EXPAND)

        btms = wx.BoxSizer(wx.VERTICAL)
        btms.Add(wx.Button(self, ID_BTM_ADDSTAR, trans.get('dSelObk_add')), flag = wx.DOWN, border=10)
        btms.Add(wx.Button(self, ID_BTM_EDITSTAR, trans.get('dSelObk_edit')))

        colums = wx.BoxSizer(wx.HORIZONTAL)
        colums.Add(grid,flag=wx.ALL, border=10)
        colums.Add(btms, flag=wx.UP | wx.RIGHT , border=10)


        hButtons = wx.BoxSizer(wx.HORIZONTAL)
        hButtons.Add(wx.Button(self, label=trans.get('dSelObj_select')), flag=wx.WEST)
        hButtons.Add(wx.Button(self, label=trans.get('dSelObj_cancel')), flag=wx.EAST)

        vCtrl = wx.BoxSizer(wx.VERTICAL)
        vCtrl.Add(colums)
        vCtrl.Add(hButtons,flag=wx.ALL, border=20)

        vList = wx.ListCtrl(self, style=wx.LC_REPORT)

        hMain = wx.BoxSizer(wx.HORIZONTAL)
        hMain.Add(vCtrl)
        hMain.Add(vList)

        self.SetSizer(hMain)




