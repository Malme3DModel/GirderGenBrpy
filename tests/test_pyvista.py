from src.Slab.pvObj import pvObj

# スラブの生成テスト
def test_Obj():
    pv = pvObj()
    Model = pv.CreateObj(T1=690, T2=1200, B1=4500, B2=4500, B3=500, i1=2, i2=2, L=100000)
    return Model

if __name__ == "__main__":

    Model = test_Obj()

    # ifcFile = test_Girder()
    ifcFile.write("./data/sample_Girder.ifc")