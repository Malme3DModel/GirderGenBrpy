import ifcopenshell
from ifcopenshell import geom

# 自作モジュール
from src.ifc_01 import IfcManager

def test_ifcopenshell():
    ifc = IfcManager()
    ifc.add_Wall()



if __name__ == "__main__":

    test_ifcopenshell()
