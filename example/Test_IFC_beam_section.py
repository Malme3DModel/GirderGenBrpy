"""
   TestIFC_beam_section.py
"""
import sys , os
import uuid
import tempfile
import ifcopenshell
import time
import math

O = 0., 0., 0.
X = 1., 0., 0.
Y = 0., 1., 0.
Z = 0., 0., 1.
create_guid = lambda: ifcopenshell.guid.compress(uuid.uuid1().hex)

def CreateBeam(ifc_file ,Container, Name , section , L , position , direction):
    Z = 0.,0.,1.
    B1 = ifc_file.createIfcBeam(create_guid(),owner_hist , Name)
    B1.ObjectType ='beam'
    
    B1_Point =ifc_file.createIfcCartesianPoint ( position ) 
    B1_Axis2Placement = ifc_file.createIfcAxis2Placement3D(B1_Point)
    B1_Axis2Placement.Axis = ifc_file.createIfcDirection(direction)
    B1_Axis2Placement.RefDirection =ifc_file.createIfcDirection(Z)

    B1_Placement = ifc_file.createIfcLocalPlacement(Container.ObjectPlacement,B1_Axis2Placement)
    B1.ObjectPlacement=B1_Placement

    B1_ExtrudePlacement = ifc_file.createIfcAxis2Placement3D(ifc_file.createIfcCartesianPoint ( (0.,0.,0.) )   )
   
    B1_Extruded=ifc_file.createIfcExtrudedAreaSolid()
    B1_Extruded.SweptArea=section
    B1_Extruded.Position=B1_ExtrudePlacement
    B1_Extruded.ExtrudedDirection = ifc_file.createIfcDirection(Z)
    B1_Extruded.Depth = L
    
    B1_Repr=ifc_file.createIfcShapeRepresentation()
    B1_Repr.ContextOfItems=context
    B1_Repr.RepresentationIdentifier = 'Body'
    B1_Repr.RepresentationType = 'SweptSolid'
    B1_Repr.Items = [B1_Extruded]
    
    B1_DefShape=ifc_file.createIfcProductDefinitionShape()
    B1_DefShape.Representations=[B1_Repr]
    B1.Representation=B1_DefShape
    
    Flr1_Container = ifc_file.createIfcRelContainedInSpatialStructure(create_guid(),owner_hist)
    Flr1_Container.RelatedElements=[B1]
    Flr1_Container.RelatingStructure= Container

def I_Section(W ,D , tw , tf  , r):
    B1_Axis2Placement2D =ifc_file.createIfcAxis2Placement2D( 
                          ifc_file.createIfcCartesianPoint( (0.,0.) ) )
    
    B1_AreaProfile = ifc_file.createIfcIShapeProfileDef('AREA')
    B1_AreaProfile.Position = B1_Axis2Placement2D 
    B1_AreaProfile.OverallWidth = W
    B1_AreaProfile.OverallDepth = D
    B1_AreaProfile.WebThickness = tw
    B1_AreaProfile.FlangeThickness = tf
    B1_AreaProfile.FilletRadius=r
    return B1_AreaProfile

def L_Section(W ,D , t   , r):
    B1_Axis2Placement2D =ifc_file.createIfcAxis2Placement2D( 
                          ifc_file.createIfcCartesianPoint( (0.,0.) ) )
    
    B1_AreaProfile = ifc_file.createIfcLShapeProfileDef('AREA')
    B1_AreaProfile.Position = B1_Axis2Placement2D 
    B1_AreaProfile.Width = W
    B1_AreaProfile.Depth = D
    B1_AreaProfile.Thickness = t

    B1_AreaProfile.FilletRadius=r
    return B1_AreaProfile

def U_Section(W ,D , tw  , tf  , r):
    B1_Axis2Placement2D =ifc_file.createIfcAxis2Placement2D( 
                          ifc_file.createIfcCartesianPoint( (0.,0.) ) )
    
    B1_AreaProfile = ifc_file.createIfcUShapeProfileDef('AREA')
    B1_AreaProfile.Position = B1_Axis2Placement2D 
    B1_AreaProfile.FlangeWidth = W
    B1_AreaProfile.Depth = D
    B1_AreaProfile.WebThickness = tw
    B1_AreaProfile.FlangeThickness = tf
    B1_AreaProfile.FilletRadius=r
    B1_AreaProfile.EdgeRadius=r*0.5
    return B1_AreaProfile

def Rect_Section(b, h):
    B1_Axis2Placement2D =ifc_file.createIfcAxis2Placement2D( 
                          ifc_file.createIfcCartesianPoint( (0.,0.) ) )
    
    B1_AreaProfile = ifc_file.createIfcRectangleProfileDef('AREA')
    B1_AreaProfile.Position = B1_Axis2Placement2D 
    B1_AreaProfile.XDim = b
    B1_AreaProfile.YDim = h
    return B1_AreaProfile


######################################



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

section1 = I_Section(W=0.2 ,D=0.3 , tw=0.012 , tf=0.012  , r = 2*0.012)
section2 = Rect_Section(b= 0.2, h=0.4)
section3 = L_Section(W = 0.1 , D = 0.1 ,t = 0.012   , r=2*0.012)
section4 = U_Section(W=0.15 ,D=0.3 , tw=0.012 , tf=0.012  , r = 2*0.012)

CreateBeam(ifc_file ,floor1, Name='Beam-floor1-B1' ,section= section1 ,
             L=4.00 ,position=(0.0,0.0,0.0) , direction=(1.0,0.0,0.0))

CreateBeam(ifc_file ,floor1, Name='Beam-floor1-B1' ,section= section2 ,
             L=4.00 ,position=(0.0,0.5,0.0) , direction=(1.0,0.0,0.0))

CreateBeam(ifc_file ,floor1, Name='Beam-floor1-B1' ,section= section3 ,
             L=4.00 ,position=(0.0,1.0,0.0) , direction=(1.0,0.0,0.0))

CreateBeam(ifc_file ,floor1, Name='Beam-floor1-B1' ,section= section4 ,
             L=4.00 ,position=(0.0,1.5,0.0) , direction=(1.0,0.0,0.0))

ifc_file.write("./data/sample_new2.ifc")

# myPath = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'OutPut'
# ifc_file.write(myPath + os.sep+'Test04.ifc')
