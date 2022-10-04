import ifcopenshell

from src.comon.comon import *
from src.comon.ifcProject import ifcProject

class ifcObj():

    def __init__(self, ifcProject: ifcProject):
        self.ifc = ifcProject

    def CreateObj(self, Container, Name3, vertices, faces, position, direction, ID, Class, Info, Type):

        B1 = self.ifc.file.create_entity(
            "IfcBuildingElementProxy",
            GlobalId = ifcopenshell.guid.new(),
            Name = Name3
        )

        ifc_faces = []
        for face in faces:
            # 座標点の配列を作成
            point_list = []
            for index in face:
                v = vertices[index]
                try:
                    v = v.tolist()
                except:
                    pass
                p = self.ifc.file.createIfcCartesianPoint(v)
                point_list.append(p)
            # 面を作成
            ifc_faces.append(
                self.ifc.file.createIfcFace(
                    [
                        self.ifc.file.createIfcFaceOuterBound(
                            self.ifc.file.createIfcPolyLoop(point_list),
                            True,
                        )
                    ]
                )
            )

        B1_Point =self.ifc.file.createIfcCartesianPoint ( position )
        B1_Axis2Placement = self.ifc.file.createIfcAxis2Placement3D(B1_Point)
        B1_Axis2Placement.Axis = self.ifc.file.createIfcDirection(direction)
        B1_Axis2Placement.RefDirection =self.ifc.file.createIfcDirection(X)

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

        # プロパティ付けてみた
        ## https://community.osarch.org/discussion/711/ifcopenshell-how-to-add-a-new-property-and-value-to-an-object
        property_values = [
            self.ifc.file.createIfcPropertySingleValue("ID", None, self.ifc.file.create_entity("IfcText", ID), None),
            self.ifc.file.createIfcPropertySingleValue("オブジェクト分類名", None, self.ifc.file.create_entity("IfcText", Class), None),
            self.ifc.file.createIfcPropertySingleValue("判別情報", None, self.ifc.file.create_entity("IfcText", Info), None),
            self.ifc.file.createIfcPropertySingleValue("種類・形式", None, self.ifc.file.create_entity("IfcText", Type), None),
        ]
        property_set = self.ifc.file.createIfcPropertySet(B1.GlobalId, self.ifc.owner_hist, "基本情報", None, property_values)
        self.ifc.file.createIfcRelDefinesByProperties(B1.GlobalId, self.ifc.owner_hist, None, None, [B1], property_set)


    def add_Obj(self, vertices, faces, Container, Name3, ID, Class, Info, Type):

        self.CreateObj(Container=Container, Name3=Name3,
                        vertices=vertices, faces=faces,
                        position=(0.0,0.0,0.0), direction=(0.0,0.0,1.0), ID=ID, Class=Class, Info=Info, Type=Type)