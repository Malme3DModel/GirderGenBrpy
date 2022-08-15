import ifcopenshell

from src.comon.comon import *
from src.comon.ifcProject import ifcProject

class ifcRebar():

    def __init__(self, ifcProject: ifcProject):
        self.ifc = ifcProject


    def CreateRebar(self, Container, Name, position, direction):

        B1_Point = self.ifc.file.createIfcCartesianPoint(position)
        B1_Axis2Placement = self.ifc.file.createIfcAxis2Placement3D(B1_Point)
        B1_Axis2Placement.Axis = self.ifc.file.createIfcDirection(direction)
        B1_Axis2Placement.RefDirection = self.ifc.file.createIfcDirection(
            direction)

        B1_Placement = self.ifc.file.createIfcLocalPlacement(
            Container.ObjectPlacement, B1_Axis2Placement)

        # 鉄筋 start
        dia = 16
        pnt1 = self.ifc.file.createIfcCartesianPoint( (0.0,0.0,1000.0) )
        pnt2 = self.ifc.file.createIfcCartesianPoint( (0.0,0.0,0.0) )
        pnt3 = self.ifc.file.createIfcCartesianPoint( (0.0,200.0,0.0) )

        line1 = self.ifc.file.createIfcPolyline()
        line1.Points = [pnt1,pnt2]

        line2 = self.ifc.file.createIfcPolyline()
        line2.Points = [pnt2,pnt3]

        line_segment1 = self.ifc.file.createIfcCompositeCurveSegment()
        line_segment1.Transition = 'CONTINUOUS'
        line_segment1.SameSense = True
        line_segment1.ParentCurve = line1

        line_segment2 = self.ifc.file.createIfcCompositeCurveSegment()
        line_segment2.Transition = 'CONTINUOUS'
        line_segment2.SameSense = True
        line_segment2.ParentCurve = line2

        Curve = self.ifc.file.createIfcCompositeCurve()
        Curve.SelfIntersect=False
        Curve.Segments = [line_segment1 , line_segment2]

        B1_Extruded = self.ifc.file.createIfcSweptDiskSolid()
        B1_Extruded.Directrix = Curve
        B1_Extruded.Radius = dia/2	# : 	IfcPositiveLengthMeasure;
        B1_Extruded.InnerRadius=None
        B1_Extruded.StartParam = 0.0	# : 	IfcParameterValue;
        B1_Extruded.EndParam = 1.0	 #: 	IfcParameterValue;
        # end

        B1_Repr = self.ifc.file.createIfcShapeRepresentation()
        B1_Repr.ContextOfItems = self.ifc.context
        B1_Repr.RepresentationIdentifier = 'Body'
        B1_Repr.RepresentationType = 'SweptSolid'
        B1_Repr.Items = [B1_Extruded]

        B1_DefShape = self.ifc.file.createIfcProductDefinitionShape()
        B1_DefShape.Representations = [B1_Repr]

        # 鉄筋情報 start
        B1 = self.ifc.file.createIfcReinforcingBar(
            create_guid() , self.ifc.owner_hist)
        B1.ObjectType = 'rebar'
        B1.Name='D{}'.format(dia)
        B1.Description ="bar no.3"
        B1.ObjectType = None
        B1.SteelGrade = 'SD345'
        B1.NominalDiameter = dia
        B1.CrossSectionArea = 198.6
        B1.BarLength = 1000.0
        B1.BarSurface = 'PLAIN'  #  'TEXTURED'
        B1.ObjectPlacement = B1_Placement
        B1.Representation = B1_DefShape
        # end

        Flr1_Container = self.ifc.file.createIfcRelContainedInSpatialStructure(
            create_guid(), self.ifc.owner_hist)
        Flr1_Container.RelatedElements = [B1]
        Flr1_Container.RelatingStructure = Container


    def add_Rebar(self, position, direction, Floor):

        self.CreateRebar(Floor, Name='bar-B1',
            position=position, direction=direction)


