import wx
import sys
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


class ObjectListDialog(wx.Dialog):
    """ implements simple dialog with star field and star list
    periodically list is updating by stars with similar names
    it also holds controlles and tranlastion instances and Bind some common events:
    OnOk, OnCancel, OnListItemSelected, OnListItemActivated
    """

    def __init__(self, parent, id, title, controller):
        wx.Dialog.__init__(self, parent, id, title, style=wx.CAPTION)
        self.controller = controller
        self.starManager = controller.star
        self.codes = controller.trans

        self.starName = ""
        self.list = StarList(self, self.codes)

        stars = self.starManager.getStars(self.starName)
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
        stars = self.starManager.getStars(self.GetStarName())
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
        return self.starManager.getStarByName(name)
  