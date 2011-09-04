import wx
import sys
from panels import SimplePanel

__author__ = 'kitru'

class StarList(wx.ListCtrl):
    def __init__(self, parent, codes):
        wx.ListCtrl.__init__(self, parent, id=wx.ID_ANY, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.AdjustListControl(codes)

    def AdjustListControl(self, codes):
        self.SetMinSize((320, 200))
        self.InsertColumn(col=0, heading=codes.get('dSelObj_listName'), format=wx.LIST_FORMAT_LEFT, width=90)
        self.InsertColumn(col=1, heading=codes.get('dSelObj_listRA'), format=wx.LIST_FORMAT_LEFT, width=110)
        self.InsertColumn(col=2, heading=codes.get('dSelObj_listDEC'), format=wx.LIST_FORMAT_LEFT, width=110)

    def FillList(self, stars):
        """ fill control list by stars with stars
         Attr:
            stars - dict('name','ra','dec') """
        self.DeleteAllItems()
        for star in stars:
            index = self.InsertStringItem(sys.maxint, star['name'])
            self.SetStringItem(index, 1, star['ra'])
            self.SetStringItem(index, 2, star['dec'])

    def GetSelectedStarName(self):
        curItemId = self.GetFirstSelected()
        item = self.GetItem(curItemId, 0).GetText()
        return item


class SimpleObjectDialog(wx.Dialog):
    def __init__(self, parent, id, title, controller):
        wx.Dialog.__init__(self, parent, id, title, style=wx.CAPTION)
        self.controller = controller
        self.codes = controller.trans

        self.selectedStar = ""
        self.list = StarList(self, self.codes)

        stars = self.controller.getStars(self.selectedStar)
        self.list.FillList(stars)

        self.Bind(wx.EVT_BUTTON, self.OnSelectClicked, id=wx.ID_OK)
        self.Bind(wx.EVT_BUTTON, self.OnCancelClicked, id=wx.ID_CANCEL)

        self.list.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnListItemSelected)
        self.list.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnListItemActived)

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.UpdateOnTimer, self.timer)
        self.timer.Start(500)

    def UpdateOnTimer(self, event):
        self.ReloadList()

    def ReloadList(self):
        stars = self.controller.getStars(self.GetSelectedStarName())
        self.list.FillList(stars)

    def GetSelectedStarName(self):
        return self.selectedStar.strip()

    def SetSelectedStarName(self, name):
        self.selectedStar = name.strip()

    def OnSelectClicked(self, event):
        self.EndModal(wx.ID_OK)

    def OnCancelClicked(self, event):
        self.EndModal(wx.ID_CANCEL)

    def OnListItemSelected(self, event):
        pass

    def OnListItemActived(self, event):
        pass



