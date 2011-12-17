import wx
from core import astronomy

from gui.dialogs.ObjectListDialog import ObjectListDialog
from gui.panels.SimplePanel import SimplePanel

__author__ = 'kitru'

class EditObjectDialog(ObjectListDialog, SimplePanel):
    def __init__(self, parent, id, controller):
        ObjectListDialog.__init__(self, parent, wx.ID_ANY, 'dEditObj_title', controller)
        self.controller = controller
        self.codes = controller.codes

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
            ObjectListDialog.UpdateOnTimer(self, event)

    def OnListItemActivated(self, event):
        star = self.GetSelectedStar()
        dialog = UpdateStarDialog(self, self.controller.codes.get('dUpdateObj_title'), self.controller, star)
        dialog.ShowModal()
        dialog.Destroy()
        ObjectListDialog.OnListItemActivated(self, event)


    def OnListCharacter (self, event):
        if event.GetKeyCode() == wx.WXK_DELETE:
            event.Skip()
            index = self.list.GetNextItem(-1, state=wx.LIST_STATE_SELECTED)
            if index != -1:
                star = self.GetSelectedStar()
                response = self.askConfirmation(star)
                if response == wx.ID_YES:
                    self._starHolder.deleteStar(star)
                    self.list.DeleteItem(index)
                    self.list.Select(index)
        else:
            event.Skip()

    def OnAddClicked(self, event):
        dialog = AddStarDialog(self, self.controller.codes.get('dAddObj_title'), self.controller)
        dialog.ShowModal()
        dialog.Destroy()
        ObjectListDialog.OnListItemActivated(self, event)

    def askConfirmation(self, star):
        confirm = wx.MessageDialog(self, caption=star['name'], message=self.codes.get('dEditObj_confirm'),
                                       style=wx.YES_NO | wx.NO_DEFAULT | wx.CENTER | wx.ICON_QUESTION | wx.CAPTION)
        response = confirm.ShowModal()
        confirm.Destroy()
        return response


class AddStarDialog(wx.Dialog):
    def __init__(self, parent, title, controller):
        id = wx.ID_ANY
        wx.Dialog.__init__(self, parent, id, title, style=wx.CAPTION)
        self.starManager = controller.resources.dbStar
        self.codes = controller.codes
        self.name = wx.TextCtrl(self, size=(120, -1))
        self.name.SetFocus()
        self.RA = wx.TextCtrl(self, size=(120, -1))
        self.DEC = wx.TextCtrl(self, size=(120, -1))

        self.saveButton = wx.Button(self, id=wx.ID_ADD, label=self.codes.get("dAddObj_add"))
        self.cancelButton = wx.Button(self, id=wx.ID_CANCEL, label=self.codes.get("dAddObj_cancel"))
        buttons = wx.BoxSizer(wx.HORIZONTAL)
        buttons.Add(self.saveButton, flag=wx.ALL | wx.ALIGN_LEFT)
        buttons.Add(self.cancelButton, flag=wx.ALL | wx.ALIGN_RIGHT)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.CreateObjectPanel(self.codes), flag=wx.ALL | wx.EXPAND | wx.ALIGN_TOP, border=10)
        sizer.Add(buttons, flag=wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.ALIGN_BOTTOM, border=10)
        self.SetSizer(sizer)
        self.Fit()

        self.Bind(wx.EVT_BUTTON, self.OnSaveClicked, id=wx.ID_ADD)
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
        return astronomy.checkCoordinates(ra, dec) & (not self.starManager.starExists(name))

    def CheckField(self, event):
        event.Skip()
        if self.isCorrectInput():
            self.saveButton.Enable()
        else:
            self.saveButton.Disable()


    def OnSaveClicked(self, event):
        name = self.name.GetValue()
        ra = self.RA.GetValue()
        dec = self.DEC.GetValue()
        self.starManager.saveStar(name, ra, dec)
        self.EndModal(wx.ID_OK)

    def OnCancelClicked(self, event):
        event.Skip()
        self.EndModal(wx.ID_CANCEL)

class UpdateStarDialog(AddStarDialog):
    def __init__(self, title, parent, controller, star):
        AddStarDialog.__init__(self, title, parent, controller)
        self.name.SetValue(star['name'])
        self.name.Disable()
        self.RA.SetValue(star['ra'])
        self.DEC.SetValue(star['dec'])
        self.saveButton.SetLabel(self.codes.get('dUpdateObj_update'))

    def isCorrectInput(self):
        """ Check correct values for RA and DEC """
        ra = self.RA.GetValue()
        dec = self.DEC.GetValue()
        return astronomy.checkCoordinates(ra, dec )

    def OnSaveClicked(self, event):
        name = self.name.GetValue()
        ra = self.RA.GetValue()
        dec = self.DEC.GetValue()
        self.starManager.updateStar(name, ra, dec)
        self.EndModal(wx.ID_OK)
  