import wx
from gui.panels.SimplePanel import SimplePanel

__author__ = 'kitru'

class ObjectPanel(SimplePanel):
    """This panel represents selected object data (name and positions)
    Attributes:
        codes - Translation codes
    """
    def __init__(self, parent, id, codes):
        SimplePanel.__init__(self, parent, id)
        self.codes = codes
        comSizer = wx.StaticBoxSizer(wx.StaticBox(self, label=codes.get("pObject")), wx.VERTICAL)
        comSizer.Add(self.CreateCoordinatesGrid(codes), flag=wx.ALL, border=10)
        comSizer.Add(wx.StaticLine(self, wx.ID_ANY, style=wx.LI_HORIZONTAL), flag=wx.ALL | wx.EXPAND)
        comSizer.Add(self.CreateBottomPanel(codes), flag=wx.ALL | wx.EXPAND)
        self.SetSizer(comSizer)

    def CreateCoordinatesGrid(self, codes):
        """ return sizer for Object position mapping
        Attr:
            codes - translation codes
        """
        sizer = wx.GridSizer(4, 3, 5, 10)

        self.objectName = self.CreateField()
        self.objectOrigRA = self.CreateCoordinateField()
        self.objectCurrRA = self.CreateCoordinateField()
        self.objectOrigDEC = self.CreateCoordinateField()
        self.objectCurrDEC = self.CreateCoordinateField()

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
        """ Return sizer with control buttons
        Attr:
            codes - translation codes
        """
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.objAccess = self.CreateCoordinateField()

        objPos = self.CreateObjectPosition(codes)
        objStatus = wx.BoxSizer(wx.HORIZONTAL)
        objStatus.Add(self.CreateCaption(codes.get('pObjAccessible')), flag=wx.RIGHT | wx.ALIGN_RIGHT, border=10)
        objStatus.Add(self.objAccess, flag=wx.ALL | wx.ALIGN_CENTER, proportion=2)


        sizer.Add(objPos, flag=wx.LEFT | wx.RIGHT | wx.TOP, border=10)
        sizer.Add(objStatus, flag=wx.ALL | wx.EXPAND, border=10)
        return sizer

    def CreateObjectPosition(self, codes):
        """ Return sizer object position
        Attr:
            codes - translation codes
        """
        self.objAltitude = self.CreateCoordinateField()
        self.objAzimuth = self.CreateCoordinateField()
        self.objHourAngle = self.CreateCoordinateField()
        self.objRisingTime = self.CreateField()
        self.objSettingTime = self.CreateField()
        self.objExpositionTime = self.CreateField()

        sizer = wx.FlexGridSizer(2, 4, 5, 10)
        sizer.Add(self.CreateCaption(codes.get('pObjALT')), flag=wx.ALL | wx.ALIGN_RIGHT)
        sizer.Add(self.objAltitude, flag=wx.ALL | wx.ALIGN_CENTER)
        sizer.Add(self.CreateCaption(codes.get('pObjRise')), flag=wx.ALL | wx.ALIGN_RIGHT)
        sizer.Add(self.objRisingTime, flag=wx.ALL | wx.ALIGN_CENTER)
        sizer.Add(self.CreateCaption(codes.get('pObjAZIMUTH')), flag=wx.ALL | wx.ALIGN_RIGHT)
        sizer.Add(self.objAzimuth, flag=wx.ALL | wx.ALIGN_CENTER)
        sizer.Add(self.CreateCaption(codes.get('pObjSet')), flag=wx.ALL | wx.ALIGN_RIGHT)
        sizer.Add(self.objSettingTime, flag=wx.ALL | wx.ALIGN_CENTER)
        sizer.Add(self.CreateCaption(codes.get('pObjHA')), flag=wx.ALL | wx.ALIGN_RIGHT)
        sizer.Add(self.objHourAngle, flag=wx.ALL | wx.ALIGN_CENTER)
        sizer.Add(self.CreateCaption(codes.get('pObjExpos')), flag=wx.ALL | wx.ALIGN_RIGHT)
        sizer.Add(self.objExpositionTime, flag=wx.ALL | wx.ALIGN_CENTER)
        return sizer

    def update(self, controller):
        object = controller.object
        """Updates Objects name and coordinates """
        if object.isSelected():
            # show object data
            data = object.getData()
            self.objectName.SetLabel(data['name'])
            self.objectOrigRA.SetLabel(data['ra'])
            self.objectOrigDEC.SetLabel(data['dec'])
            # show object current coordinates
            coord = object.getCurrentPosition()
            self.objectCurrRA.SetLabel(coord['ra'])
            self.objectCurrDEC.SetLabel(coord['dec'])
            self.objAltitude.SetLabel(coord['alt'])
            self.objAzimuth.SetLabel(coord['az'])
            # show telescope position
            ha = object.getHA()
            self.objHourAngle.SetLabel(ha)
            # show observation times
            times = object.getRiseSetTimes()
            self.objRisingTime.SetLabel(times['rise'])
            self.objSettingTime.SetLabel(times['set'])
            # show exosition time
            exp = object.getExpositionTime()
            self.objExpositionTime.SetLabel(exp)

            accesibility = object.isAccessible()
            self.objAccess.SetLabel(self.codes.get(accesibility))
