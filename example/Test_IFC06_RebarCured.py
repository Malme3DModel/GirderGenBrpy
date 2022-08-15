import sys , os
import time
import uuid
import math

import ifcopenshell

O = 0., 0., 0.
X = 1., 0., 0.
Y = 0., 1., 0.
Z = 0., 0., 1.
create_guid = lambda: ifcopenshell.guid.compress(uuid.uuid1().hex)


filename = 'output_rebar3.ifc'
timestamp = time.time()
timestring = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(timestamp))
creator = "Chakkree Tiyawongsuwan"
organization = "Southeast Asia University"
application, application_version = "IfcOpenShell", "0.5"
project_globalid, project_name = create_guid(), "TestGrid"



# open for Blank
ifc_file = ifcopenshell.file()

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
# bar1.BarRole = 'MAIN'
bar1.BarSurface = 'PLAIN'  #  'TEXTURED'


#----------------------------------

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
# bar2.BarRole = 'MAIN'
bar2.BarSurface = 'PLAIN'  #  'TEXTURED'

#----------------------------------

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


bar_placement = ifc_file.createIfcLocalPlacement()
bar_placement.RelativePlacement = ifc_file.createIfcAxis2Placement3D(
       ifc_file.createIfcCartesianPoint( (150.0 , 150.0,0.0) ) ,axis_Z ,  axis_X)

bar3 = ifc_file.createIfcReinforcingBar(create_guid() , owner_hist)
bar3.Name='RB12'
bar3.Description ="bar no.3"
bar3.ObjectType = None
bar3.ObjectPlacement = bar_placement
bar3.Representation = bar_DefShape
bar3.SteelGrade = 'SR24'
bar3.NominalDiameter = 12.0
bar3.CrossSectionArea = math.pi*(12.0/2)**2
bar3.BarLength = 1000.0
# bar3.BarRole = 'MAIN'
bar3.BarSurface = 'PLAIN'  #  'TEXTURED'

#----------------------------------

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


bar_placement = ifc_file.createIfcLocalPlacement()
bar_placement.RelativePlacement = ifc_file.createIfcAxis2Placement3D(
       ifc_file.createIfcCartesianPoint( (00.0 , 150.0,0.0) ) ,axis_Z ,  axis_X)

bar4 = ifc_file.createIfcReinforcingBar(create_guid() , owner_hist)
bar4.Name='RB12'
bar4.Description ="bar no.4"
bar4.ObjectType = None
bar4.ObjectPlacement = bar_placement
bar4.Representation = bar_DefShape
bar4.SteelGrade = 'SR24'
bar4.NominalDiameter = 12.0
bar4.CrossSectionArea = math.pi*(12.0/2)**2
bar4.BarLength = 1000.0
# bar4.BarRole = 'MAIN'
bar4.BarSurface = 'PLAIN'  #  'TEXTURED'


Rel = ifc_file.createIfcRelContainedInSpatialStructure(create_guid() , owner_hist)
Rel.RelatedElements = [bar1 , bar2 , bar3, bar4]
Rel.RelatingStructure = floor1

#=============================================
ifc_file.write("./data/sample_new.ifc")
