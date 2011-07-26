#!/usr/bin/python
# -*- coding: utf-8 -*-

# absolute.py

import wx

class Example(wx.Frame):
    def __init__(self, parent, title):
        super(Example, self).__init__(parent, title=title,
                                      )

        self.InitUI()
        self.Centre()
        self.Show()

    def InitUI(self):
        panel = wx.Panel(self, -1)

        menubar = wx.MenuBar()
        filem = wx.Menu()
        editm = wx.Menu()
        helpm = wx.Menu()

        menubar.Append(filem, '&File')
        menubar.Append(editm, '&Edit')
        menubar.Append(helpm, '&Help')
        self.SetMenuBar(menubar)

        hbox_common = wx.BoxSizer(wx.HORIZONTAL)
        vbox_control = wx.BoxSizer(wx.VERTICAL)
        vbox_starlist = wx.BoxSizer(wx.VERTICAL)
        wx.BoxSizer()

        hbox_common.Add(vbox_control, flag=wx.LEFT)
        hbox_common.Add(vbox_starlist, flag=wx.RIGHT)

        cap_position = wx.StaticText(panel, label="positions:")
        vbox_control.Add(cap_position, flag=wx.LEFT)
        caption = wx.StaticText(panel, label="Stars:")
        vbox_starlist.Add(caption, flag=wx.LEFT)
        self.SetAutoLayout(1)

if __name__ == '__main__':
    app = wx.App()
    Example(None, title='')
    app.MainLoop()
