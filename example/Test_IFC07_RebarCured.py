"""
 Test_IFC07_RebarCured.py
"""

import sys , os
import time
import uuid
import math

import ifcopenshell

O = (0., 0., 0.)
X = 1., 0., 0.
Y = 0., 1., 0.
Z = 0., 0., 1.

def create_ifcaxis2placement(ifcfile, point=O, dir1=Z, dir2=X):
    point = ifcfile.createIfcCartesianPoint(point)
    dir1 = ifcfile.createIfcDirection(dir1)
    dir2 = ifcfile.createIfcDirection(dir2)
    axis2placement = ifcfile.createIfcAxis2Placement3D(point, dir1, dir2)
    return axis2placement



create_guid = lambda: ifcopenshell.guid.compress(uuid.uuid1().hex)


filename = 'output_rebar07_RebarCurved.ifc'
timestamp = time.time()
timestring = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(timestamp))
creator = "Chakkree Tiyawongsuwan"
organization = "Southeast Asia University"
application, application_version = "IfcOpenShell", "0.5"
project_globalid, project_name = create_guid(), "TestRebar"



# open for Blank
ifc_file = ifcopenshell.file(schema='IFC4')

#=============================================

org = ifc_file.createIfcOrganization( )
org.Name = organization

app = ifc_file.createIfcApplication( )
app.ApplicationDeveloper = org
app.Version = "0.16.6700"
app.ApplicationFullName = "FreeCAD"

person = ifc_file.createIfcPerson()
person.FamilyName="Chakkree Tiyawongsuwan"


person_org= ifc_file.createIfcPersonAndOrganization()
person_org.ThePerson=person
person_org.TheOrganization=org

owner_hist= ifc_file.createIfcOwnerHistory()
owner_hist.OwningUser = person_org
owner_hist.OwningApplication = app
owner_hist.ChangeAction= "NOCHANGE"
owner_hist.CreationDate= int(time.time())

LengthUnit = ifc_file.createIfcSIUnit()
LengthUnit.UnitType = "LENGTHUNIT"
LengthUnit.Prefix = "MILLI"
LengthUnit.Name="METRE"

#AreaUnit = ifc_file.createIfcSIUnit("AREAUNIT" , None, "SQUARE_METRE")
AreaUnit = ifc_file.createIfcSIUnit()
AreaUnit.UnitType = "AREAUNIT"
AreaUnit.Name="SQUARE_METRE"


VolumeUnit = ifc_file.createIfcSIUnit()
VolumeUnit.UnitType = "VOLUMEUNIT"
VolumeUnit.Name="CUBIC_METRE"


PlaneAngleUnit = ifc_file.createIfcSIUnit()
PlaneAngleUnit.UnitType = "PLANEANGLEUNIT"
PlaneAngleUnit.Name  ="RADIAN"

AngleUnit = ifc_file.createIfcMeasureWithUnit()
AngleUnit.UnitComponent =PlaneAngleUnit 
AngleUnit.ValueComponent = ifc_file.createIfcPlaneAngleMeasure(math.pi/180)


DimExp = ifc_file.createIfcDimensionalExponents(0,0,0,0,0,0,0)


ConvertBaseUnit = ifc_file.createIfcConversionBasedUnit()
ConvertBaseUnit.Dimensions = DimExp
ConvertBaseUnit.UnitType="PLANEANGLEUNIT"
ConvertBaseUnit.Name="DEGREE"
ConvertBaseUnit.ConversionFactor = AngleUnit


UnitAssignment=ifc_file.createIfcUnitAssignment([LengthUnit , AreaUnit , VolumeUnit ,ConvertBaseUnit])

axis_X = ifc_file.createIfcDirection( X )
axis_Y = ifc_file.createIfcDirection( Y )
axis_Z = ifc_file.createIfcDirection( Z )
Pnt_O = ifc_file.createIfcCartesianPoint( O )


