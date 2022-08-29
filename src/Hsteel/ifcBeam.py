import ifcopenshell

from src.comon.comon import *
from src.comon.ifcProject import ifcProject

class ifcBeam():

    def __init__(self, ifcProject: ifcProject):
        self.ifc = ifcProject

    def CreateBeam(self ,Container, Name , section , L , position , direction):
        B1 = self.ifc.file.createIfcBeam(create_guid(), self.ifc.owner_hist , Name)
        B1.ObjectType ='beam'

        B1_Point =self.ifc.file.createIfcCartesianPoint ( position )
        B1_Axis2Placement = self.ifc.file.createIfcAxis2Placement3D(B1_Point)
        B1_Axis2Placement.Axis = self.ifc.file.createIfcDirection(direction)
        B1_Axis2Placement.RefDirection =self.ifc.file.createIfcDirection(Z)

        B1_Placement = self.ifc.file.createIfcLocalPlacement(Container.ObjectPlacement,B1_Axis2Placement)
        B1.ObjectPlacement=B1_Placement

        B1_ExtrudePlacement = self.ifc.file.createIfcAxis2Placement3D(self.ifc.file.createIfcCartesianPoint ( (0.,0.,0.) )   )

        B1_Extruded=self.ifc.file.createIfcExtrudedAreaSolid()
        B1_Extruded.SweptArea=section
        B1_Extruded.Position=B1_ExtrudePlacement
        B1_Extruded.ExtrudedDirection = self.ifc.file.createIfcDirection(Z)
        B1_Extruded.Depth = L

        B1_Repr=self.ifc.file.createIfcShapeRepresentation()
        B1_Repr.ContextOfItems=self.ifc.context
        B1_Repr.RepresentationIdentifier = 'Body'
        B1_Repr.RepresentationType = 'SweptSolid'
        B1_Repr.Items = [B1_Extruded]

        B1_DefShape=self.ifc.file.createIfcProductDefinitionShape()
        B1_DefShape.Representations=[B1_Repr]
        B1.Representation=B1_DefShape

        Flr1_Container = self.ifc.file.createIfcRelContainedInSpatialStructure(create_guid(), self.ifc.owner_hist)
        Flr1_Container.RelatedElements=[B1]
        Flr1_Container.RelatingStructure= Container



    def add_Beam(self, L, D, W, tf, tw, amount, interval, T, floor1):

        section1 = I_Section(self.ifc.file, W=W ,D=D , tw=tw , tf=tf  , r = 0)

        dy = ((float(amount)-1.0) * interval / 2.0)
        for i in range(int(amount)):

            self.CreateBeam(floor1, Name='Beam-floor1-B{}'.format(i) ,section= section1 ,
                    L=L ,position=(0.0, dy ,0.0) , direction=(1.0,0.0,0.0))

            dy -= interval



def I_Section(ifc_file, W ,D , tw , tf  , r):
    B1_Axis2Placement2D =ifc_file.createIfcAxis2Placement2D(
                        ifc_file.createIfcCartesianPoint( (0.,0.) ) )

    B1_AreaProfile = ifc_file.createIfcIShapeProfileDef('AREA')
    B1_AreaProfile.Position = B1_Axis2Placement2D
    B1_AreaProfile.OverallWidth = W
    B1_AreaProfile.OverallDepth = D
    B1_AreaProfile.WebThickness = tw
    B1_AreaProfile.FlangeThickness = tf
    B1_AreaProfile.FilletRadius=r
    return B1_AreaProfile


def L_Section(ifc_file, W ,D , t   , r):
    B1_Axis2Placement2D =ifc_file.createIfcAxis2Placement2D(
                        ifc_file.createIfcCartesianPoint( (0.,0.) ) )

    B1_AreaProfile = ifc_file.createIfcLShapeProfileDef('AREA')
    B1_AreaProfile.Position = B1_Axis2Placement2D
    B1_AreaProfile.Width = W
    B1_AreaProfile.Depth = D
    B1_AreaProfile.Thickness = t

    B1_AreaProfile.FilletRadius=r
    return B1_AreaProfile

def U_Section(ifc_file, W ,D , tw  , tf  , r):
    B1_Axis2Placement2D =ifc_file.createIfcAxis2Placement2D(
                        ifc_file.createIfcCartesianPoint( (0.,0.) ) )

    B1_AreaProfile = ifc_file.createIfcUShapeProfileDef('AREA')
    B1_AreaProfile.Position = B1_Axis2Placement2D
    B1_AreaProfile.FlangeWidth = W
    B1_AreaProfile.Depth = D
    B1_AreaProfile.WebThickness = tw
    B1_AreaProfile.FlangeThickness = tf
    B1_AreaProfile.FilletRadius=r
    B1_AreaProfile.EdgeRadius=r*0.5
    return B1_AreaProfile

def Rect_Section(ifc_file, b, h):
    B1_Axis2Placement2D =ifc_file.createIfcAxis2Placement2D(
                        ifc_file.createIfcCartesianPoint( (0.,0.) ) )

    B1_AreaProfile = ifc_file.createIfcRectangleProfileDef('AREA')
    B1_AreaProfile.Position = B1_Axis2Placement2D
    B1_AreaProfile.XDim = b
    B1_AreaProfile.YDim = h
    return B1_AreaProfile