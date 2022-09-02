from src.Hsteel.pvHsteel import Hsteel

#主桁の配置

#主桁のパラメータ
amount_V = 4.0 #主桁の本数
interval_V = 2.0 #主桁の配置間隔
W = 1.0
D = 0.2
tw = 0.012
tf = 0.012

#その他配置に関するパラメータ
length = 33.0 #支間長

interval = interval_V
amount = amount_V

class ArrayH1():
    def __init__(self):
        pass

    def Array(self, L, D, W, tf, tw, s_BP, s_EP, amount, interval):
        pointlist = []
        x = -(amount - 1.0) * interval / 2.0
        y = -(s_BP + s_EP) / 2.0
        z = (W/2.0 + tf)
        for i in range(int(amount)):
            point = [x, y, z]
            pointlist.append(point)
            x += interval

        Models = []
        for i in range(int(amount)):
            Model = Hsteel.CreateBeam(Hsteel, L=L, D=D, W=W, tf=tf, tw=tw, position=pointlist[i])
            Models.append(Model)

        Obj = Models[0]
        for i in range(len(Models)-1):
            Obj += Models[i+1]
        return Obj