# Defining project and representation contexts 
WorldCoordinateSystem = ifc_file.createIfcAxis2Placement3D()
WorldCoordinateSystem.Location=Pnt_O
WorldCoordinateSystem.Axis = axis_Z
WorldCoordinateSystem.RefDirection = axis_X

context = ifc_file.createIfcGeometricRepresentationContext()
context.ContextType = "Model"
context.CoordinateSpaceDimension = 3
context.Precision = 1.e-05
context.WorldCoordinateSystem = WorldCoordinateSystem

myProject = ifc_file.createIfcProject(create_guid())
myProject.OwnerHistory = owner_hist
myProject.Name = "Test Rebar"
myProject.RepresentationContexts = [context]
myProject.UnitsInContext = UnitAssignment


# Defining site, building and first story ------------
site_placement = ifc_file.createIfcLocalPlacement()
site_placement.RelativePlacement=WorldCoordinateSystem
mySite = ifc_file.createIfcSite( create_guid() )
mySite.OwnerHistory = owner_hist
mySite.Name = "My Site"
mySite.ObjectPlacement = site_placement
mySite.CompositionType="ELEMENT"

building_placement = ifc_file.createIfcLocalPlacement()
building_placement.PlacementRelTo = site_placement
building_placement.RelativePlacement = WorldCoordinateSystem

myBuilding = ifc_file.createIfcBuilding( create_guid(), owner_hist )
myBuilding.Name = "Test Building"
myBuilding.ObjectPlacement = building_placement
myBuilding.CompositionType="ELEMENT"

floor1_placement = ifc_file.createIfcLocalPlacement()
floor1_placement.PlacementRelTo = building_placement
floor1_placement.RelativePlacement = WorldCoordinateSystem

floor1 = ifc_file.createIfcBuildingStorey( create_guid(), owner_hist )
floor1.Name = "Floor 1"
floor1.ObjectPlacement = floor1_placement
floor1.CompositionType="ELEMENT"



container_project = ifc_file.createIfcRelAggregates(create_guid() , owner_hist)
container_project.Name="Project Container"
container_project.RelatingObject = myProject 
container_project.RelatedObjects = [mySite]

container_site = ifc_file.createIfcRelAggregates(create_guid() , owner_hist)
container_site.Name = "Site Container"
container_site.RelatingObject = mySite
container_site.RelatedObjects = [myBuilding] 

container_storey = ifc_file.createIfcRelAggregates(create_guid() , owner_hist)
container_storey.Name = "Building Container"
container_storey.RelatingObject = myBuilding
container_storey.RelatedObjects = [floor1] 

# End Basic IFC
#===========================================

pnt1 = ifc_file.createIfcCartesianPoint( (0.0,0.0,0.0) )
pnt2 = ifc_file.createIfcCartesianPoint( (0.0,0.0,1000.0) )

bar_line = ifc_file.createIfcPolyline()
bar_line.Points = [pnt1,pnt2]

bar_solid = ifc_file.createIfcSweptDiskSolid()
bar_solid.Directrix = bar_line	 #: 	IfcCurve;
bar_solid.Radius = 6.0	# : 	IfcPositiveLengthMeasure;
bar_solid.InnerRadius=None
bar_solid.StartParam = 0.0	# : 	IfcParameterValue;
bar_solid.EndParam = 1.0	 #: 	IfcParameterValue;


bar_ShapeRepr = ifc_file.createIfcShapeRepresentation()
bar_ShapeRepr.ContextOfItems = context
bar_ShapeRepr.RepresentationIdentifier = 'Body'
bar_ShapeRepr.RepresentationType = 'AdvancedSweptSolid'
bar_ShapeRepr.Items = [bar_solid]

bar_DefShape = ifc_file.createIfcProductDefinitionShape()
bar_DefShape.Representations = [bar_ShapeRepr]  # 

