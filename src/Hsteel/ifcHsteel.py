import ifcopenshell

from src.comon.comon import *
from src.comon.ifcProject import ifcProject

class ifcHsteel():

    def __init__(self, ifcProject: ifcProject):
        self.ifc = ifcProject


    def CreateBeam(self, Container, Name, point_list_extrusion_area, position, direction, length):



        B1_Point = self.ifc.file.createIfcCartesianPoint(position)
        B1_Axis2Placement = self.ifc.file.createIfcAxis2Placement3D(B1_Point)
        B1_Axis2Placement.Axis = self.ifc.file.createIfcDirection(direction)
        B1_Axis2Placement.RefDirection = self.ifc.file.createIfcDirection(
            direction)

        B1_Placement = self.ifc.file.createIfcLocalPlacement(
            Container.ObjectPlacement, B1_Axis2Placement)

        B1_ExtrudePlacement = self.ifc.file.createIfcAxis2Placement3D(
            self.ifc.file.createIfcCartesianPoint(Z))

        # H鋼 start
        B1_Extruded = create_ifcextrudedareasolid(self.ifc.file,
                point_list_extrusion_area,
                B1_ExtrudePlacement, (0.0, 0.0, 1.0), extrusion = length)
        # end

        B1_Repr = self.ifc.file.createIfcShapeRepresentation()
        B1_Repr.ContextOfItems = self.ifc.context
        B1_Repr.RepresentationIdentifier = 'Body'
        B1_Repr.RepresentationType = 'SweptSolid'
        B1_Repr.Items = [B1_Extruded]

        B1_DefShape = self.ifc.file.createIfcProductDefinitionShape()
        B1_DefShape.Representations = [B1_Repr]

        # H鋼 start
        B1 = self.ifc.file.createIfcSlab(
            create_guid(), self.ifc.owner_hist, Name)
        B1.ObjectType = 'Hsteel'
        B1.ObjectPlacement = B1_Placement
        B1.Representation = B1_DefShape
        # end

        Flr1_Container = self.ifc.file.createIfcRelContainedInSpatialStructure(
            create_guid(), self.ifc.owner_hist)
        Flr1_Container.RelatedElements = [B1]
        Flr1_Container.RelatingStructure = Container


    def add_Beam(self, L, D, W, tf, tw, amount, interval, T, Floor):
        x1 = (tw / 2.0)
        x2 = (D / 2.0)
        dx = ((float(amount)-1.0) * interval / 2.0)
        dy = tf + T + (W / 2.0)
        y1 = W / 2.0
        y2 = y1 + tf / 2.0
        for i in range(int(amount)):
            point_list_extrusion_area=[
                (-x1-dx, -y1-dy, 0.0),
                (-x2-dx, -y1-dy, 0.0),
                (-x2-dx, -y2-dy, 0.0),
                ( x2-dx, -y2-dy, 0.0),
                ( x2-dx, -y1-dy, 0.0),
                ( x1-dx, -y1-dy, 0.0),
                ( x1-dx,  y1-dy, 0.0),
                ( x2-dx,  y1-dy, 0.0),
                ( x2-dx,  y2-dy, 0.0),
                (-x2-dx,  y2-dy, 0.0),
                (-x2-dx,  y1-dy, 0.0),
                (-x1-dx,  y1-dy, 0.0),
                (-x1-dx, -y1-dy, 0.0)
                ]
            self.CreateBeam(Floor, Name='Beam-B1',
                point_list_extrusion_area=point_list_extrusion_area,
                position=(0.0,0.0,0.0), direction=(1.0,0.0,0.0), length=L)
            dx -= interval




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