import wx

__author__ = 'kitru'

class SimplePanel(wx.Panel):
    def __init__(self, parent=None, ID=wx.ID_ANY):
        wx.Panel.__init__(self, parent, ID)

        #Sizes and Fonts
        self.BUTTON_SIZE_SMALL = (30,25)
        self.IN_FIELD_SIZE_NORMAL = (85,27)
        self.BUTTON_SIZE_LARGE = (85,27)
        self.BUTTON_FONT_NORMAL = wx.Font(10, wx.SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.BUTTON_FONT_BOLD = wx.Font(10, wx.SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)

    def CreateHeader(self, name):
        return self.CreateElement(name, wx.Font(10, wx.SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

    def CreateCaption(self, name):
        return self.CreateElement(name, wx.Font(10, wx.SWISS, wx.FONTSTYLE_SLANT, wx.FONTWEIGHT_LIGHT))

    def CreateField(self):
        return self.CreateElement()

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

    def CreateButton(self, label="",font=None, size=wx.DefaultSize):
        speedSelButton = wx.Button(self, id=wx.ID_ANY, label=label, size=size)
        if font:
            speedSelButton.SetFont(font)
        return speedSelButton

    def CreateBitmapButton(self, rel_path, file_type, size=wx.DefaultSize):
        bitmap = wx.Bitmap(rel_path, file_type)
        return wx.BitmapButton(self, id=wx.ID_ANY, bitmap=bitmap,size=size)

    def CreateToggleButton(self, label="", font=None ,size=wx.DefaultSize):
        toggleButton = wx.ToggleButton(self, id=wx.ID_ANY, label=label, size=size)
        if font:
            toggleButton.SetFont(font)
        return toggleButton
  