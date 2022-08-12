
def I_Section(ifcFile, W , D , tw , tf, r):
    B1_Axis2Placement2D = ifcFile.createIfcAxis2Placement2D( 
                            ifcFile.createIfcCartesianPoint( (0.,0.) ) )
    
    B1_AreaProfile = ifcFile.createIfcIShapeProfileDef('AREA')
    B1_AreaProfile.Position = B1_Axis2Placement2D 
    B1_AreaProfile.OverallWidth = W
    B1_AreaProfile.OverallDepth = D
    B1_AreaProfile.WebThickness = tw
    B1_AreaProfile.FlangeThickness = tf
    B1_AreaProfile.FilletRadius = r

    return B1_AreaProfile