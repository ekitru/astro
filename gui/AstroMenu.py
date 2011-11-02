import wx
from gui.dialogs import SelectObjectDialog, EditObjectDialog, MessageDialog, LogsDialog, SettingsDialog
from ids import *

__author__ = 'kitru'

class AstroMenu(wx.MenuBar):
    """ Creates menu and reaction for menu item activization  """

    def __init__(self, controller):
        wx.MenuBar.__init__(self)
        self._controller = controller
        self._resources = controller.getResources()
        self._codes = controller.getResources().getCodes()

        objMenu = self.CreateObjectMenu(self._codes)
        toolsMenu = self.CreateToolsMenu(self._codes)

        self.Append(menu=objMenu, title=self._codes.get('mObj'))
        self.Append(menu=toolsMenu, title=self._codes.get('mTools'))

    def OnSelectObject(self, event):
        """ Select object from DB, also allows to add new object """
        event.Skip(False)
        dialog = SelectObjectDialog(self, self._resources)
        ret = dialog.ShowModal()
        dialog.Destroy()

        if ret == wx.ID_OK:
            self._controller.forceLog()

    def OnEditObject(self, event):
        """ Working with DB objects: add, update, delete """
        event.Skip(False)
        self.showDial(EditObjectDialog)

    def OnMessage(self, event):
        """ Allows to setup new observation message (comment) """
        event.Skip(False)
        ret = self.showDial(MessageDialog)
        if ret == wx.ID_OK:
            print('updated msg')
            self._controller.forceLog()

    def OnLogs(self, event):
        """ Shows observation logs """
        event.Skip(False)
        self.showDial(LogsDialog)

    def OnSettings(self, event):
        """ Give opportunities to change program default setups, like language or connection parameters """
        event.Skip(False)
        dialog = SettingsDialog(self, wx.ID_ANY, self._codes, self._controller)
        dialog.ShowModal()
        dialog.Destroy()

    def showDial(self, Dialog):
        """ Perform dialog opening and closing
        Attr:
            Dialog(wx.Dialog) class object
        """
        dialog = Dialog(self, wx.ID_ANY, self._controller)
        ret = dialog.ShowModal()
        dialog.Destroy()
        return ret


    def CreateObjectMenu(self, trans):
        """ Object sub items: Select object, Edit object """
        menu = wx.Menu()
        self.selectObj = wx.MenuItem(menu, ID_SELOBJ_DIALOG, text=trans.get('smSelObj') + '\tctrl+o',
                                     help=trans.get('smSelObjHelp'))
        self.editObj = wx.MenuItem(menu, ID_EDITOBJ_DIALOG, text=trans.get('smEditObj') + '\tctrl+e',
                                   help=trans.get('smEditObjHelp'))
        menu.AppendItem(self.selectObj)
        menu.AppendItem(self.editObj)
        return menu

    def CreateToolsMenu(self, trans):
        """ Tools sub items: message, logs, settings """
        menu = wx.Menu()

        self.message = wx.MenuItem(menu, ID_MSG_DIALOG, text=trans.get('smMessage') + '\tctrl+m',
                                   help=trans.get('smMessageHelp'))
        menu.AppendItem(self.message)

        self.message = wx.MenuItem(menu, ID_LOGS_DIALOG, text=trans.get('smLogs') + '\tctrl+l',
                                   help=trans.get('smLogsHelp'))
        menu.AppendItem(self.message)

        self.settings = wx.MenuItem(menu, ID_SETTINGS_DIALOG, text=trans.get('smSettings') + '\tctrl+s',
                                    help=trans.get('smSettingsHelp'))
        menu.AppendItem(self.settings)
        return menu

  