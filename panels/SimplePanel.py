import wx
from os.path import join

__author__ = 'kitru'

class SimplePanel(wx.Panel):
    def __init__(self, parent=None, id=wx.ID_ANY):
        wx.Panel.__init__(self, parent, id)

    def CreateHeader(self, name):
        return self.CreateElement(name, wx.Font(10, wx.SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

    def CreateCaption(self, name):
        return self.CreateElement(name, wx.Font(10, wx.SWISS, wx.FONTSTYLE_SLANT, wx.FONTWEIGHT_LIGHT))

    def CreateField(self):
        element = self.CreateElement()
        element.SetMinSize(wx.Size(80, 20))
        return element

    def CreateCoordField(self):
        element = self.CreateElement()
        element.SetMinSize(wx.Size(80, 20))
        return element

    def CreateElement(self, name="", font=None):
        element = wx.StaticText(self, wx.ID_ANY, name)
        if font:
            element.SetFont(font)
        return element

    def CreateInputField(self, size=wx.DefaultSize):
        return wx.TextCtrl(self, id=wx.ID_ANY, size=size)

    def CreateButton(self, label="", font=None, size=wx.DefaultSize):
        speedSelButton = wx.Button(self, id=wx.ID_ANY, label=label, size=size)
        if font:
            speedSelButton.SetFont(font)
        return speedSelButton

    def CreateBitmapButton(self, name, file_type, size=wx.DefaultSize):
        path = join('resources', 'icons', name)
        bitmap = wx.Bitmap(path, file_type)
        return wx.BitmapButton(self, id=wx.ID_ANY, bitmap=bitmap, size=size)

    def CreateToggleButton(self, label="", font=None, size=wx.DefaultSize):
        toggleButton = wx.ToggleButton(self, id=wx.ID_ANY, label=label, size=size)
        if font:
            toggleButton.SetFont(font)
        return toggleButton

    #Sizes and Fonts
    def sizeSmall(self):
        return 30, 25

    def sizeLarge(self):
        return 85, 27

    def fontNorm(self):
        return wx.Font(10, wx.SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)

    def fontBold(self):
        return wx.Font(10, wx.SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)

    def bitmapType(self):
        return wx.BITMAP_TYPE_ICO