import time
import math
import ifcopenshell

from src.comon.comon import *

class ifcProject:

    def __init__(self):

        filename = 'output_rebar3.ifc'
        timestamp = time.time()
        timestring = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(timestamp))
        creator = "hirano"
        organization = "malme"
        application, application_version = "IfcOpenShell", "0.5"
        project_globalid, project_name = create_guid(), "TestGrid"


        # open for Blank
        self.file = ifcopenshell.file(schema="IFC2X3")

        #=============================================

        org = self.file.createIfcOrganization( )
        org.Name = organization

        app = self.file.createIfcApplication( )
        app.ApplicationDeveloper = org
        app.Version = "0.16.6700"
        app.ApplicationFullName = "FreeCAD"

        person = self.file.createIfcPerson()
        person.FamilyName="Hirano"


        person_org= self.file.createIfcPersonAndOrganization()
        person_org.ThePerson=person
        person_org.TheOrganization=org

        self.owner_hist= self.file.createIfcOwnerHistory()
        self.owner_hist.OwningUser = person_org
        self.owner_hist.OwningApplication = app
        self.owner_hist.ChangeAction= "ADDED"
        self.owner_hist.CreationDate= int(time.time())

        LengthUnit = self.file.createIfcSIUnit()
        LengthUnit.UnitType = "LENGTHUNIT"
        LengthUnit.Prefix = "MILLI"
        LengthUnit.Name="METRE"

        AreaUnit = self.file.createIfcSIUnit()
        AreaUnit.UnitType = "AREAUNIT"
        AreaUnit.Prefix = "MILLI"
        AreaUnit.Name="SQUARE_METRE"

        VolumeUnit = self.file.createIfcSIUnit()
        VolumeUnit.UnitType = "VOLUMEUNIT"
        VolumeUnit.Prefix = "MILLI"
        VolumeUnit.Name="CUBIC_METRE"

        SolidAngleUnit = self.file.createIfcSIUnit()
        SolidAngleUnit.UnitType = "SOLIDANGLEUNIT"
        SolidAngleUnit.Name="STERADIAN"

        MassUnit = self.file.createIfcSIUnit()
        MassUnit.UnitType = "MASSUNIT"
        MassUnit.Name="GRAM"

        TimeUnit = self.file.createIfcSIUnit()
        TimeUnit.UnitType = "TIMEUNIT"
        TimeUnit.Name="SECOND"

        ThermodynamicTemperatureUnit = self.file.createIfcSIUnit()
        ThermodynamicTemperatureUnit.UnitType = "THERMODYNAMICTEMPERATUREUNIT"
        ThermodynamicTemperatureUnit.Name="DEGREE_CELSIUS"

        LuminousIntensityUnit = self.file.createIfcSIUnit()
        LuminousIntensityUnit.UnitType = "LUMINOUSINTENSITYUNIT"
        LuminousIntensityUnit.Name="LUMEN"

        PlaneAngleUnit = self.file.createIfcSIUnit()
        PlaneAngleUnit.UnitType = "PLANEANGLEUNIT"
        PlaneAngleUnit.Name  ="RADIAN"

        AngleUnit = self.file.createIfcMeasureWithUnit()
        AngleUnit.UnitComponent =PlaneAngleUnit
        AngleUnit.ValueComponent = self.file.createIfcPlaneAngleMeasure(math.pi/180)


        DimExp = self.file.createIfcDimensionalExponents(0,0,0,0,0,0,0)


        ConvertBaseUnit = self.file.createIfcConversionBasedUnit()
        ConvertBaseUnit.Dimensions = DimExp
        ConvertBaseUnit.UnitType="PLANEANGLEUNIT"
        ConvertBaseUnit.Name="DEGREE"
        ConvertBaseUnit.ConversionFactor = AngleUnit


        UnitAssignment=self.file.createIfcUnitAssignment([LengthUnit , AreaUnit , VolumeUnit ,ConvertBaseUnit, SolidAngleUnit, MassUnit, 
                                                          TimeUnit, ThermodynamicTemperatureUnit, LuminousIntensityUnit, PlaneAngleUnit])

        # Defining project and representation contexts
        WorldCoordinateSystem = create_ifcaxis2placement_world(self.file)

        self.context = self.file.createIfcGeometricRepresentationContext()
        self.context.ContextType = "Model"
        self.context.CoordinateSpaceDimension = 3
        self.context.Precision = 1.e-08
        self.context.WorldCoordinateSystem = WorldCoordinateSystem

        myProject = self.file.createIfcProject(create_guid())
        myProject.OwnerHistory = self.owner_hist
        myProject.Name = "Test Girder"
        myProject.RepresentationContexts = [self.context]
        myProject.UnitsInContext = UnitAssignment

        # Defining site, building and first story ------------
        site_placement = self.file.createIfcLocalPlacement()
        site_placement.RelativePlacement = create_ifcaxis2placement(self.file)
        mySite = self.file.createIfcSite( create_guid() )
        mySite.OwnerHistory = self.owner_hist
        mySite.Name = "My Site"
        mySite.ObjectPlacement = site_placement
        mySite.CompositionType="ELEMENT"

        container_project = self.file.createIfcRelAggregates(create_guid() , self.owner_hist)
        container_project.Name="Project Container"
        container_project.RelatingObject = myProject
        container_project.RelatedObjects = [mySite]

        building_placement = self.file.createIfcLocalPlacement()
        building_placement.PlacementRelTo = site_placement
        building_placement.RelativePlacement = create_ifcaxis2placement(self.file)

        self.myBuilding = self.file.createIfcBuilding( create_guid(), self.owner_hist )
        self.myBuilding.Name = "Test Building"
        self.myBuilding.ObjectPlacement = building_placement
        self.myBuilding.CompositionType="ELEMENT"

        container_site = self.file.createIfcRelAggregates(create_guid() , self.owner_hist)
        container_site.Name = "Site Container"
        container_site.RelatingObject = mySite
        container_site.RelatedObjects = [self.myBuilding]

        self.container_storey = self.file.createIfcRelAggregates(create_guid() , self.owner_hist)
        self.container_storey.Name = "Building Container"
        self.container_storey.RelatingObject = self.myBuilding
        self.container_storey.RelatedObjects = []

        self.floor1_placement = self.file.createIfcLocalPlacement()
        self.floor1_placement.PlacementRelTo = building_placement
        self.floor1_placement.RelativePlacement = create_ifcaxis2placement(self.file)


    def create_place(self, Name):

        floor1 = self.file.createIfcBuildingStorey( create_guid(), self.owner_hist, Name, None, None, self.myBuilding, None, None, "ELEMENT", 0.0)
        floor1.ObjectPlacement = self.floor1_placement
        self.container_storey.RelatedObjects = [floor1]

        return floor1