class SelectObjectDialog(SimpleObjectDialog):
    def __init__(self, parent, id, controller):
        SimpleObjectDialog.__init__(self, parent, wx.ID_ANY, controller.trans.get('dSelObj_title'), controller)

        self.name = wx.TextCtrl(self, size=(120, -1))
        self.name.SetFocus()
        self.RA = wx.TextCtrl(self, size=(120, -1))
        self.DEC = wx.TextCtrl(self, size=(120, -1))

        vCtrl = wx.BoxSizer(wx.VERTICAL)
        objProp = self.CreateObjectPanel(self.codes)
        vCtrl.Add(objProp, flag=wx.ALL | wx.ALIGN_RIGHT, border=5)

        ctrlButtons = wx.BoxSizer(wx.HORIZONTAL)
        self.selectButton = wx.Button(self, wx.ID_OK, label=self.codes.get('dSelObj_select'))
        self.selectButton.Disable()
        ctrlButtons.Add(self.selectButton, flag=wx.ALIGN_BOTTOM)
        ctrlButtons.Add(wx.Button(self, wx.ID_CANCEL, label=self.codes.get('dSelObj_cancel')), flag=wx.ALIGN_BOTTOM)
        vCtrl.Add(ctrlButtons, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)

        hMain = wx.FlexGridSizer(1, 2)
        hMain.Add(vCtrl, flag=wx.ALL | wx.EXPAND)
        hMain.Add(self.list, flag=wx.ALL | wx.EXPAND)

        self.SetSizer(hMain)
        self.Fit()

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.UpdateOnTimer, self.timer)
        self.timer.Start(500)


    def CreateObjectPanel(self, codes):
        objProp = wx.FlexGridSizer(2, 2, 5, 5)
        objProp.Add(wx.StaticText(self, wx.ID_ANY, codes.get('dSelObj_name')),
                    flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        objProp.Add(self.name, flag=wx.ALL | wx.EXPAND | wx.ALIGN_RIGHT)
        objProp.Add(wx.StaticText(self, wx.ID_ANY, codes.get('dSelObj_RA')),
                    flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        objProp.Add(self.RA, flag=wx.ALL | wx.EXPAND | wx.ALIGN_RIGHT)
        objProp.Add(wx.StaticText(self, wx.ID_ANY, codes.get('dSelObj_DEC')),
                    flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        objProp.Add(self.DEC, flag=wx.ALL | wx.EXPAND | wx.ALIGN_RIGHT)
        return objProp

    def UpdateOnTimer(self, event):
        self.selectButton.Enable(self.isCorrectInput())

        userInput = self.name.GetValue().strip()
        if userInput != self.GetSelectedStarName():    #if new star name is entered update input fields and reread db
            self.SetSelectedStarName(userInput)
            self.RA.SetValue("")
            self.DEC.SetValue("")
            SimpleObjectDialog.UpdateOnTimer(self, event)

    def isCorrectInput(self):
        """ Check correct values for RA and DEC """
        ra = self.RA.GetValue()
        dec = self.DEC.GetValue()
        return self.controller.checkHours(ra) and self.controller.checkDegrees(dec)

    def OnSelectClicked(self, event):
        self.SetSelectedStar()

    def OnListItemSelected(self, event):
        name = self.list.GetSelectedStarName()
        star = self.controller.getStarByName(name)
        self.SetNewStar(star)

    def SetNewStar(self, star):
        inName = star['name'].strip()
        self.name.SetValue(inName)
        self.selectedStar = inName
        self.RA.SetValue(star['ra'])
        self.DEC.SetValue(star['dec'])

    def OnListItemActived(self, event):
        self.SetSelectedStar()

    def SetSelectedStar(self):
        if self.controller.isStarExist(self.selectedStar):
            self.controller.setObject(self.selectedStar)
            self.EndModal(wx.ID_OK)
        else:
            confirm = wx.MessageDialog(self, caption=self.selectedStar, message=self.codes.get('dSelObj_addQues'),
                                       style=wx.YES_NO | wx.YES_DEFAULT | wx.CENTER)
            if confirm.ShowModal() == wx.ID_YES:
                confirm.Destroy()
                self.controller.saveStar(self.selectedStar, self.RA.GetValue(), self.DEC.GetValue())
                self.controller.setObject(self.selectedStar)
                self.EndModal(wx.ID_OK)


class EditObjectDialog(SimpleObjectDialog, SimplePanel):
    def __init__(self, parent, id, controller):
        SimpleObjectDialog.__init__(self, parent, wx.ID_ANY, controller.trans.get('dEditObj_title'), controller)

        findBox = wx.BoxSizer(wx.HORIZONTAL)
        findBox.Add(self.CreateCaption(self.codes.get('dEditObj_find')), flag=wx.ALIGN_LEFT| wx.ALIGN_CENTER)
        self.text = wx.TextCtrl(self, size=(180, -1))
        self.text.SetFocus()
        findBox.Add(self.text, flag=wx.ALL | wx.EXPAND, border=10)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(findBox, flag=wx.LEFT, border=10)
        sizer.Add(self.list, flag=wx.ALL | wx.EXPAND | wx.ALIGN_CENTER)
        butSizer = wx.BoxSizer(wx.HORIZONTAL)
        butSizer.Add(wx.Button(self, wx.ID_CANCEL, label=self.codes.get('dEditObj_cancel')),
                     flag=wx.EXPAND | wx.ALL | wx.ALIGN_RIGHT)
        sizer.Add(butSizer, flag=wx.ALIGN_BOTTOM | wx.EXPAND)

        self.SetSizer(sizer)
        self.Fit()

        self.list.Bind(wx.EVT_KEY_DOWN, self.OnListCharacter)


    def OnListItemSelected(self, event):
        name = self.list.GetSelectedStarName()
        star = self.controller.getStarByName(name)
        print('selected star', star)


    def UpdateOnTimer(self, event):
        userInput = self.text.GetValue().strip()
        if userInput != self.GetSelectedStarName():    #if new star name is entered update input fields and reread db
            self.SetSelectedStarName(userInput)
            SimpleObjectDialog.UpdateOnTimer(self, event)



    def OnListCharacter (self, event):
        print "list character"
        if event.GetKeyCode() == wx.WXK_DELETE:
            print 'DELETE'
            event.Skip()
            index = self.list.GetNextItem(-1, state = wx.LIST_STATE_SELECTED )
            if index!=-1:
                self.list.DeleteItem ( index)
        else:
            print 'something'
            event.Skip()

