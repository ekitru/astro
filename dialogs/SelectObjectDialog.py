import wx
import astronomy

from dialogs.ObjectListDialog import ObjectListDialog

__author__ = 'kitru'

class SelectObjectListDialog(ObjectListDialog):
    def __init__(self, parent, id, controller):
        ObjectListDialog.__init__(self, parent, wx.ID_ANY, controller.trans.get('dSelObj_title'), controller)

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
            ObjectListDialog.UpdateOnTimer(self, event)

    def isCorrectCoordinates(self):
        """ Check correct values for RA and DEC """
        ra = self.RA.GetValue()
        dec = self.DEC.GetValue()
        return astronomy.checkCoordinates(dec, ra)

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

        if self.starManager.starExists(self.starName):
            self.controller.setObject(self.starName)
            self.EndModal(wx.ID_OK)
        else:
            confirm = wx.MessageDialog(self, caption=self.starName, message=self.codes.get('dSelObj_addQues'),
                                       style=wx.YES_NO | wx.YES_DEFAULT | wx.CENTER)
            if confirm.ShowModal() == wx.ID_YES:
                confirm.Destroy()
                self.starManager.saveStar(self.starName, self.RA.GetValue(), self.DEC.GetValue())
                self.controller.setObject(self.starName)
                self.EndModal(wx.ID_OK)
  