bar1 = ifc_file.createIfcReinforcingBar(create_guid() , owner_hist)
bar1.Name='RB12'
bar1.Description ="bar no.1"
bar1.ObjectType = None
bar1.ObjectPlacement = floor1_placement
bar1.Representation = bar_DefShape
bar1.SteelGrade = 'SR24'
bar1.NominalDiameter = 12.0
bar1.CrossSectionArea = math.pi*(12.0/2)**2
bar1.BarLength = 1000.0
#bar1.BarRole = 'MAIN'
bar1.BarSurface = 'PLAIN'  #  'TEXTURED'


# Bar No.2
#----------------------------------
pnt1 = ifc_file.createIfcCartesianPoint( (0.0,0.0,1000.0) )
pnt2 = ifc_file.createIfcCartesianPoint( (0.0,0.0,0.0) )

pnt3 = ifc_file.createIfcCartesianPoint( (0.0,0.0,-1000.0) )


line1 = ifc_file.createIfcPolyline()
line1.Points = [pnt1,pnt2]

line2 = ifc_file.createIfcPolyline()
line2.Points = [pnt2,pnt3]

line3 = ifc_file.createIfcPolyline()
line3.Points = [pnt1,pnt2,pnt3]



segment = ifc_file.createIfcCompositeCurveSegment()
segment.Transition = 'CONTSAMEGRADIENT'
segment.SameSense = False
#segment.ParentCurve = Curve


line_segment1 = ifc_file.createIfcCompositeCurveSegment()
line_segment1.Transition = 'CONTINUOUS'
line_segment1.SameSense = True
line_segment1.ParentCurve = line1

line_segment2 = ifc_file.createIfcCompositeCurveSegment()
line_segment2.Transition = 'CONTINUOUS'
line_segment2.SameSense = True
line_segment2.ParentCurve = line2

#arc_segment2


Curve = ifc_file.createIfcCompositeCurve()
Curve.SelfIntersect=False
#Curve.Segments = [line1 , line2]
Curve.Segments = [line_segment1 , line_segment2]



bar_solid = ifc_file.createIfcSweptDiskSolid()
#bar_solid.Directrix = line3	 #: 	IfcCurve;  # OK
bar_solid.Directrix = Curve
bar_solid.Radius = 6.0	# : 	IfcPositiveLengthMeasure;
bar_solid.InnerRadius=None
bar_solid.StartParam = 0.0	# : 	IfcParameterValue;
bar_solid.EndParam = 1.0	 #: 	IfcParameterValue;


bar_ShapeRepr = ifc_file.createIfcShapeRepresentation()
bar_ShapeRepr.ContextOfItems = context
bar_ShapeRepr.RepresentationIdentifier = 'Body'
bar_ShapeRepr.RepresentationType = 'AdvancedSweptSolid'
bar_ShapeRepr.Items = [bar_solid]

bar_DefShape = ifc_file.createIfcProductDefinitionShape()
bar_DefShape.Representations = [bar_ShapeRepr]  # 


bar_placement = ifc_file.createIfcLocalPlacement()
bar_placement.RelativePlacement = ifc_file.createIfcAxis2Placement3D(
       ifc_file.createIfcCartesianPoint( (150.0 , 0.0,0.0) ) ,axis_Z ,  axis_X)

bar2 = ifc_file.createIfcReinforcingBar(create_guid() , owner_hist)
bar2.Name='RB12'
bar2.Description ="bar no.2"
bar2.ObjectType = None
bar2.ObjectPlacement = bar_placement
bar2.Representation = bar_DefShape
bar2.SteelGrade = 'SR24'
bar2.NominalDiameter = 12.0
bar2.CrossSectionArea = math.pi*(12.0/2)**2
bar2.BarLength = 1000.0
#bar2.BarRole = 'MAIN'
bar2.BarSurface = 'PLAIN'  #  'TEXTURED'



