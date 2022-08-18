from src.Girder import Girder

# H鋼の生成テスト
def test_Beam():
    girder = Girder()
    girder.add_Beam(L=10.0,D=0.3,W=0.2,tf=0.012,tw=0.012,T=1.0,amount=3.0,interval=1.0)

    return girder.ifc.file


# スラブの生成テスト
def test_Slab():
    girder = Girder()
    girder.add_Slab(L=10.0, B=5.0, b=0.5, H=1.0, T=0.5, i=0.02)

    return girder.ifc.file


# 鉄筋の生成テスト
def test_Rebar():
    girder = Girder()
    girder.add_Rebar(position=(0.0,0.0,0.0) , direction=(1.0,0.0,0.0))

    return girder.ifc.file

# 合成桁の生成テスト
def test_Girder():
    girder = Girder()
    L=10.0
    B=5.0
    b=0.5
    H=1.0
    T=0.5
    i=0.02
    D=0.3
    W=1.0
    tf=0.012
    tw=0.012
    amount=3.0
    interval=2.0
    girder.add_Hsteel(L=L,D=D,W=W,tf=tf,tw=tw,amount=amount,interval=interval,T=T)
    girder.add_Slab(L=L,B=B,b=b,H=H,T=T,i=i)


    return girder.ifc.file



if __name__ == "__main__":

    ifcFile = test_Beam()

    # ifcFile = test_Girder()
    ifcFile.write("./data/sample_Girder.ifc")

