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


filename = 'output_grid1.ifc'
timestamp = time.time()
timestring = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(timestamp))
creator = "Chakkree Tiyawongsuwan"
organization = "Southeast Asia University"
application, application_version = "IfcOpenShell", "0.5"
project_globalid, project_name = create_guid(), "TestGrid"


# open for Blank
# ifc_file = ifcopenshell.open('Dummy.ifc') # chest!! ifc_file have only ifc header
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

#  Global unit definitions
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


footprint_context = ifc_file.createIfcGeometricRepresentationSubContext()
footprint_context.ContextIdentifier = 'FootPrint'
footprint_context.ContextType = "Model"
footprint_context.ParentContext = context
footprint_context.TargetView = 'MODEL_VIEW'

myProject = ifc_file.createIfcProject(create_guid())
myProject.OwnerHistory = owner_hist
myProject.Name = "Test Grid"
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
floor1.Elevation = 1000


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

# --- Defining the grid axes geometry  -----

GridXList = [   {'id':'1' , 'distance':0.0 } ,
                {'id':'2' , 'distance':4000.0}  ]

GridYList = [   {'id':'A' , 'distance':0.0 } ,
                {'id':'B' , 'distance':4000.0}  ]

xMin = GridXList[0]['distance']-2000.0 ; xMax =  GridXList[-1]['distance']+2000.0 
yMin =  GridYList[0]['distance']-2000.0 ; yMax =  GridYList[-1]['distance']+2000.0 


polylineSet = []
gridX = []
for iGrid in GridXList:
    pnt1 = ifc_file.createIfcCartesianPoint( (iGrid['distance'],yMin) )
    pnt2 = ifc_file.createIfcCartesianPoint( (iGrid['distance'],yMax) )
    Line = ifc_file.createIfcPolyline( [pnt1 , pnt2] )
    polylineSet.append(Line)
    grid = ifc_file.createIfcGridAxis()
    grid.AxisTag = iGrid['id']
    grid.AxisCurve = Line
    grid.SameSense = True
    gridX.append(grid)

gridY = []
for iGrid in GridYList:
    pnt1 = ifc_file.createIfcCartesianPoint( (xMin ,iGrid['distance']) )
    pnt2 = ifc_file.createIfcCartesianPoint( (xMax,iGrid['distance']) )
    Line = ifc_file.createIfcPolyline( [pnt1 , pnt2] )
    polylineSet.append(Line)
    grid = ifc_file.createIfcGridAxis()
    grid.AxisTag = iGrid['id']
    grid.AxisCurve = Line
    grid.SameSense = True
    gridY.append(grid)

# Defining the grid 
PntGrid = ifc_file.createIfcCartesianPoint( O )

myGridCoordinateSystem = ifc_file.createIfcAxis2Placement3D()
myGridCoordinateSystem.Location= PntGrid
myGridCoordinateSystem.Axis = axis_Z
myGridCoordinateSystem.RefDirection = axis_X

grid_placement = ifc_file.createIfcLocalPlacement()
grid_placement.PlacementRelTo = floor1_placement
grid_placement.RelativePlacement = myGridCoordinateSystem

grid_curvedSet =  ifc_file.createIfcGeometricCurveSet(polylineSet)

gridShape_Reppresentation = ifc_file.createIfcShapeRepresentation()
gridShape_Reppresentation.ContextOfItems = footprint_context
gridShape_Reppresentation.RepresentationIdentifier = 'FootPrint'
gridShape_Reppresentation.RepresentationType = 'GeometricCurveSet'
gridShape_Reppresentation.Items = [grid_curvedSet]

grid_Reppresentation = ifc_file.createIfcProductDefinitionShape()
grid_Reppresentation.Representations  = [gridShape_Reppresentation]

myGrid = ifc_file.createIfcGrid(create_guid() , owner_hist)
myGrid.ObjectPlacement = grid_placement
myGrid.Representation = grid_Reppresentation
myGrid.UAxes=gridX
myGrid.VAxes=gridY

# assignment to spatial structure ------------------------------------------ 
container_SpatialStructure= ifc_file.createIfcRelContainedInSpatialStructure(create_guid() , owner_hist)
container_SpatialStructure.Name='BuildingStoreyContainer'
container_SpatialStructure.Description = 'BuildingStoreyContainer for Elements'
container_SpatialStructure.RelatingStructure = floor1
container_SpatialStructure.RelatedElements = [myGrid]

#=============================================
ifc_file.write("./data/sample_new.ifc")

# filePath = os.path.dirname(os.path.abspath(__file__))
# ifc_file.write(filePath+ os.sep+filename)