# bar No. 3
#----------------------------------
dia = 12
pnt1 = ifc_file.createIfcCartesianPoint( (0.0,0.0,1000.0) )
pnt2 = ifc_file.createIfcCartesianPoint( (0.0,0.0,0.0) )

pnt3 = ifc_file.createIfcCartesianPoint( (0.0,200.0,0.0) )


line1 = ifc_file.createIfcPolyline()
line1.Points = [pnt1,pnt2]

line2 = ifc_file.createIfcPolyline()
line2.Points = [pnt2,pnt3]


line_segment1 = ifc_file.createIfcCompositeCurveSegment()
line_segment1.Transition = 'CONTINUOUS'
line_segment1.SameSense = True
line_segment1.ParentCurve = line1

line_segment2 = ifc_file.createIfcCompositeCurveSegment()
line_segment2.Transition = 'CONTINUOUS'
line_segment2.SameSense = True
line_segment2.ParentCurve = line2

#arc_segment2


Curve = ifc_file.createIfcCompositeCurve()
Curve.SelfIntersect=False
#Curve.Segments = [line1 , line2]
Curve.Segments = [line_segment1 , line_segment2]



bar_solid = ifc_file.createIfcSweptDiskSolid()
#bar_solid.Directrix = line3	 #: 	IfcCurve;  # OK
bar_solid.Directrix = Curve
bar_solid.Radius = dia/2	# : 	IfcPositiveLengthMeasure;
bar_solid.InnerRadius=None
bar_solid.StartParam = 0.0	# : 	IfcParameterValue;
bar_solid.EndParam = 1.0	 #: 	IfcParameterValue;


bar_ShapeRepr = ifc_file.createIfcShapeRepresentation()
bar_ShapeRepr.ContextOfItems = context
bar_ShapeRepr.RepresentationIdentifier = 'Body'
bar_ShapeRepr.RepresentationType = 'AdvancedSweptSolid'
bar_ShapeRepr.Items = [bar_solid]

bar_DefShape = ifc_file.createIfcProductDefinitionShape()
bar_DefShape.Representations = [bar_ShapeRepr]  # 


bar_placement = ifc_file.createIfcLocalPlacement()
bar_placement.RelativePlacement = ifc_file.createIfcAxis2Placement3D(
       ifc_file.createIfcCartesianPoint( (300.0 , 0.0,0.0) ) ,axis_Z ,  axis_X)

bar3 = ifc_file.createIfcReinforcingBar(create_guid() , owner_hist)
bar3.Name='RB{}'.format( dia )
bar3.Description ="bar no.3"
bar3.ObjectType = None
bar3.ObjectPlacement = bar_placement
bar3.Representation = bar_DefShape
bar3.SteelGrade = 'SR24'
bar3.NominalDiameter = 12.0
bar3.CrossSectionArea = math.pi*(12.0/2)**2
bar3.BarLength = 1000.0
#bar3.BarRole = 'MAIN'
bar3.BarSurface = 'PLAIN'  #  'TEXTURED'


# bar No. 4
#----------------------------------
dia = 12.
R = 3*dia
Ext = 12*dia

pnt1 = ifc_file.createIfcCartesianPoint( (0.0,0.0,1000.0) )
pnt2 = ifc_file.createIfcCartesianPoint( (0.0,0.0,0.0) )

pnt3 = ifc_file.createIfcCartesianPoint( (0.0,R,0.0) )
pnt4 = ifc_file.createIfcCartesianPoint( (0.0,R,-R) )
pnt5 = ifc_file.createIfcCartesianPoint( (0.0,R+Ext,-R) )

line1 = ifc_file.createIfcPolyline()
line1.Points = [pnt1,pnt2]

line2 = ifc_file.createIfcPolyline()
line2.Points = [pnt4,pnt5]


line_segment1 = ifc_file.createIfcCompositeCurveSegment()
line_segment1.Transition = 'CONTINUOUS'
line_segment1.SameSense = True
line_segment1.ParentCurve = line1



