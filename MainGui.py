# -*- coding: utf-8 -*-

import wx
from panels import *
from dialogs import *
from ids import *

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
        self.positioningPanel = PositionPanel(ID=ID_POSITIONING, **panelArgs)
        self.telescopePanel = TelescopePanel(ID=ID_TELESCOPE, **panelArgs)
        self.controlPanel = ControlPanel(ID=ID_CONTROLPANEL, **panelArgs)

        grid = wx.FlexGridSizer(1, 2, 10, 10)   #3,2,10,10
        gridColumn1 = wx.BoxSizer(wx.VERTICAL)
        gridColumn2 = wx.BoxSizer(wx.VERTICAL)

        gridColumn1.Add(self.objectPanel, flag=wx.ALL | wx.EXPAND)
        gridColumn1.Add(self.positioningPanel, flag=wx.ALL | wx.EXPAND)
        gridColumn1.Add(self.controlPanel, flag=wx.ALL | wx.EXPAND)

        gridColumn2.Add(self.timeDatePanel, flag=wx.ALL | wx.EXPAND)
        gridColumn2.Add(self.telescopePanel, flag=wx.ALL | wx.EXPAND)

        grid.Add(gridColumn1)
        grid.Add(gridColumn2)

        canvas = wx.BoxSizer(wx.VERTICAL)
        canvas.Add(grid, flag=wx.ALL | wx.EXPAND, border=10)
        self.SetSizer(canvas)
        self.Centre()

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)
        self.timer.Start(500)

        self.Bind(wx.EVT_BUTTON, self.OnButtonAutoManual, self.controlPanel.butAutoManual)
        self.Bind(wx.EVT_BUTTON, self.OnButtonMove, self.controlPanel.butMove)
        self.Bind(wx.EVT_BUTTON, self.OnButtonUp, self.controlPanel.butMovUpRA)
        self.Bind(wx.EVT_BUTTON, self.OnButtonDown, self.controlPanel.butMovDwnRA)
        self.Bind(wx.EVT_BUTTON, self.OnButtonLeft, self.controlPanel.butMovLftDEC)
        self.Bind(wx.EVT_BUTTON, self.OnButtonRight, self.controlPanel.butMovRhtDEC)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.OnButtonSelHour, self.controlPanel.butSelHour)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.OnButtonSelMin, self.controlPanel.butSelMin)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.OnButtonSelSec, self.controlPanel.butSelSec)
        self.Bind(wx.EVT_BUTTON, self.OnButtonIncFoc, self.controlPanel.butIncFoc)
        self.Bind(wx.EVT_BUTTON, self.OnButtonDecFoc, self.controlPanel.butDecFoc)


    #noinspection PyUnusedLocal
    def OnSelectObject(self, event):
        selObj = SelectObjectDialog(self, wx.ID_ANY, self.controller)
        selObj.ShowModal()
        selObj.Destroy()

    #noinspection PyUnusedLocal
    def OnEditObject(self, event):
        editObj = EditObjectDialog(self, wx.ID_ANY, self.controller)
        editObj.ShowModal()
        editObj.Destroy()

    #noinspection PyUnusedLocal
    def OnSettings(self, event):
        print('Settings')

    def OnButtonAutoManual(self, event):
        button = event.GetEventObject()
        if self.controller.autoControlSelected():
            self.controller.selectManualControl()
            button.SetLabel(self.trans.get('pCtrlMan'))
        else:
            self.controller.selectAutoControl()
            button.SetLabel(self.trans.get('pCtrlAuto'))

    def OnButtonMove(self, event):
        print('butMove')

    def OnButtonUp(self, event):
        print('butMovUpRA')

    def OnButtonDown(self, event):
        print('butMovDwnRA')

    def OnButtonLeft(self, event):
        print('butMovLftDEC')

    def OnButtonRight(self, event):
        print('butMovRhtDEC')

    def OnButtonSelHour(self, event):
        print('butSelHour')

    def OnButtonSelMin(self, event):
        print('butSelMin')

    def OnButtonSelSec(self, event):
        print('butSelSec')

    def OnButtonIncFoc(self, event):
        print('butIncFoc')

    def OnButtonDecFoc(self, event):
        print('butDecFoc')


    def update(self, event):
        self.objectPanel.update(self.controller)
        self.timeDatePanel.update(self.controller)
        self.positioningPanel.update(self.controller)
        self.controlPanel.update(self.controller)

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
