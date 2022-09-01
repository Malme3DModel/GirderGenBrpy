from src.Lsteel.pvLsteel import Lsteel
from src.pvTranlate import Move
import pyvista as pv

#中間対傾構の配置

#主桁のパラメータ
amount_V = 4.0 #主桁の本数
interval_V = 5.0 #主桁の配置間隔
W = 1.0
D = 0.2
tw = 0.012
tf = 0.012

#中間対傾構のパラメータ
A = 0.12
B = 0.12
t = 0.009
s = 0.16 #離隔
W = W

#その他配置に関するパラメータ
length = 33.0 #支間長
interval_H = 5.5 #横構の配置間隔
amount_H = length / interval_H + 1.0
T = 0.5 #スラブ厚
location = [1,2,4,5] #中間対傾構を配置する列番号（起点側から0）



class ArrayL():
    def __init__(self):
        pass
    #対傾構を横断方向に配置
    def HArray(self, A, B, t, s, s_in, s_out, H, D, W, dz, tf, interval, amount):
        #対傾構の作成
        Model = Lsteel.add_LSteel(Lsteel, A, B, t, H, D, s, s_in, s_out, dz, tf)
        HPointlist = []
        x = -(amount - 2.0)*interval/2.0
        y = 0.0
        z = 0.0
        for i in range(int(amount)-1):
            point = [x, y, z]
            HPointlist.append(point)
            x += interval

        print(HPointlist)

        HModels = []
        for i in range(len(HPointlist)):
            HModel = Move.MoveObject(Move, Model, coordinate=HPointlist[i])
            HModels.append(HModel)

        Obj = HModels[0]
        for i in range(len(HModels)-1):
            Obj += HModels[i+1]
        return Obj

    #対傾構を縦断方向に配置
    def Array(self, A, B, t, s, s_in, s_out, H, W, D, tf, dz, amount_H, amount_V, interval_H, interval_V, location):
        obj = self.HArray(self, A, B, t, s, s_in, s_out, H, D, W, dz, tf, interval=interval_V, amount=amount_V)
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