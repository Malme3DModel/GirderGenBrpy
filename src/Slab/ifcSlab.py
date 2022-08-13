import ifcopenshell

from src.comon.comon import *
from src.comon.ifcProject import ifcProject

class ifcSlab():

    def __init__(self, ifcProject: ifcProject):
        self.ifc = ifcProject


    def CreateSlab(self, Container, Name, point_list_extrusion_area, position, direction):

        B1 = self.ifc.file.createIfcSlab(
            create_guid(), self.ifc.owner_hist, Name)
        B1.ObjectType = 'slab'

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

        # スラブ
        B1_Extruded = create_ifcextrudedareasolid(self.ifc.file,
                point_list_extrusion_area,
                B1_ExtrudePlacement, (0.0, 0.0, 1.0), 3.0)
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


    def add_Slab(self, point_list_extrusion_area, position, direction, Floor):

        self.CreateSlab(Floor, Name='Slab-B1',
            point_list_extrusion_area=point_list_extrusion_area,
            position=position, direction=direction)




# Creates an IfcPolyLine from a list of points, specified as Python tuples
def create_ifcpolyline(ifcfile, point_list):
    ifcpts = []
    for point in point_list:
        point = ifcfile.createIfcCartesianPoint(point)
        ifcpts.append(point)
    polyline = ifcfile.createIfcPolyLine(ifcpts)
    return polyline


# Creates an IfcExtrudedAreaSolid from a list of points, specified as Python tuples
def create_ifcextrudedareasolid(ifcfile, point_list, ifcaxis2placement, extrude_dir, extrusion):
    polyline = create_ifcpolyline(ifcfile, point_list)
    ifcclosedprofile = ifcfile.createIfcArbitraryClosedProfileDef("AREA", None, polyline)
    ifcdir = ifcfile.createIfcDirection(extrude_dir)
    ifcextrudedareasolid = ifcfile.createIfcExtrudedAreaSolid(ifcclosedprofile, ifcaxis2placement, ifcdir, extrusion)
    return ifcextrudedareasolid