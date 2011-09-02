# -*- coding: utf-8 -*-

import wx
from dialogs import SelectObjectDiag
from ids import *
from panels import TimeDatePanel, ObjectPanel, PositioningPanel, TelescopePanel
from PlcGui import PlcGui

class MainGui(wx.Frame):
    def __init__(self, parent, title, controller):
        super(MainGui, self).__init__(parent, title=title,
                                      size=(706, 388))
        #        InspectionTool().Show()
        self.controller = controller
        self.trans = self.controller.trans

        self.SetMenuBar(AstroMenu(self.trans))

        self.Bind(wx.EVT_MENU, self.OnSelectObject, id=ID_SELOBJ)
        self.Bind(wx.EVT_MENU, self.OnEditObject, id=ID_EDITOBJ)
        self.Bind(wx.EVT_MENU, self.OnSettings, id=ID_SETTINGS)

        self.CreateStatusBar()
        self.SetStatusText('Program starts')

        panelArgs = {"parent": self, "codes": self.trans}

        self.objectPanel = ObjectPanel(ID=ID_OBJPANEL, **panelArgs)
        self.timeDatePanel = TimeDatePanel(ID=ID_TIMEPANEL, **panelArgs)
        self.positioningPanel = PositioningPanel(ID=ID_POSITIONING, **panelArgs)
        self.telescopePanel = TelescopePanel(ID=ID_TELESCOPE, **panelArgs)

        grid = wx.FlexGridSizer(2, 2, 10, 10)
        grid.Add(self.objectPanel, flag=wx.ALL | wx.EXPAND)
        grid.Add(self.positioningPanel, flag=wx.ALL | wx.EXPAND)
        grid.Add(self.timeDatePanel, flag=wx.ALL | wx.EXPAND)

        grid.Add(self.telescopePanel, flag=wx.ALL | wx.EXPAND)

        canvas = wx.BoxSizer(wx.VERTICAL)
        canvas.Add(grid, flag=wx.ALL | wx.EXPAND, border=10)
        self.SetSizer(canvas)
        self.Centre()

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)
        self.timer.Start(500)

        self.Bind(wx.EVT_BUTTON, self.OnTakeCtrlButton, self.positioningPanel.control)
        self.Bind(wx.EVT_CLOSE, self.OnMainGuiClose)

    #noinspection PyUnusedLocal
    def OnSelectObject(self, event):
        selObj = SelectObjectDiag(None, wx.ID_ANY, self.controller)
        selObj.ShowModal()
        selObj.Destroy()

    #noinspection PyUnusedLocal
    def OnEditObject(self, event):
        print('Edit object')

    #noinspection PyUnusedLocal
    def OnSettings(self, event):
        print('Settings')

    def OnTakeCtrlButton(self,event):
        takeCtrlButton = event.GetEventObject()
        if not hasattr(self, "plcGui"):
            self.plcGui = PlcGui(None,"PLC Control")
        elif self.plcGui is None:
            self.plcGui = PlcGui(None,"PLC Control")

        if takeCtrlButton.GetLabel() == "Take Control":
            takeCtrlButton.SetLabel("Release Control")
            self.plcGui.Show()
        else:
            takeCtrlButton.SetLabel("Take Control")
            self.plcGui.Hide()

    def OnMainGuiClose(self,event):
        if hasattr(self, "plcGui") and self.plcGui is not None:
            self.plcGui.Destroy()
        self.Destroy()

    def resetStateOfPositioningPanel(self):
        self.positioningPanel.control.SetLabel("Take Control")
        self.plcGui = None

    def update(self, event):
        selStar = self.getSelectedStar(self.controller)
        self.objectPanel.update(*selStar)
        self.timeDatePanel.update(self.controller.mechanics.getCurrentTimeDate())
        self.positioningPanel.update()
        self.Layout()
        self.Fit()
        self.Show()

    #noinspection PyUnusedLocal
    def update(self, event):
        self.objectPanel.update(self.controller)
        self.timeDatePanel.update(self.controller)
        self.positioningPanel.update(self.controller)

        self.Layout()
        self.Fit()
        self.Show()


class AstroMenu(wx.MenuBar):
    def __init__(self, trans):
        wx.MenuBar.__init__(self)

        objMenu = self.CreateObjectMenu(trans)
        toolsMenu = self.CreateToolsMenu(trans)

        self.Append(menu=objMenu, title=trans.get('mObj'))
        self.Append(menu=toolsMenu, title=trans.get('mTools'))

    def CreateObjectMenu(self, trans):
        menu = wx.Menu()
        self.selectObj = wx.MenuItem(menu, ID_SELOBJ, text=trans.get('smSelObj') + '\tctrl+o',
                                     help=trans.get('smSelObjHelp'))
        self.editObj = wx.MenuItem(menu, ID_EDITOBJ, text=trans.get('smEditObj') + '\tctrl+e',
                                   help=trans.get('smEditObjHelp'))
        menu.AppendItem(self.selectObj)
        menu.AppendItem(self.editObj)
        return menu

    def CreateToolsMenu(self, trans):
        menu = wx.Menu()
        self.settings = wx.MenuItem(menu, ID_SETTINGS, text=trans.get('smSettings') + '\tctrl+s',
                                    help=trans.get('smSettingsHelp'))
        menu.AppendItem(self.settings)
        return menu
