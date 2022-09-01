from src.Hsteel.pvHsteel import Hsteel
from src.pvRotate import Rotate
from src.pvTranlate import Move
import pyvista as pv
import numpy as np
import math

#横構の配置

#横構のパラメータ
W = 0.2
D = 0.2
tf = 0.012
tw = 0.012
L = 3.2
s_edge = 0.2 #端部における主桁からの離隔
s_middle = 0.1 #中間部における主桁からの離隔

#主桁のパラメータ
amount_V = 3.0 #主桁の本数
interval_V = 2.5 #主桁の配置間隔

#その他配置に関するパラメータ
length = 33.0 #支間長
T = 0.5 #スラブ厚
interval_H = 5.5 #対傾構の配置間隔
amount_H = length / interval_H + 1.0 #対傾構の数
dz = 0.30


#横げたを作成
class ArrayH3:
    def CreateBeam(self, D, W, tf, tw, s_edge, s_middle, interval_H, interval_V, dz, reverse):
        L = math.sqrt((interval_H / 2.0)**2.0 + (interval_V)**2.0) - (s_edge + s_middle)
        y = -L / 2.0
        z = W / 2.0 + tf
        Model = Hsteel.CreateBeam(Hsteel, L, D, W, tf, tw, position=(0.0,y,z))
        x = s_edge - s_middle
        Model_L = Move.MoveObject(Move, obj=Model, coordinate=(x,interval_H/4.0,dz))
        Model_R = Move.MoveObject(Move, obj=Model, coordinate=(x,3.0*interval_H/4.0,dz))

        z_rotate = np.round(np.degrees(np.arctan(interval_V/(interval_H/2.0))),1)
        Model_LM = Rotate.rotate(Rotate, obj=Model_L, origine=(0.0,interval_H/4.0,dz), x_rotate=0.0, y_rotate=0.0, z_rotate=-z_rotate)
        Model_RM = Rotate.rotate(Rotate, obj=Model_R, origine=(0.0,3.0*interval_H/4.0,dz), x_rotate=0.0, y_rotate=0.0, z_rotate=z_rotate)
        Models = Model_LM + Model_RM

        if reverse == True:
            RModel_0 = Move.MoveObject(Move, obj=Models, coordinate=(0.0,0.0,-z-dz))
            RModel_R = Rotate.rotate(Rotate, obj=RModel_0, origine=(0.0,0.0,0.0), x_rotate=0.0, y_rotate=180.0, z_rotate=0.0)
            RModel = Move.MoveObject(Move, obj=RModel_R, coordinate=(0.0,0.0,z+dz))
            Models = RModel
        return Models

    #縦断方向に配置
    def Array_V(self, D, W, tf, tw, s_edge, s_middle, amount_H, interval_H, interval_V, dz, reverse):
        Models = self.CreateBeam(self, D, W, tf, tw, s_edge, s_middle, interval_H, interval_V, dz, reverse)
        VObj = []
        y = 0.0
        for i in range(int(amount_H)-1):
            Models_M = Move.MoveObject(Move, obj=Models, coordinate=(0.0,y,0.0))
            VObj.append(Models_M)
            y += interval_H

        Obj_0 = VObj[0]
        for i in range(len(VObj)-1):
            Obj_0 += VObj[i+1]
        return Obj_0

    #水平方向に配置
    def Array(self, D, W, tf, tw, s_edge, s_middle, amount_H, amount_V, interval_H, interval_V, dz, reverse):
        Obj_L = self.Array_V(self, D, W, tf, tw, s_edge, s_middle, amount_H, interval_H, interval_V, dz, reverse=False)
        Obj_R = self.Array_V(self, D, W, tf, tw, s_edge, s_middle, amount_H, interval_H, interval_V, dz, reverse=True)
        x = (amount_V - 2.0)*(interval_V / 2.0)
        if reverse == True:
            x *= -1.0
        Obj_LM = Move.MoveObject(Move, obj=Obj_L, coordinate=(-x,0.0,0.0))
        Obj_RM = Move.MoveObject(Move, obj=Obj_R, coordinate=(x,0.0,0.0))
        Obj = Obj_LM + Obj_RM
        return Obj
