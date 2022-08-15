"""
    合成桁を生成する
"""

from src.comon.ifcProject import ifcProject
from src.Hsteel.ifcHsteel import ifcHsteel
from src.Slab.ifcSlab import ifcSlab
from src.Rebar.ifcRebar import ifcRebar

class Girder():

    def __init__(self):
        # ifcファイルを生成
        self.ifc = ifcProject()
        # 階を生成
        self.Floor1 = self.ifc.file.by_type("IfcBuildingStorey")[0]

        self.Hsteel = ifcHsteel(self.ifc)
        self.Slab = ifcSlab(self.ifc)
        self.Rebar = ifcRebar(self.ifc)


    # H鋼の生成
    def add_Beam(self, W, D, tw, tf, r,
                    L, position, direction):
        self.Hsteel.add_Beam(W, D, tw, tf, r,
                    L, position, direction, self.Floor1)


    # スラブの生成
    def add_Slab(self, point_list_extrusion_area, position, direction):
        self.Slab.add_Slab(point_list_extrusion_area,
                    position, direction, self.Floor1)


    # 鉄筋の生成
    def add_Rebar(self, position, direction):
        self.Rebar.add_Rebar(position, direction, self.Floor1)
