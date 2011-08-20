import wx
from wx.lib.inspection import InspectionTool
import sys
from ids import *

__author__ = 'kitru'

class SelectObjectDiag(wx.Dialog):
    def __init__(self, parent, id, controller):
        wx.Dialog.__init__(self, parent, id, controller.trans.get('dSelObj_title'), style= wx.CAPTION)

        self.controller = controller
        trans = controller.trans

        self.starName = ""
        self.name = wx.TextCtrl(self, size=(120,-1))
        self.RA = wx.TextCtrl(self, size=(120,-1))
        self.DEC = wx.TextCtrl(self, size=(120,-1))

        self.vList = self.CreateListCtrl(trans)
        self.fillList(self.controller.getStars(self.starName))

        objProp = self.CreateObjectPanel(trans)

        ctrlButtons = wx.BoxSizer(wx.HORIZONTAL)
        ctrlButtons.Add(wx.Button(self, wx.ID_OK, label=trans.get('dSelObj_select')), flag=wx.ALIGN_BOTTOM)
        ctrlButtons.Add(wx.Button(self, wx.ID_CANCEL, label=trans.get('dSelObj_cancel')), flag=wx.ALIGN_BOTTOM)

        vCtrl = wx.BoxSizer(wx.VERTICAL)
        vCtrl.Add(objProp, flag=wx.ALL | wx.ALIGN_RIGHT, border=5)
        vCtrl.Add(ctrlButtons, 1, flag=wx.ALL | wx.EXPAND, border=5)

        hMain = wx.FlexGridSizer(1, 2)
        hMain.Add(vCtrl, flag=wx.ALL | wx.EXPAND)
        hMain.Add(self.vList, flag=wx.ALL | wx.EXPAND)

        self.SetSizer(hMain)
        self.Fit()

        self.Bind(wx.EVT_BUTTON, self.OnSelectClicked, id=wx.ID_OK)
        self.Bind(wx.EVT_BUTTON, self.OnCancelClicked, id=wx.ID_CANCEL)
        self.vList.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnListItemSelected)

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)
        self.timer.Start(500)

    def CreateListCtrl(self, trans):
        vList = wx.ListCtrl(self, style=wx.LC_REPORT)
        vList.SetMinSize((340, 200))
        vList.InsertColumn(0, trans.get('dSelObj_id'), format=wx.LIST_FORMAT_RIGHT, width=40)
        vList.InsertColumn(1, trans.get('dSelObj_listName'), format=wx.LIST_FORMAT_LEFT, width=100)
        vList.InsertColumn(2, trans.get('dSelObj_listRA'), format=wx.LIST_FORMAT_LEFT, width=100)
        vList.InsertColumn(3, trans.get('dSelObj_listDEC'), format=wx.LIST_FORMAT_LEFT, width=100)
        return vList

    def CreateObjectPanel(self, trans):
        objProp = wx.FlexGridSizer(2, 2, 5, 5)
        objProp.Add(wx.StaticText(self, wx.ID_ANY, trans.get('dSelObj_name')), flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        objProp.Add(self.name, flag=wx.ALL | wx.EXPAND | wx.ALIGN_RIGHT)
        objProp.Add(wx.StaticText(self, wx.ID_ANY, trans.get('dSelObj_RA')), flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        objProp.Add(self.RA, flag=wx.ALL | wx.EXPAND | wx.ALIGN_RIGHT)
        objProp.Add(wx.StaticText(self, wx.ID_ANY, trans.get('dSelObj_DEC')), flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        objProp.Add(self.DEC, flag=wx.ALL | wx.EXPAND | wx.ALIGN_RIGHT)
        return objProp

    def update(self, event):
        userInput = self.name.GetValue().strip()

        if userInput != self.starName:
            self.starName = userInput
            self.RA.SetValue("")
            self.DEC.SetValue("")
            stars = self.controller.getStars(self.starName)
            self.fillList(stars)

    def fillList(self, stars):
        self.vList.DeleteAllItems()
        for star in stars:
            index = self.vList.InsertStringItem(sys.maxint, str(star['id']))
            self.vList.SetStringItem(index, 1, star['name'])
            self.vList.SetStringItem(index, 2, star['ra'])
            self.vList.SetStringItem(index, 3, star['dec'])

    def OnListItemSelected(self, event):
        id = self.getSelectedStarID()
        star = self.controller.getStarById(id)
        self.setNewStar(star)

    def getSelectedStarID(self):
        curItemId = self.vList.GetFirstSelected()
        item = self.vList.GetItem(curItemId, 0).GetText()
        return item

    def setNewStar(self, star):
        self.name.SetValue(star['name'])
        self.starName = star['name'].strip()
        self.RA.SetValue(star['ra'])
        self.DEC.SetValue(star['dec'])

    def OnSelectClicked(self, event):
        self.controller.setObject(self.name.GetValue(),self.RA.GetValue(),self.DEC.GetValue())
        self.EndModal(wx.ID_OK)
    def OnCancelClicked(self, event):
        self.EndModal(wx.ID_CANCEL)

