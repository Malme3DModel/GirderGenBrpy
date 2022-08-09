import ifcopenshell
import uuid

class IfcManager():
    def __init__(self):
        self.ifcFile = ifcopenshell.open("./data/sample.ifc")
        self.owner_history = self.ifcFile.createIfcOwnerHistory() 
        self.context = self.ifcFile.by_type("IfcGeometricRepresentationContext")[0]


    def create_guid(self):
        return ifcopenshell.guid.compress(uuid.uuid1().hex)

    # # Creates an IfcAxis2Placement3D from Location, Axis and RefDirection specified as Python tuples
    def create_ifcaxis2placement(self, point, dir1, dir2):
        point = self.ifcFile.createIfcCartesianPoint(point)
        dir1 = self.ifcFile.createIfcDirection(dir1)
        dir2 = self.ifcFile.createIfcDirection(dir2)
        axis2placement = self.ifcFile.createIfcAxis2Placement3D(point, dir1, dir2)
        return axis2placement

    # Creates an IfcLocalPlacement from Location, Axis and RefDirection, specified as Python tuples, and relative placement
    def create_ifclocalplacement(self, point, dir1, dir2, relative_to=None):
        axis2placement = self.create_ifcaxis2placement(point,dir1,dir2)
        ifclocalplacement2 = self.ifcFile.createIfcLocalPlacement(relative_to,axis2placement)
        return ifclocalplacement2

    # Creates an IfcExtrudedAreaSolid from a list of points, specified as Python tuples
    def create_ifcextrudedareasolid(self, point_list, ifcaxis2placement, extrude_dir, extrusion):
        polyline = self.create_ifcpolyline(point_list)
        ifcclosedprofile = self.ifcFile.createIfcArbitraryClosedProfileDef("AREA", None, polyline)
        ifcdir = self.ifcFile.createIfcDirection(extrude_dir)
        ifcextrudedareasolid = self.ifcFile.createIfcExtrudedAreaSolid(ifcclosedprofile, ifcaxis2placement, ifcdir, extrusion)
        return ifcextrudedareasolid


    def create_ifcpolyline(self, point_list):
        ifcpts = []
        for point in point_list:
            point = self.ifcFile.createIfcCartesianPoint(point)
            ifcpts.append(point)
        polyline = self.ifcFile.createIfcPolyLine(ifcpts)
        return polyline


    def add_Slab(self, b, h, L, position, direction):
        
        wall_placement = self.create_ifclocalplacement((0., 0., 0.), (0., 0., 1.), (1., 0., 0.))

        polyline = self.create_ifcpolyline( [(0.0, 0.0, 0.0), (5.0, 0.0, 0.0)])
        axis_representation = self.ifcFile.createIfcShapeRepresentation(self.context, "Axis", "Curve2D", [polyline])

        extrusion_placement = self.create_ifcaxis2placement( (0.0, 0.0, 0.0),
                (0.0, 0.0, 1.0), (1.0, 0.0, 0.0))
        point_list_extrusion_area = [(0.0, -.2, 0.0), (5.0, -.2, 0.0), (5.0,
            .2, 0.0), (0.0, .2, 0.0), (0.0, -.2, 0.0)]
        solid = self.create_ifcextrudedareasolid(point_list_extrusion_area,
                extrusion_placement, (0.0, 0.0, 1.0), 3.0)

        body_representation = self.ifcFile.createIfcShapeRepresentation(
                                self.context, "Body", "SweptSolid", [solid])

        product_shape = self.ifcFile.createIfcProductDefinitionShape(None, None, [axis_representation, body_representation])

        slab = self.ifcFile.createIfcSlab(self.create_guid(), self.owner_history, "Slab", "An awesome slab", None, wall_placement, product_shape, None)

        # 別ファイルとして書き出す
        self.ifcFile.write("./data/sample_new.ifc")

        