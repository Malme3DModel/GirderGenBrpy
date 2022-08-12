# H鋼の生成テスト
from src.Hsection.ifc_H import H_IfcManager
def test_ifc_H():
    ifc = H_IfcManager()
    ifc.add_Beam(W=0.2 ,D=0.3 , tw=0.012 , tf=0.012  , r = 2*0.012,
                    L=4.00 ,position=(0.0,0.0,0.0) , direction=(1.0,0.0,0.0))

# スラブの生成テスト
from src.slab.ifc_slab import IfcManager
def test_ifc_slab():
    ifc = IfcManager()
    ifc.add_Slab(b=3 ,h=0.3,
                    L=4.00 ,position=(0.0,0.0,0.0) , direction=(1.0,0.0,0.0))


if __name__ == "__main__":

    test_ifc_H()

