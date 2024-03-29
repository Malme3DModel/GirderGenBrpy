import time
import math
import ifcopenshell

from src.comon.comon import *

class ifcProject:

    def __init__(self, ProjectName, Name1, Name_R, Class_R, Milepost_B, Milepost_E, BP, EP):

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
        app.ApplicationFullName = "Brpy"

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
        LengthUnit.Name="METRE"

        AreaUnit = self.file.createIfcSIUnit()
        AreaUnit.UnitType = "AREAUNIT"
        AreaUnit.Name="SQUARE_METRE"

        VolumeUnit = self.file.createIfcSIUnit()
        VolumeUnit.UnitType = "VOLUMEUNIT"
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
        myProject.Name = ProjectName
        myProject.ObjectType = ProjectName
        myProject.RepresentationContexts = [self.context]
        myProject.UnitsInContext = UnitAssignment

        # Defining site, building and first story ------------
        site_placement = self.file.createIfcLocalPlacement()
        site_placement.RelativePlacement = create_ifcaxis2placement(self.file)
        mySite = self.file.createIfcSite( create_guid() )
        mySite.OwnerHistory = self.owner_hist
        mySite.ObjectType = "地理情報"
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
        self.myBuilding.Name = Name1
        self.myBuilding.ObjectPlacement = building_placement
        self.myBuilding.CompositionType="ELEMENT"
        
        # 階層１の属性情報を付与
        ## https://community.osarch.org/discussion/711/ifcopenshell-how-to-add-a-new-property-and-value-to-an-object
        property_values = [
            self.file.createIfcPropertySingleValue("ID", None, self.file.create_entity("IfcText", "1"), None),
            self.file.createIfcPropertySingleValue("オブジェクト分類名", None, self.file.create_entity("IfcText", "橋梁"), None),
            self.file.createIfcPropertySingleValue("判別情報1（路線名）", None, self.file.create_entity("IfcText", Name_R), None),
            self.file.createIfcPropertySingleValue("判別情報2（道路種別）", None, self.file.create_entity("IfcText", Class_R), None),
            self.file.createIfcPropertySingleValue("判別情報3-1（開始距離標）", None, self.file.create_entity("IfcText", Milepost_B), None),
            self.file.createIfcPropertySingleValue("判別情報3-2（終了距離標）", None, self.file.create_entity("IfcText", Milepost_E), None),
            self.file.createIfcPropertySingleValue("判別情報3-3（開始測点番号）", None, self.file.create_entity("IfcText", BP), None),
            self.file.createIfcPropertySingleValue("判別情報3-4（終了測点番号）", None, self.file.create_entity("IfcText", EP), None),
        ]
        property_set = self.file.createIfcPropertySet(self.myBuilding.GlobalId, self.owner_hist, "基本情報", None, property_values)
        self.file.createIfcRelDefinesByProperties(self.myBuilding.GlobalId, self.owner_hist, None, None, [self.myBuilding], property_set)
        
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


    def create_place(self, Name, ID, Class, Info, Type):

        floor1 = self.file.createIfcBuildingStorey( create_guid(), self.owner_hist, Name, None, None, self.myBuilding, None, None, "ELEMENT", 0.0)
        floor1.ObjectPlacement = self.floor1_placement
        
        # プロパティ付けてみた
        ## https://community.osarch.org/discussion/711/ifcopenshell-how-to-add-a-new-property-and-value-to-an-object
        property_values = [
            self.file.createIfcPropertySingleValue("ID", None, self.file.create_entity("IfcText", ID), None),
            self.file.createIfcPropertySingleValue("オブジェクト分類名", None, self.file.create_entity("IfcText", Class), None),
            self.file.createIfcPropertySingleValue("判別情報", None, self.file.create_entity("IfcText", Info), None),
            self.file.createIfcPropertySingleValue("種類・形式", None, self.file.create_entity("IfcText", Type), None),
        ]
        property_set = self.file.createIfcPropertySet(floor1.GlobalId, self.owner_hist, "基本情報", None, property_values)
        self.file.createIfcRelDefinesByProperties(floor1.GlobalId, self.owner_hist, None, None, [floor1], property_set)
        ##

        self.container_storey.RelatedObjects = [floor1]

        return floor1
