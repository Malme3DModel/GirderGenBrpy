"""
   TestIFC_beam_section.py
"""
import sys , os
import uuid
import tempfile
import ifcopenshell

create_guid = lambda: ifcopenshell.guid.compress(uuid.uuid1().hex)

def CreateBeam(ifcFile ,Container, Name , section , L , position , direction):
    Z = 0.,0.,1.
    B1 = ifcFile.createIfcBeam(create_guid(),owner_history , Name)
    B1.ObjectType ='beam'
    
    B1_Point =ifcFile.createIfcCartesianPoint ( position ) 
    B1_Axis2Placement = ifcFile.createIfcAxis2Placement3D(B1_Point)
    B1_Axis2Placement.Axis = ifcFile.createIfcDirection(direction)
    B1_Axis2Placement.RefDirection =ifcFile.createIfcDirection(Z)

    B1_Placement = ifcFile.createIfcLocalPlacement(Container.ObjectPlacement,B1_Axis2Placement)
    B1.ObjectPlacement=B1_Placement

    B1_ExtrudePlacement = ifcFile.createIfcAxis2Placement3D(ifcFile.createIfcCartesianPoint ( (0.,0.,0.) )   )
   
    B1_Extruded=ifcFile.createIfcExtrudedAreaSolid()
    B1_Extruded.SweptArea=section
    B1_Extruded.Position=B1_ExtrudePlacement
    B1_Extruded.ExtrudedDirection = ifcFile.createIfcDirection(Z)
    B1_Extruded.Depth = L
    
    B1_Repr=ifcFile.createIfcShapeRepresentation()
    B1_Repr.ContextOfItems=context
    B1_Repr.RepresentationIdentifier = 'Body'
    B1_Repr.RepresentationType = 'SweptSolid'
    B1_Repr.Items = [B1_Extruded]
    
    B1_DefShape=ifcFile.createIfcProductDefinitionShape()
    B1_DefShape.Representations=[B1_Repr]
    B1.Representation=B1_DefShape
    
    Flr1_Container = ifcFile.createIfcRelContainedInSpatialStructure(create_guid(),owner_history)
    Flr1_Container.RelatedElements=[B1]
    Flr1_Container.RelatingStructure= Container

def I_Section(W ,D , tw , tf  , r):
    B1_Axis2Placement2D =ifcfile.createIfcAxis2Placement2D( 
                          ifcfile.createIfcCartesianPoint( (0.,0.) ) )
    
    B1_AreaProfile = ifcfile.createIfcIShapeProfileDef('AREA')
    B1_AreaProfile.Position = B1_Axis2Placement2D 
    B1_AreaProfile.OverallWidth = W
    B1_AreaProfile.OverallDepth = D
    B1_AreaProfile.WebThickness = tw
    B1_AreaProfile.FlangeThickness = tf
    B1_AreaProfile.FilletRadius=r
    return B1_AreaProfile

def L_Section(W ,D , t   , r):
    B1_Axis2Placement2D =ifcfile.createIfcAxis2Placement2D( 
                          ifcfile.createIfcCartesianPoint( (0.,0.) ) )
    
    B1_AreaProfile = ifcfile.createIfcLShapeProfileDef('AREA')
    B1_AreaProfile.Position = B1_Axis2Placement2D 
    B1_AreaProfile.Width = W
    B1_AreaProfile.Depth = D
    B1_AreaProfile.Thickness = t

    B1_AreaProfile.FilletRadius=r
    return B1_AreaProfile

def U_Section(W ,D , tw  , tf  , r):
    B1_Axis2Placement2D =ifcfile.createIfcAxis2Placement2D( 
                          ifcfile.createIfcCartesianPoint( (0.,0.) ) )
    
    B1_AreaProfile = ifcfile.createIfcUShapeProfileDef('AREA')
    B1_AreaProfile.Position = B1_Axis2Placement2D 
    B1_AreaProfile.FlangeWidth = W
    B1_AreaProfile.Depth = D
    B1_AreaProfile.WebThickness = tw
    B1_AreaProfile.FlangeThickness = tf
    B1_AreaProfile.FilletRadius=r
    B1_AreaProfile.EdgeRadius=r*0.5
    return B1_AreaProfile

def Rect_Section(b, h):
    B1_Axis2Placement2D =ifcfile.createIfcAxis2Placement2D( 
                          ifcfile.createIfcCartesianPoint( (0.,0.) ) )
    
    B1_AreaProfile = ifcfile.createIfcRectangleProfileDef('AREA')
    B1_AreaProfile.Position = B1_Axis2Placement2D 
    B1_AreaProfile.XDim = b
    B1_AreaProfile.YDim = h
    return B1_AreaProfile

