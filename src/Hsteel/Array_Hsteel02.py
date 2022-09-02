from src.Hsteel.pvHsteel import Hsteel
from src.pvRotate import Rotate
from src.pvTranlate import Move
import pyvista as pv

#荷重分配横桁の配置

#荷重分配横桁のパラメータ
W = 1.0
D = 0.2
tf = 0.012
tw = 0.012
location = [3] #荷重分配横桁を配置する列番号（起点側から0）
s_edge = 0.1345 #端部における主桁からの離隔
s_middle = 0.205 #中間部における主桁からの離隔

#主桁のパラメータ
amount_V = 4.0 #主桁の本数
interval_V = 2.0 #主桁の配置間隔

#その他配置に関するパラメータ
length = 33.0 #支間長
T = 0.5 #スラブ厚
interval_H = 5.5 #横構の配置間隔
amount_H = length / interval_H + 1.0 #横構の数

class ArrayH2():
    def __init__(self):
        pass
    
    def createBeam(self, D, W, tf, tw, s_edge, s_middle, dz, amount, interval): #amountは主桁の数、intervalは主桁の配置間隔
        #荷重分配横桁を作成
        Amount = amount -1.0
        L1 = interval - (s_edge + s_middle)
        L2 = interval - (s_middle * 2.0)
        y1 = -L1/2.0
        y2 = -L2/2.0
        z = (W/2.0 + tf)
        Model_E = Hsteel.CreateBeam(Hsteel, L=L1, D=D, W=W, tf=tf, tw=tw, position=(0.0,y1,z))
        Model_M = Hsteel.CreateBeam(Hsteel, L=L2, D=D, W=W, tf=tf, tw=tw, position=(0.0,y2,z))

        #荷重分配横桁を回転,移動
        dx =  s_middle - s_edge
        RModel_E = Rotate.rotate(Rotate, obj=Model_E, origine=(0.0,0.0,0.0), x_rotate=0.0, y_rotate=0.0, z_rotate=90.0)
        RModel_EL = Move.MoveObject(Move, obj=RModel_E, coordinate=(-dx, 0.0, 0.0))
        RModel_ER = Move.MoveObject(Move, obj=RModel_E, coordinate=(dx, 0.0, 0.0))
        RModel_M = Rotate.rotate(Rotate, obj=Model_M, origine=(0.0,0.0,0.0), x_rotate=0.0, y_rotate=0.0, z_rotate=90.0)

        #荷重分配横桁を水平方向に配置
        x1 = (Amount - 1.0)*interval / 2.0
        z = dz
        Obj_EL = Move.MoveObject(Move, obj=RModel_EL, coordinate=(-x1, 0.0, z))
        Obj_ER = Move.MoveObject(Move, obj=RModel_ER, coordinate=(x1, 0.0, z))

        x2 = -x1 + interval
        Models = []
        for i in range(int(Amount)-2):
            Obj_M = Move.MoveObject(Move, obj=RModel_M, coordinate=(x2, 0.0, z))
            Models.append(Obj_M)
            x2 += interval

        HObj = Obj_EL + Obj_ER
        for i in range(len(Models)):
            HObj += Models[i]
        return HObj

    def Array(self, D, W, tf, tw, s_edge, s_middle, dz, amount_H, amount_V, interval_H, interval_V, location): #"_H"は横構、"_V"は主桁を表すパラメータ
        obj = self.createBeam(self, D, W, tf, tw, s_edge, s_middle, dz, amount=amount_V, interval=interval_V)
        #荷重分配横桁を縦断方向に配置
        VPointlist = []
        x = 0.0
        y = 0.0
        z = 0.0
        for i in range(int(amount_H)):
            VPoint = [x,y,z]
            VPointlist.append(VPoint)
            y += interval_H

        VModels = []
        for i in range(int(amount_H)):
            VModel = Move.MoveObject(Move, obj=obj, coordinate=VPointlist[i])
            VModels.append(VModel)

        VObj = []
        for i in range(len(location)):
            VObj.append(VModels[location[i]])

        Obj = VObj[0]
        for i in range(len(VObj)-1):
            Obj += VObj[i+1]
        return Obj


