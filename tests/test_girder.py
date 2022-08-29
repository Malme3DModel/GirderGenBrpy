from src.Girder import Girder

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

    ifcFile = test_Girder()

    # ifcFile = test_Girder()
    ifcFile.write("./data/sample_Girder.ifc")

