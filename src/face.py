import ifcopenshell
import uuid
import time
import tempfile
import ifcopenshell
import pdb


O = 0., 0., 0.
X = 1., 0., 0.
Y = 0., 1., 0.
Z = 0., 0., 1.

# Helper function definitions

# Creates an IfcAxis2Placement3D from Location, Axis and RefDirection specified as Python tuples
def create_ifcaxis2placement(ifcfile, point=O, dir1=Z, dir2=X):
    point = ifcfile.createIfcCartesianPoint(point)
    dir1 = ifcfile.createIfcDirection(dir1)
    dir2 = ifcfile.createIfcDirection(dir2)
    axis2placement = ifcfile.createIfcAxis2Placement3D(point, dir1, dir2)
    #pdb.set_trace()
    print("fn calling")
    print("point %s" % point)
    print("dir1 %s" % dir1)
    print("dir2 %s" % dir2)
    print("axis2placement %s" % axis2placement)
    return axis2placement

def create_ifclocalplacement(ifcfile, point=O, dir1=Z, dir2=X, relative_to=None):
    axis2placement = create_ifcaxis2placement(ifcfile,point,dir1,dir2)
    ifclocalplacement2 = ifcfile.createIfcLocalPlacement(relative_to,axis2placement)
    #pdb.set_trace()
    return ifclocalplacement2

IFC_model = ifcopenshell.open("./data/sample.ifc")

IFC_vertices = [
            IFC_model.createIfcCartesianPoint( (0.0, 0.0, 0.0) ),
            IFC_model.createIfcCartesianPoint( (0.0, 1.0, 0.0) ),
            IFC_model.createIfcCartesianPoint( (1.0, 1.0, 0.0) ),
            IFC_model.createIfcCartesianPoint( (1.0, 0.0, 0.0) )
        ]

face = [[0,1,2,3],[4,5,6,7],[8,9,10,11]]
cartesian_points = []
for vertex in face[0]:
    cartesian_points.append(IFC_vertices[vertex])
polyloop = IFC_model.create_entity("IfcPolyLoop", Polygon=cartesian_points)
outerbound = IFC_model.create_entity("IfcFaceOuterBound", Bound=polyloop, Orientation=True)  # orientation of vertices is CCW

faceModel = IFC_model.create_entity("IfcFace", Bounds=[outerbound])


faceModel.ObjectPlacement = create_ifclocalplacement(ifcfile=IFC_model, point=O, dir1=Z, dir2=X, relative_to=None)

IFC_model.write("./data/sample_face.ifc")