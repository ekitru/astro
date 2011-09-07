import wx
import sys
from panels import SimplePanel

__author__ = 'kitru'

class StarList(wx.ListCtrl):
    """ extended ListCtrl for showing stars in natural form (name, ra, dec). RA,DEC in readable form like HH:MM:SS """

    def __init__(self, parent, codes):
        wx.ListCtrl.__init__(self, parent, id=wx.ID_ANY, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.AdjustListControl(codes)

    def AdjustListControl(self, codes):
        self.SetMinSize((320, 200))
        self.InsertColumn(col=0, heading=codes.get('dSelObj_listName'), format=wx.LIST_FORMAT_LEFT, width=90)
        self.InsertColumn(col=1, heading=codes.get('dSelObj_listRA'), format=wx.LIST_FORMAT_LEFT, width=110)
        self.InsertColumn(col=2, heading=codes.get('dSelObj_listDEC'), format=wx.LIST_FORMAT_LEFT, width=110)

    def FillList(self, stars):
        """ fill control list with stars
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
    """ implements simple dialog with star field and star list
    periodically list is updating by stars with similar names
    it also holds controlles and tranlastion instances and Bind some common events:
    OnOk, OnCancel, OnListItemSelected, OnListItemActivated
    """

    def __init__(self, parent, id, title, controller):
        wx.Dialog.__init__(self, parent, id, title, style=wx.CAPTION)
        self.controller = controller
        self.codes = controller.trans

        self.starName = ""
        self.list = StarList(self, self.codes)

        stars = self.controller.getStars(self.starName)
        self.list.FillList(stars)

        self.Bind(wx.EVT_BUTTON, self.OnOkClicked, id=wx.ID_OK)
        self.Bind(wx.EVT_BUTTON, self.OnCancelClicked, id=wx.ID_CANCEL)

        self.list.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnListItemSelected)
        self.list.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnListItemActivated)

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.UpdateOnTimer, self.timer)
        self.timer.Start(500)

    def UpdateOnTimer(self, event):
        """ on timer reload list content  """
        self.ReloadList()

    def ReloadList(self):
        stars = self.controller.getStars(self.GetStarName())
        self.list.FillList(stars)

    def GetStarName(self):
        return self.starName.strip()

    def SetStarName(self, name):
        self.starName = name.strip()

    def OnOkClicked(self, event):
        self.EndModal(wx.ID_OK)

    def OnCancelClicked(self, event):
        self.EndModal(wx.ID_CANCEL)

    def OnListItemSelected(self, event): #item selection in list
        pass

    def OnListItemActivated(self, event): #double click or enter pressed
        self.ReloadList()

    def GetSelectedStar(self):
        name = self.list.GetSelectedStarName()
        return self.controller.getStarByName(name)


class SelectObjectDialog(SimpleObjectDialog):
    def __init__(self, parent, id, controller):
        SimpleObjectDialog.__init__(self, parent, wx.ID_ANY, controller.trans.get('dSelObj_title'), controller)

        self.text = wx.TextCtrl(self, size=(120, -1))
        self.text.SetFocus()
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

    def CreateObjectPanel(self, codes):
        grid = wx.FlexGridSizer(2, 2, 5, 5)
        grid.Add(wx.StaticText(self, wx.ID_ANY, codes.get('dSelObj_name')),
                 flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        grid.Add(self.text, flag=wx.ALL | wx.EXPAND | wx.ALIGN_RIGHT)
        grid.Add(wx.StaticText(self, wx.ID_ANY, codes.get('dSelObj_RA')),
                 flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        grid.Add(self.RA, flag=wx.ALL | wx.EXPAND | wx.ALIGN_RIGHT)
        grid.Add(wx.StaticText(self, wx.ID_ANY, codes.get('dSelObj_DEC')),
                 flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        grid.Add(self.DEC, flag=wx.ALL | wx.EXPAND | wx.ALIGN_RIGHT)
        return grid

    def UpdateOnTimer(self, event):
        self.selectButton.Enable(self.isCorrectCoordinates())

        userInput = self.text.GetValue().strip()
        if userInput != self.GetStarName():    #if new star name is entered update input fields and reread db
            self.SetStarName(userInput)
            self.RA.Clear()
            self.DEC.Clear()
            SimpleObjectDialog.UpdateOnTimer(self, event)

    def isCorrectCoordinates(self):
        """ Check correct values for RA and DEC """
        ra = self.RA.GetValue()
        dec = self.DEC.GetValue()
        return self.controller.checkCoordinates(dec, ra)

    def OnOkClicked(self, event):
        self.SelectStar()

    def OnListItemActivated(self, event):
        self.SelectStar()

    def OnListItemSelected(self, event):
        star = self.GetSelectedStar()
        self.SetNewStar(star)

    def SetNewStar(self, star):
        inName = star['name'].strip()
        self.text.SetValue(inName)
        self.starName = inName
        self.RA.SetValue(star['ra'])
        self.DEC.SetValue(star['dec'])

    def SelectStar(self):
        if not self.isCorrectCoordinates():
            return

        if self.controller.starExists(self.starName):
            self.controller.setObject(self.starName)
            self.EndModal(wx.ID_OK)
        else:
            confirm = wx.MessageDialog(self, caption=self.starName, message=self.codes.get('dSelObj_addQues'),
                                       style=wx.YES_NO | wx.YES_DEFAULT | wx.CENTER)
            if confirm.ShowModal() == wx.ID_YES:
                confirm.Destroy()
                self.controller.saveStar(self.starName, self.RA.GetValue(), self.DEC.GetValue())
                self.controller.setObject(self.starName)
                self.EndModal(wx.ID_OK)


class EditObjectDialog(SimpleObjectDialog, SimplePanel):
    def __init__(self, parent, id, controller):
        SimpleObjectDialog.__init__(self, parent, wx.ID_ANY, controller.trans.get('dEditObj_title'), controller)

        findBox = wx.BoxSizer(wx.HORIZONTAL)
        findBox.Add(self.CreateCaption(self.codes.get('dEditObj_find')), flag=wx.ALIGN_CENTER)
        self.text = wx.TextCtrl(self, size=(180, -1))
        self.text.SetFocus()
        findBox.Add(self.text, flag=wx.ALL | wx.EXPAND, border=10)

        addButton = wx.BoxSizer(wx.VERTICAL)
        addButton.Add(wx.Button(self, wx.ID_ADD, label=self.codes.get('dEditObj_add')), flag=wx.ALL | wx.EXPAND | wx.ALIGN_LEFT)
        cancelButton = wx.BoxSizer(wx.VERTICAL)
        cancelButton.Add(wx.Button(self, wx.ID_CANCEL, label=self.codes.get('dEditObj_cancel')), flag=wx.ALL | wx.EXPAND | wx.ALIGN_RIGHT)

        butSizer = wx.BoxSizer(wx.HORIZONTAL)
        butSizer.Add(addButton, flag=wx.EXPAND)
        butSizer.Add(cancelButton, flag=wx.EXPAND)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(findBox, flag=wx.LEFT | wx.ALIGN_TOP, border=10)
        sizer.Add(self.list, flag=wx.ALL | wx.EXPAND | wx.ALIGN_CENTER)
        sizer.Add(butSizer, flag=wx.ALIGN_BOTTOM | wx.EXPAND | wx.ALL, border=10)

        self.SetSizer(sizer)
        self.Fit()

        self.list.Bind(wx.EVT_KEY_DOWN, self.OnListCharacter)
        self.Bind(wx.EVT_BUTTON, self.OnAddClicked, id=wx.ID_ADD)


    def UpdateOnTimer(self, event):
        userInput = self.text.GetValue().strip()
        if userInput != self.GetStarName():    #if new star name is entered update input fields and reread db
            self.SetStarName(userInput)
            SimpleObjectDialog.UpdateOnTimer(self, event)

    def OnListItemActivated(self, event):
        star = self.GetSelectedStar()
        dialog = UpdateStarDialog(self, self.controller, star)
        dialog.ShowModal()
        dialog.Destroy()
        SimpleObjectDialog.OnListItemActivated(self, event)


    def OnListCharacter (self, event):
        if event.GetKeyCode() == wx.WXK_DELETE:
            event.Skip()
            index = self.list.GetNextItem(-1, state=wx.LIST_STATE_SELECTED)
            if index != -1:
                star = self.GetSelectedStar()
                response = self.askConfirmation(star)
                if response == wx.ID_YES:
                    self.controller.deleteStar(star)
                    self.list.DeleteItem(index)
        else:
            event.Skip()

    def OnAddClicked(self, event):
        dialog = AddStarDialog(self, self.controller)
        dialog.ShowModal()
        dialog.Destroy()
        SimpleObjectDialog.OnListItemActivated(self, event)

    def askConfirmation(self, star):
        confirm = wx.MessageDialog(self, caption=star['name'], message=self.codes.get('dEditObj_confirm'),
                                       style=wx.YES_NO | wx.NO_DEFAULT | wx.CENTER)
        response = confirm.ShowModal()
        confirm.Destroy()
        return response


class AddStarDialog(wx.Dialog):
    def __init__(self, parent, controller):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=controller.trans.get('dAddObj_title'), style=wx.CAPTION)
        self.controller = controller
        self.codes = controller.trans
        self.name = wx.TextCtrl(self, size=(120, -1))
        self.name.SetFocus()
        self.RA = wx.TextCtrl(self, size=(120, -1))
        self.DEC = wx.TextCtrl(self, size=(120, -1))

        self.saveButton = wx.Button(self, id=wx.ID_OK, label=self.codes.get("dAddObj_add"))
        self.cancelButton = wx.Button(self, id=wx.ID_CANCEL, label=self.codes.get("dAddObj_cancel"))
        buttons = wx.BoxSizer(wx.HORIZONTAL)
        buttons.Add(self.saveButton, flag=wx.ALL | wx.ALIGN_LEFT)
        buttons.Add(self.cancelButton, flag=wx.ALL | wx.ALIGN_RIGHT)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.CreateObjectPanel(self.codes), flag=wx.ALL | wx.EXPAND | wx.ALIGN_TOP, border=10)
        sizer.Add(buttons, flag=wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.ALIGN_BOTTOM, border=10)
        self.SetSizer(sizer)
        self.Fit()

        self.Bind(wx.EVT_BUTTON, self.OnSaveClicked, id=wx.ID_OK)
        self.Bind(wx.EVT_BUTTON, self.OnCancelClicked, id=wx.ID_CANCEL)

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.CheckField, self.timer)
        self.timer.Start(500)

    def CreateObjectPanel(self, codes):
        grid = wx.FlexGridSizer(2, 2, 5, 5)
        grid.Add(wx.StaticText(self, wx.ID_ANY, codes.get('dAddObj_name')),
                 flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        grid.Add(self.name, flag=wx.ALL | wx.EXPAND | wx.ALIGN_RIGHT)
        grid.Add(wx.StaticText(self, wx.ID_ANY, codes.get('dAddObj_ra')),
                 flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        grid.Add(self.RA, flag=wx.ALL | wx.EXPAND | wx.ALIGN_RIGHT)
        grid.Add(wx.StaticText(self, wx.ID_ANY, codes.get('dAddObj_dec')),
                 flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        grid.Add(self.DEC, flag=wx.ALL | wx.EXPAND | wx.ALIGN_RIGHT)
        return grid

    def isCorrectInput(self):
        """ Check correct values for RA and DEC """
        name = self.name.GetValue()
        ra = self.RA.GetValue()
        dec = self.DEC.GetValue()
        return self.controller.checkCoordinates(dec, ra) & (not self.controller.starExists(name))

    def CheckField(self, event):
        if self.isCorrectInput():
            self.saveButton.Enable()
        else:
            self.saveButton.Disable()


    def OnSaveClicked(self, event):
        name = self.name.GetValue()
        ra = self.RA.GetValue()
        dec = self.DEC.GetValue()
        star = self.controller.saveStar(name, ra, dec)
        self.EndModal(wx.ID_OK)

    def OnCancelClicked(self, event):
        self.EndModal(wx.ID_CANCEL)

class UpdateStarDialog(AddStarDialog):
    def __init__(self, parent, controller, star):
        AddStarDialog.__init__(self, parent, controller)
        self.name.SetValue(star['name'])
        self.name.Disable()
        self.RA.SetValue(star['ra'])
        self.DEC.SetValue(star['dec'])
        self.saveButton.SetLabel(self.codes.get('dUpdateObj_update'))

    def isCorrectInput(self):
        """ Check correct values for RA and DEC """
        name = self.name.GetValue()
        ra = self.RA.GetValue()
        dec = self.DEC.GetValue()
        return self.controller.checkCoordinates(dec, ra)

    def OnSaveClicked(self, event):
        name = self.name.GetValue()
        ra = self.RA.GetValue()
        dec = self.DEC.GetValue()
        star = self.controller.updateStar(name, ra, dec)
        self.EndModal(wx.ID_OK)