template = """ISO-10303-21;
HEADER;
FILE_DESCRIPTION(('ViewDefinition [CoordinationView]'),'2;1');
FILE_NAME('','2016-06-19T20:11:24',(),(),'IfcOpenShell 0.5.0-dev','IfcOpenShell 0.5.0-dev','');
FILE_SCHEMA(('IFC2X3'));
ENDSEC;
DATA;
#1=IFCPROJECT('1JDO00DXyHvhYmD1VhSTH7',#4,'Test Project','Test Create IFC by ifcOpenShell',$,$,'Design',(#16,#15),#7);
#2=IFCPERSON($,'Tiyawongsuwan','Chakkree',$,$,$,$,$);
#3=IFCORGANIZATION($,'Southeast Asia University',$,$,$);
#4=IFCPERSONANDORGANIZATION(#2,#3,$);
#5=IFCAPPLICATION(#3,'0.0.0.1','macro ifcOpenShell run on FreeCAD','SAU_IFC');
#6=IFCOWNERHISTORY(#4,#5,$,.ADDED.,1466341884,$,$,1466341884);
#7=IFCUNITASSIGNMENT((#8,#9,#10));
#8=IFCSIUNIT(*,.LENGTHUNIT.,$,.METRE.);
#9=IFCSIUNIT(*,.AREAUNIT.,$,.SQUARE_METRE.);
#10=IFCSIUNIT(*,.VOLUMEUNIT.,$,.CUBIC_METRE.);
#11=IFCCARTESIANPOINT((0.,0.,0.));
#12=IFCDIRECTION((0.,0.,1.));
#13=IFCDIRECTION((1.,0.,0.));
#14=IFCAXIS2PLACEMENT3D(#11,#12,#13);
#15=IFCGEOMETRICREPRESENTATIONCONTEXT('3D','Model',3,1.E-005,#14,$);
#16=IFCGEOMETRICREPRESENTATIONCONTEXT($,'Plan',3,1.E-005,#14,$);
#17=IFCGEOMETRICREPRESENTATIONSUBCONTEXT('Axis','Plan',*,*,*,*,#16,0.01,.PLAN_VIEW.,$);
#18=IFCSITE('1JDQSFDXyHvfS$D1VhSTH7',#6,'TestSite',$,$,$,$,$,.ELEMENT.,$,$,$,$,$);
#19=IFCBUILDING('1JDSuXDXyHveD0D1VhSTH7',#6,'House',$,$,$,$,$,$,$,$,$);
#20=IFCBUILDINGSTOREY('1JDSuYDXyHvhXTD1VhSTH7',#6,'Floor1',$,$,#29,$,$,.ELEMENT.,1.);
#21=IFCBUILDINGSTOREY('1JDSuZDXyHvgZBD1VhSTH7',#6,'Floor2',$,$,#30,$,$,.ELEMENT.,4.);
#22=IFCBUILDINGSTOREY('1JDSuaDXyHvgbKD1VhSTH7',#6,'Roof',$,$,#31,$,$,.ELEMENT.,7.);
#23=IFCCARTESIANPOINT((0.,0.,1.));
#24=IFCCARTESIANPOINT((0.,0.,3.));
#25=IFCCARTESIANPOINT((0.,0.,3.));
#26=IFCAXIS2PLACEMENT3D(#23,$,$);
#27=IFCAXIS2PLACEMENT3D(#24,$,$);
#28=IFCAXIS2PLACEMENT3D(#25,$,$);
#29=IFCLOCALPLACEMENT($,#26);
#30=IFCLOCALPLACEMENT(#29,#27);
#31=IFCLOCALPLACEMENT(#30,#28);
#32=IFCRELAGGREGATES('1JDSubDXyHvhVcD1VhSTH7',#6,'Site2Project',$,#1,(#18));
#33=IFCRELAGGREGATES('1JDSucDXyHvg2wD1VhSTH7',#6,'Building2Site',$,#18,(#19));
#34=IFCRELAGGREGATES('1JDVKmDXyHvhiiD1VhSTH7',#6,'Storey2Building',$,#19,(#20,#21,#22));
ENDSEC;
END-ISO-10303-21;
"""

temp_filename = "./data/sample.ifc"
# temp_handle, temp_filename = tempfile.mkstemp(suffix=".ifc")
with open(temp_filename, "w") as f:
    f.write(template)

ifcfile = ifcopenshell.open(temp_filename)

owner_history = ifcfile.by_type("IfcOwnerHistory")[0]
project = ifcfile.by_type("IfcProject")[0]
context = ifcfile.by_type("IfcGeometricRepresentationContext")[0]

Floor1 = ifcfile.by_type("IfcBuildingStorey")[0]

section1 = I_Section(W=0.2 ,D=0.3 , tw=0.012 , tf=0.012  , r = 2*0.012)
section2 = Rect_Section(b= 0.2, h=0.4)
section3 = L_Section(W = 0.1 , D = 0.1 ,t = 0.012   , r=2*0.012)
section4 = U_Section(W=0.15 ,D=0.3 , tw=0.012 , tf=0.012  , r = 2*0.012)

CreateBeam(ifcfile ,Floor1, Name='Beam-Floor1-B1' ,section= section1 ,
             L=4.00 ,position=(0.0,0.0,0.0) , direction=(1.0,0.0,0.0))

CreateBeam(ifcfile ,Floor1, Name='Beam-Floor1-B1' ,section= section2 ,
             L=4.00 ,position=(0.0,0.5,0.0) , direction=(1.0,0.0,0.0))

CreateBeam(ifcfile ,Floor1, Name='Beam-Floor1-B1' ,section= section3 ,
             L=4.00 ,position=(0.0,1.0,0.0) , direction=(1.0,0.0,0.0))

CreateBeam(ifcfile ,Floor1, Name='Beam-Floor1-B1' ,section= section4 ,
             L=4.00 ,position=(0.0,1.5,0.0) , direction=(1.0,0.0,0.0))

ifcfile.write("./data/sample_new.ifc")

# myPath = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'OutPut'
# ifcfile.write(myPath + os.sep+'Test04.ifc')
