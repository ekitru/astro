import wx
from panels.SimplePanel import SimplePanel

__author__ = 'kitru'

class ObjectPanel(SimplePanel):
    """This panel represents selected object data (name and positions)
    Attributes:
        codes - Translation codes
    """
    def __init__(self, parent, ID=wx.ID_ANY, codes=None):
        SimplePanel.__init__(self, parent, ID)

        comSizer = wx.StaticBoxSizer(wx.StaticBox(self, label=codes.get("pObject")), wx.VERTICAL)
        comSizer.Add(self.CreateCoordinatesGrid(codes), flag=wx.ALL, border=10)
        comSizer.Add(wx.StaticLine(self, wx.ID_ANY, style=wx.LI_HORIZONTAL), flag=wx.ALL | wx.EXPAND)
        comSizer.Add(self.CreateBottomPanel(codes), flag=wx.ALL | wx.EXPAND)
        self.SetSizer(comSizer)

    def CreateCoordinatesGrid(self, codes):
        sizer = wx.GridSizer(4, 3, 5, 10)

        self.objectName = self.CreateField()
        self.objectOrigRA = self.CreateCoordField()
        self.objectCurrRA = self.CreateCoordField()
        self.objectOrigDEC = self.CreateCoordField()
        self.objectCurrDEC = self.CreateCoordField()

        sizer.Add(self.CreateCaption(codes.get('pObjName')), flag=wx.ALL | wx.ALIGN_RIGHT)
        sizer.Add(self.objectName, flag=wx.ALL | wx.EXPAND | wx.CENTER)
        sizer.Add(self.CreateField())

        sizer.Add(self.CreateField())
        sizer.Add(self.CreateCaption(codes.get('pObjEpoch')), flag=wx.ALL | wx.ALIGN_CENTER_HORIZONTAL)
        sizer.Add(self.CreateCaption(codes.get('pObjNow')), flag=wx.ALL | wx.ALIGN_CENTER_HORIZONTAL)
        sizer.Add(self.CreateCaption(codes.get('pObjRA')), flag=wx.ALL | wx.ALIGN_RIGHT)
        sizer.Add(self.objectOrigRA, flag=wx.ALL | wx.ALIGN_CENTER)
        sizer.Add(self.objectCurrRA, flag=wx.ALL | wx.ALIGN_CENTER)

        sizer.Add(self.CreateCaption(codes.get('pObjDEC')), flag=wx.ALL | wx.ALIGN_RIGHT)
        sizer.Add(self.objectOrigDEC, flag=wx.ALL | wx.ALIGN_CENTER)
        sizer.Add(self.objectCurrDEC, flag=wx.ALL | wx.ALIGN_CENTER)
        return sizer

    def CreateBottomPanel(self, codes):
        sizer = wx.BoxSizer(wx.VERTICAL)

        objPos = self.CreateObjectPosition(codes)
        sizer.Add(objPos, flag=wx.ALL, border=10)

        return sizer

    def CreateObjectPosition(self, codes):
        self.objAltitude = self.CreateCoordField()
        self.objHourAngle = self.CreateCoordField()
        self.objRisingTime = self.CreateField()
        self.objSettingTime = self.CreateField()

        sizer = wx.FlexGridSizer(2, 4, 5, 10)
        sizer.Add(self.CreateCaption(codes.get('pObjALT')), flag=wx.ALL | wx.ALIGN_RIGHT)
        sizer.Add(self.objAltitude, flag=wx.ALL | wx.ALIGN_CENTER)
        sizer.Add(self.CreateCaption(codes.get('pObjRise')), flag=wx.ALL | wx.ALIGN_RIGHT)
        sizer.Add(self.objRisingTime, flag=wx.ALL | wx.ALIGN_CENTER)
        sizer.Add(self.CreateCaption(codes.get('pObjHA')), flag=wx.ALL | wx.ALIGN_RIGHT)
        sizer.Add(self.objHourAngle, flag=wx.ALL | wx.ALIGN_CENTER)
        sizer.Add(self.CreateCaption(codes.get('pObjSet')), flag=wx.ALL | wx.ALIGN_RIGHT)
        sizer.Add(self.objSettingTime, flag=wx.ALL | wx.ALIGN_CENTER)
        return sizer

    def update(self, controller):
        """Updates Objects name and coordinates
        """

        object = controller.getObject()
        data = object.getData()

        self.objectName.SetLabel(data['name'])
        self.objectOrigRA.SetLabel(data['ra'])
        self.objectOrigDEC.SetLabel(data['dec'])

        position = object.getCurrentPosition()
        self.objectCurrRA.SetLabel(position['ra'])
        self.objectCurrDEC.SetLabel(position['dec'])
        self.objAltitude.SetLabel(position['alt'])
        self.objHourAngle.SetLabel(position['ha'])
        self.objRisingTime.SetLabel(position['rise'])
        self.objSettingTime.SetLabel(position['set'])
  