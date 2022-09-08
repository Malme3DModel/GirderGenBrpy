import ifcopenshell
import uuid

O = 0., 0., 0.
X = 1., 0., 0.
Y = 0., 1., 0.
Z = 0., 0., 1.

def create_guid():
    return ifcopenshell.guid.compress(uuid.uuid1().hex)


# Creates an IfcAxis2Placement3D from Location, Axis and RefDirection specified as Python tuples
def create_ifcaxis2placement(ifcfile, point=O, dir1=Z, dir2=X):
    point = ifcfile.createIfcCartesianPoint(point)
    dir1 = ifcfile.createIfcDirection(dir1)
    dir2 = ifcfile.createIfcDirection(dir2)
    axis2placement = ifcfile.createIfcAxis2Placement3D(point, dir1, dir2)
    return axis2placement

def create_ifcaxis2placement_world(ifcfile, point=O):
    point = ifcfile.createIfcCartesianPoint(point)
    axis2placement = ifcfile.createIfcAxis2Placement3D(point)
    return axis2placement




