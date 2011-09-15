# -*- coding: utf-8 -*-

import wx
from panels import *
from dialogs import *
from ids import *

class MainGui(wx.Frame):
    """ Main GUI class, includes all panels and dialogs with Binding for calls  """

    def __init__(self, parent, title, controller):
        super(MainGui, self).__init__(parent, title=title,
                                      size=(706, 388))
        #        InspectionTool().Show()
        self.controller = controller

        panelArgs = {"parent": self, "codes": controller.trans}

        self.objectPanel = ObjectPanel(ID=ID_OBJPANEL, **panelArgs)
        self.timeDatePanel = TimeDatePanel(ID=ID_TIMEPANEL, **panelArgs)
        self.positioningPanel = PositionPanel(ID=ID_POSITIONING, **panelArgs)
        self.telescopePanel = TelescopePanel(ID=ID_TELESCOPE, **panelArgs)
        self.manualSetpointPanel = ManualSetpointPanel(controller=self.controller, ID=ID_MANUALSETPOINTPANEL, **panelArgs)
        self.controlModePanel = ControlModePanel(controller=self.controller, ID=ID_CONTROLMODEPANEL, **panelArgs)

        gridColumn1 = wx.BoxSizer(wx.VERTICAL)

        gridColumn1.Add(self.objectPanel, flag=wx.ALL | wx.EXPAND)
        gridColumn1.Add(self.positioningPanel, flag=wx.ALL | wx.EXPAND)
        gridColumn1.AddSpacer(10)
        gridColumn1.Add(self.controlModePanel, flag=wx.ALL | wx.EXPAND)
        gridColumn1.AddSpacer(5)
        gridColumn1.Add(self.manualSetpointPanel, flag=wx.ALL | wx.EXPAND)
        gridColumn2 = wx.BoxSizer(wx.VERTICAL)

        gridColumn2.Add(self.timeDatePanel, flag=wx.ALL | wx.EXPAND)
        gridColumn2.Add(self.telescopePanel, flag=wx.ALL | wx.EXPAND)

        grid = wx.FlexGridSizer(1, 2, 10, 10)   #3,2,10,10
        grid.Add(gridColumn1)
        grid.Add(gridColumn2)

        canvas = wx.BoxSizer(wx.VERTICAL)
        canvas.Add(grid, flag=wx.ALL | wx.EXPAND, border=10)

        self.SetSizer(canvas)
        self.Centre()

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)
        self.timer.Start(500)

        menu = AstroMenu(self.controller)
        self.SetMenuBar(menu)

        self.Bind(wx.EVT_MENU, menu.OnSelectObject, id=ID_SELOBJ)
        self.Bind(wx.EVT_MENU, menu.OnEditObject, id=ID_EDITOBJ)

        self.Bind(wx.EVT_MENU, menu.OnMessage, id=ID_MESSAGE)
        self.Bind(wx.EVT_MENU, menu.OnLogs, id=ID_LOGS)
        self.Bind(wx.EVT_MENU, menu.OnSettings, id=ID_SETTINGS)

        self.CreateStatusBar()
        self.SetStatusText('Program starts')


    def update(self, event):
        """ Updates panels view """
        self.controller.updateSetPoint()
        self.objectPanel.update(self.controller)
        self.timeDatePanel.update(self.controller)
        self.positioningPanel.update(self.controller)
        self.manualSetpointPanel.update(self.controller)
        self.controlModePanel.update(self.controller)

        self.Layout()
        self.Fit()
        self.Show()


class AstroMenu(wx.MenuBar):
    """ Creates menu and reaction for menu item activization  """

    def __init__(self, controller):
        wx.MenuBar.__init__(self)
        self.controller = controller

        objMenu = self.CreateObjectMenu(controller.trans)
        toolsMenu = self.CreateToolsMenu(controller.trans)

        self.Append(menu=objMenu, title=controller.trans.get('mObj'))
        self.Append(menu=toolsMenu, title=controller.trans.get('mTools'))

    def OnSelectObject(self, event):
        """ Select object from DB, also allows to add new object """

        self.showDial(SelectObjectDialog)

    def OnEditObject(self, event):
        """ Working with DB objects: add, update, delete """
        self.showDial(EditObjectDialog)

    def OnMessage(self, event):
        """ Allows to setup new observation message (comment) """
        self.showDial(MessageDialog)

    def OnLogs(self, event):
        """ Shows observation logs """
        self.showDial(LogsDialog)

    def OnSettings(self, event):
        """ Give opportunities to change program default setups, like language or connection parameters """
        self.showDial(SettingsDialog)

    def showDial(self, Dialog):
        """ Perform dialog opening and closing
        Attr:
            Dialog(wx.Dialog) class object
        """
        dialog = Dialog(self, wx.ID_ANY, self.controller)
        dialog.ShowModal()
        dialog.Destroy()


    def CreateObjectMenu(self, trans):
        """ Object sub items: Select object, Edit object """
        menu = wx.Menu()
        self.selectObj = wx.MenuItem(menu, ID_SELOBJ, text=trans.get('smSelObj') + '\tctrl+o',
                                     help=trans.get('smSelObjHelp'))
        self.editObj = wx.MenuItem(menu, ID_EDITOBJ, text=trans.get('smEditObj') + '\tctrl+e',
                                   help=trans.get('smEditObjHelp'))
        menu.AppendItem(self.selectObj)
        menu.AppendItem(self.editObj)
        return menu

    def CreateToolsMenu(self, trans):
        """ Tools sub items: message, logs, settings """
        menu = wx.Menu()

        self.message = wx.MenuItem(menu, ID_MESSAGE, text=trans.get('smMessage') + '\tctrl+m',
                                   help=trans.get('smMessageHelp'))
        menu.AppendItem(self.message)

        self.message = wx.MenuItem(menu, ID_LOGS, text=trans.get('smLogs') + '\tctrl+l',
                                   help=trans.get('smLogsHelp'))
        menu.AppendItem(self.message)

        self.settings = wx.MenuItem(menu, ID_SETTINGS, text=trans.get('smSettings') + '\tctrl+s',
                                    help=trans.get('smSettingsHelp'))
        menu.AppendItem(self.settings)
        return menu
