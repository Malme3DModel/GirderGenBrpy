import ifcopenshell

from src.comon.comon import *
from src.comon.ifcProject import ifcProject


class ifcHsteel():

    def __init__(self, ifcProject: ifcProject):
        self.ifc = ifcProject

    def CreateBeam(self, Container, Name, section, L, position, direction):
        B1 = self.ifc.file.createIfcBeam(
            create_guid(), self.ifc.owner_hist, Name)
        B1.ObjectType = 'beam'

        B1_Point = self.ifc.file.createIfcCartesianPoint(position)
        B1_Axis2Placement = self.ifc.file.createIfcAxis2Placement3D(B1_Point)
        B1_Axis2Placement.Axis = self.ifc.file.createIfcDirection(direction)
        B1_Axis2Placement.RefDirection = self.ifc.file.createIfcDirection(
            direction)

        B1_Placement = self.ifc.file.createIfcLocalPlacement(
            Container.ObjectPlacement, B1_Axis2Placement)
        B1.ObjectPlacement = B1_Placement

        B1_ExtrudePlacement = self.ifc.file.createIfcAxis2Placement3D(
            self.ifc.file.createIfcCartesianPoint(Z))

        # H鋼
        B1_Extruded = self.ifc.file.createIfcExtrudedAreaSolid()
        B1_Extruded.SweptArea = section
        B1_Extruded.Position = B1_ExtrudePlacement
        B1_Extruded.ExtrudedDirection = self.ifc.file.createIfcDirection(Z)
        B1_Extruded.Depth = L
        #

        B1_Repr = self.ifc.file.createIfcShapeRepresentation()
        B1_Repr.ContextOfItems = self.ifc.context
        B1_Repr.RepresentationIdentifier = 'Body'
        B1_Repr.RepresentationType = 'SweptSolid'
        B1_Repr.Items = [B1_Extruded]

        B1_DefShape = self.ifc.file.createIfcProductDefinitionShape()
        B1_DefShape.Representations = [B1_Repr]
        B1.Representation = B1_DefShape

        Flr1_Container = self.ifc.file.createIfcRelContainedInSpatialStructure(
            create_guid(), self.ifc.owner_hist)
        Flr1_Container.RelatedElements = [B1]
        Flr1_Container.RelatingStructure = Container


    def add_Beam(self, W, D, tw, tf, r,
                    L, position, direction, Floor):

        section1 = I_Section(self.ifc.file, W, D, tw, tf, r)

        self.CreateBeam(Floor, Name='Beam-B1', section=section1,
                        L=L, position=position, direction=direction)


def I_Section(ifcFile, W , D , tw , tf, r):
    B1_Axis2Placement2D = ifcFile.createIfcAxis2Placement2D(
                            ifcFile.createIfcCartesianPoint( (0.,0.) ) )

    B1_AreaProfile = ifcFile.createIfcIShapeProfileDef('AREA')
    B1_AreaProfile.Position = B1_Axis2Placement2D
    B1_AreaProfile.OverallWidth = W
    B1_AreaProfile.OverallDepth = D
    B1_AreaProfile.WebThickness = tw
    B1_AreaProfile.FlangeThickness = tf
    B1_AreaProfile.FilletRadius = r

    return B1_AreaProfile