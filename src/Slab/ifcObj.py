import ifcopenshell

from src.comon.comon import *
from src.comon.ifcProject import ifcProject

class ifcObj():

    def __init__(self, ifcProject: ifcProject):
        self.ifc = ifcProject

    def CreateObj(self, Container, Name, vertices, faces, position, direction):

        B1 = self.ifc.file.create_entity(
            "IfcBuildingElementProxy",
            GlobalId = ifcopenshell.guid.new(),
            Name = Name
        )

        ifc_faces = []
        for face in faces:
            ifc_faces.append(
                self.ifc.file.createIfcFace(
                    [
                        self.ifc.file.createIfcFaceOuterBound(
                            self.ifc.file.createIfcPolyLoop(
                                [self.ifc.file.createIfcCartesianPoint(vertices[index-1]) for index in face]
                            ),
                            True,
                        )
                    ]
                )
            )


        B1_Point =self.ifc.file.createIfcCartesianPoint ( position )
        B1_Axis2Placement = self.ifc.file.createIfcAxis2Placement3D(B1_Point)
        B1_Axis2Placement.Axis = self.ifc.file.createIfcDirection(direction)
        B1_Axis2Placement.RefDirection =self.ifc.file.createIfcDirection(Z)

        B1_Placement = self.ifc.file.createIfcLocalPlacement(Container.ObjectPlacement,B1_Axis2Placement)
        B1.ObjectPlacement=B1_Placement

        B1_Extruded = self.ifc.file.createIfcFacetedBrep(self.ifc.file.createIfcClosedShell(ifc_faces))

        B1_Repr=self.ifc.file.createIfcShapeRepresentation()
        B1_Repr.ContextOfItems=self.ifc.context
        B1_Repr.RepresentationIdentifier = 'Body'
        B1_Repr.RepresentationType = 'Brep'
        B1_Repr.Items = [B1_Extruded]

        B1_DefShape=self.ifc.file.createIfcProductDefinitionShape()
        B1_DefShape.Representations=[B1_Repr]
        B1.Representation=B1_DefShape

        Flr1_Container = self.ifc.file.createIfcRelContainedInSpatialStructure(create_guid(), self.ifc.owner_hist)
        Flr1_Container.RelatedElements=[B1]
        Flr1_Container.RelatingStructure= Container



    def add_Slab(self, vertices, faces, Floor):

        self.CreateObj(Floor, Name='Slab-B1',
                        vertices=vertices, faces=faces,
                        position=(0.0,3.0,0.0), direction=(1.0,0.0,0.0))

