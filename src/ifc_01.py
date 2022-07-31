import ifcopenshell
from ifcopenshell import geom

class IfcManager():
    def __init__(self):
        pass


    def add_Wall(self):
        # sasa コメントアウト 
        # settings = ifcopenshell.geom.settings()
        # settings.set(settings.USE_PYTHON_OPENCASCADE, True)

        # 既存のIFCファイルを読み込む
        ifc_file = ifcopenshell.open("./data/sample.ifc")

        # 新規作成する壁のテンプレートを読み込む
        sample_wall = ifc_file.createIfcWall()

        # 座標を設定する
        context = ifc_file.by_type("IfcGeometricRepresentationContext")[0]
        point1 = ifc_file.createIfcCartesianPoint((0.0, 0.0, 0.0))
        point2 = ifc_file.createIfcCartesianPoint((5.0, 0.0, 0.0))
        ifcpts = []
        ifcpts.append(point1)
        ifcpts.append(point2)
        polyline = ifc_file.createIfcPolyLine(ifcpts)

        # 形状を設定する
        axis_representation = ifc_file.createIfcShapeRepresentation(context, "Axis", "Curve2D", [polyline])
        product_shape = ifc_file.createIfcProductDefinitionShape(None, None, [axis_representation])

        # 新規壁を追加する
        sample_wall.Representation = product_shape
        ifc_file.add(sample_wall.Representation)

        # 別ファイルとして書き出す
        ifc_file.write("./data/sample_new.ifc")