#pl = create_ifcaxis2placement(ifc_file, point=(600.0,R,0.0), dir1=X, dir2=Z)
pl = ifc_file.createIfcAxis2Placement3D()
pl.Location = pnt3
pl.Axis = axis_X
pl.RefDirection = axis_Y


circle1 = ifc_file.createIfcCircle()
circle1.Position = pl
circle1.Radius = R

arc1 = ifc_file.createIfcTrimmedCurve()
arc1.BasisCurve = circle1
arc1.SenseAgreement = True
"""
arc1.MasterRepresentation='PARAMETER'
arc1.Trim1=[ifc_file.createIfcParameterValue(180.)]
arc1.Trim2=[ifc_file.createIfcParameterValue(270.)]
"""
#arc1.MasterRepresentation='CARTESIAN'
arc1.MasterRepresentation='PARAMETER'
arc1.Trim1=[pnt2,ifc_file.createIfcParameterValue(180.)]
arc1.Trim2=[pnt4,ifc_file.createIfcParameterValue(270.)]

line_segment2 = ifc_file.createIfcCompositeCurveSegment()
line_segment2.Transition = 'CONTSAMEGRADIENT'
line_segment2.SameSense = True
line_segment2.ParentCurve = arc1



line_segment3= ifc_file.createIfcCompositeCurveSegment()
line_segment3.Transition = 'CONTSAMEGRADIENT'
line_segment3.SameSense = True
line_segment3.ParentCurve = line2


#arc_segment2
Curve = ifc_file.createIfcCompositeCurve()
Curve.SelfIntersect=False
#Curve.Segments = [line1 , line2]
Curve.Segments = [line_segment1 , line_segment2 ,line_segment3]



bar_solid = ifc_file.createIfcSweptDiskSolid()
#bar_solid.Directrix = line3	 #: 	IfcCurve;  # OK
bar_solid.Directrix = Curve
bar_solid.Radius = dia/2	# : 	IfcPositiveLengthMeasure;
bar_solid.InnerRadius=None
bar_solid.StartParam = 0.0	# : 	IfcParameterValue;
bar_solid.EndParam = 1.0	 #: 	IfcParameterValue;


bar_ShapeRepr = ifc_file.createIfcShapeRepresentation()
bar_ShapeRepr.ContextOfItems = context
bar_ShapeRepr.RepresentationIdentifier = 'Body'
bar_ShapeRepr.RepresentationType = 'AdvancedSweptSolid'
bar_ShapeRepr.Items = [bar_solid]

bar_DefShape = ifc_file.createIfcProductDefinitionShape()
bar_DefShape.Representations = [bar_ShapeRepr]  #


bar_placement = ifc_file.createIfcLocalPlacement()
bar_placement.RelativePlacement = ifc_file.createIfcAxis2Placement3D(
       ifc_file.createIfcCartesianPoint( (450.0 , 0.0,0.0) ) ,axis_Z ,  axis_X)

bar4 = ifc_file.createIfcReinforcingBar(create_guid() , owner_hist)
bar4.Name='RB{:0d}'.format( int(dia) )
bar4.Description ="bar no.4"
bar4.ObjectType = None
bar4.ObjectPlacement = bar_placement
bar4.Representation = bar_DefShape
bar4.SteelGrade = 'SR24'
bar4.NominalDiameter = 12.0
bar4.CrossSectionArea = math.pi*(12.0/2)**2
bar4.BarLength = 1000.0
#bar4.BarRole = 'MAIN'
bar4.BarSurface = 'PLAIN'  #  'TEXTURED'



Rel = ifc_file.createIfcRelContainedInSpatialStructure(create_guid() , owner_hist)
Rel.RelatedElements = [bar1 , bar2 , bar3 , bar4]
Rel.RelatingStructure = floor1

#=============================================
ifc_file.write("./data/sample_new.ifc")


