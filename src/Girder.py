"""
    合成桁を生成する
"""

from src.comon.ifcProject import ifcProject
from src.Hsteel.ifcHsteel import ifcHsteel
from src.Hsteel.ifcBeam import ifcBeam
from src.Slab.ifcSlab import ifcSlab
from src.Slab.ifcObj import ifcObj
from src.Slab.pvSlab import pvSlab

from src.Rebar.ifcRebar import ifcRebar

class Girder():

    def __init__(self):
        # ifcファイルを生成
        self.ifc = ifcProject()
        # 階を生成
        self.Floor1 = self.ifc.create_place("Floor 1")


    # H鋼の生成
    def add_Hsteel(self, L, D, W, tf, tw, amount, interval, T):
        Hsteel = ifcHsteel(self.ifc)
        Hsteel.add_Beam(L, D, W, tf, tw, amount, interval, T, self.Floor1)

    # H鋼の生成
    def add_Beam(self, L, D, W, tf, tw, amount, interval, T):
        Beam = ifcBeam(self.ifc)
        Beam.add_Beam(L, D, W, tf, tw, amount, interval, T, self.Floor1)

    # スラブの生成
    def add_Slab(self, L, B, b, H, T, i):
        Slab = ifcSlab(self.ifc)
        Slab.add_Slab(L, B, b, H, T, i, self.Floor1)

    # 任意形状の生成
    def add_Obj(self, vertices, faces):
        Slab = ifcObj(self.ifc)
        Slab.add_Slab(vertices, faces, self.Floor1)

    # 鉄筋の生成
    def add_Rebar(self, position, direction):
        Rebar = ifcRebar(self.ifc)
        Rebar.add_Rebar(position, direction, self.Floor1)
        
    
    def createSlab(self, H, T, b1, b2, b3, i1, i2, points, R, detail):
        Slab = pvSlab(self.ifc)
        Slab.create_mesh(H, T, b1, b2, b3, i1, i2, points, R, detail, self.Floor1)

