import ifcopenshell
import ifcopenshell.template
from src.comon.comon import *
from src.comon.object import *

class H_IfcManager():

    def __init__(self):

        self.ifcFile = ifcopenshell.template.create(schema_identifier='IFC4')
        #self.ifcFile = ifcopenshell.file(schema='IFC4')
        #履歴
        self.owner_history = self.ifcFile.createIfcOwnerHistory() 
        # 環境
        self.context = self.ifcFile.by_type("IfcGeometricRepresentationContext")[0]


    def CreateBeam(self ,Container, Name , section , L , position , direction):
      Z = 0.,0.,1.
      B1 = self.ifcFile.createIfcBeam(create_guid(), self.owner_history , Name)
      B1.ObjectType ='beam'
      
      B1_Point =self.ifcFile.createIfcCartesianPoint ( position ) 
      B1_Axis2Placement = self.ifcFile.createIfcAxis2Placement3D(B1_Point)
      B1_Axis2Placement.Axis = self.ifcFile.createIfcDirection(direction)
      B1_Axis2Placement.RefDirection = self.ifcFile.createIfcDirection(direction) 

      B1_Placement = self.ifcFile.createIfcLocalPlacement(Container.ObjectPlacement,B1_Axis2Placement)
      B1.ObjectPlacement=B1_Placement

      B1_ExtrudePlacement = self.ifcFile.createIfcAxis2Placement3D(self.ifcFile.createIfcCartesianPoint(Z))
    
      B1_Extruded=self.ifcFile.createIfcExtrudedAreaSolid()
      B1_Extruded.SweptArea=section
      B1_Extruded.Position=B1_ExtrudePlacement
      B1_Extruded.ExtrudedDirection = self.ifcFile.createIfcDirection(Z)
      B1_Extruded.Depth = L
      
      B1_Repr=self.ifcFile.createIfcShapeRepresentation()
      B1_Repr.ContextOfItems = self.context
      B1_Repr.RepresentationIdentifier = 'Body'
      B1_Repr.RepresentationType = 'SweptSolid'
      B1_Repr.Items = [B1_Extruded]
      
      B1_DefShape=self.ifcFile.createIfcProductDefinitionShape()
      B1_DefShape.Representations=[B1_Repr]
      B1.Representation=B1_DefShape
      
      Flr1_Container = self.ifcFile.createIfcRelContainedInSpatialStructure(create_guid(),self.owner_history)
      Flr1_Container.RelatedElements=[B1]
      Flr1_Container.RelatingStructure= Container


    def add_Beam(self, W ,D ,tw ,tf, r,
                    L ,position, direction):

      self.ifcFile.write("./data/sample_new.ifc")
      return

      section1 = I_Section(self.ifcFile, W, D, tw, tf, r)

      # 階を生成
      storey_placement = create_ifclocalplacement(self.ifcFile)
      Floor1 = self.ifcFile.createIfcBuildingStorey(create_guid(), self.owner_history, 'Floor1', None, None, storey_placement, None, None, "ELEMENT", 0.0)

      self.CreateBeam(Floor1, Name='Beam-Floor1-B1' ,section= section1 ,
                      L=L ,position=position, direction=direction)

      # 別ファイルとして書き出す
      self.ifcFile.write("./data/sample_new.ifc")

        