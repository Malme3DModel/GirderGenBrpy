import ifcopenshell
import uuid

class IfcManager():
    def __init__(self):
        self.ifcFile = ifcopenshell.open("./data/sample.ifc")
        self.owner_history = self.ifcFile.createIfcOwnerHistory() 
        self.context = self.ifcFile.by_type("IfcGeometricRepresentationContext")[0]


    def create_guid(self):
      return ifcopenshell.guid.compress(uuid.uuid1().hex)

    def I_Section(self, W , D , tw , tf, r):
        B1_Axis2Placement2D = self.ifcFile.createIfcAxis2Placement2D( 
                              self.ifcFile.createIfcCartesianPoint( (0.,0.) ) )
        
        B1_AreaProfile = self.ifcFile.createIfcIShapeProfileDef('AREA')
        B1_AreaProfile.Position = B1_Axis2Placement2D 
        B1_AreaProfile.OverallWidth = W
        B1_AreaProfile.OverallDepth = D
        B1_AreaProfile.WebThickness = tw
        B1_AreaProfile.FlangeThickness = tf
        B1_AreaProfile.FilletRadius = r
        return B1_AreaProfile


    def Rect_Section(self, b, h):
      B1_Axis2Placement2D =self.ifcFile.createIfcAxis2Placement2D( 
                            self.ifcFile.createIfcCartesianPoint( (0.,0.) ) )
      
      B1_AreaProfile = self.ifcFile.createIfcRectangleProfileDef('AREA')
      B1_AreaProfile.Position = B1_Axis2Placement2D 
      B1_AreaProfile.XDim = b
      B1_AreaProfile.YDim = h
      return B1_AreaProfile

    def CreateBeam(self ,Container, Name , section , L , position , direction):
      Z = 0.,0.,1.
      B1 = self.ifcFile.createIfcBeam(self.create_guid(), self.owner_history , Name)
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
      
      Flr1_Container = self.ifcFile.createIfcRelContainedInSpatialStructure(self.create_guid(),self.owner_history)
      Flr1_Container.RelatedElements=[B1]
      Flr1_Container.RelatingStructure= Container


    def add_Beam(self, W ,D ,tw ,tf, r,
                    L ,position, direction):
      section1 = self.I_Section(W, D, tw, tf, r)
      Floor1 = self.ifcFile.by_type("IfcBuildingStorey")[0]

      self.CreateBeam(Floor1, Name='Beam-Floor1-B1' ,section= section1 ,
                      L=L ,position=position, direction=direction)

      # 別ファイルとして書き出す
      self.ifcFile.write("./data/sample_new.ifc")

        