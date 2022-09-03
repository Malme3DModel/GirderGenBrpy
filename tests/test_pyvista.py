import pyvista as pv

from src.comon.ifcProject import ifcProject
from src.pvGirder import createGirder
from src.ifcObj import ifcObj

# 合成桁の生成テスト
def test_Obj():

    #スラブのパラメータ
    b1 = 4.25
    b2 = 4.25
    b3 = 0.6
    i1 = 0.02
    i2 = 0.02
    SH = 0.55
    T1 = 0.2
    T2 = 0.35
    n = 3.0 #1:n
    Ss = 1.0 #端部から主桁中心までの離隔

    #主桁のパラメータ
    amount_V = 3.0 #主桁の本数
    W = 1.70
    D = 0.31
    tw = 0.028
    tf = 0.024

    #中間対傾構のパラメータ
    A = 0.15
    B = 0.15
    H = 1.38
    t = 0.009
    s = 0.1 #離隔
    s_in = 0.16
    s_out = 0.16
    location = [1,2,4,5] #中間対傾構を配置する列番号（起点側から0）
    dz = 0.30 #ウェブから対傾構までの離隔

    #横構のパラメータ
    W2 = 0.12
    D3 = 0.18
    tf2 = 0.012
    tw2 = 0.012
    s_edge = 0.2 #端部における主桁からの離隔
    s_middle = 0.2 #中間部における主桁からの離隔

    #荷重分配横桁のパラメータ
    W3 = 1.28
    D4 = 0.25
    tf3 = 0.012
    tw3 = 0.012
    location2 = [3] #荷重分配横桁を配置する列番号（起点側から0）
    s_edge2 = 0.0 #端部における主桁からの離隔
    s_middle2 = 0.0 #中間部における主桁からの離隔

    #端横桁のパラメータ
    D5 = 0.25
    tf4 = 0.012
    tw4 = 0.012
    s_edge3 = 0.0 #端部における主桁からの離隔
    s_middle3 = 0.0 #中間部における主桁からの離隔

    #その他配置に関するパラメータ
    s_BP = 0.4 #始点側端部から端横構までの離隔
    s_EP = 0.4 #終点側端部から端横構までの離隔
    L = 33.0 #支間長
    interval_H = 5.5 #対傾構の配置間隔

    Model = createGirder(
    b1,
    b2,
    b3,
    i1,
    i2,
    SH,
    T1,
    T2,
    n,
    Ss,
    amount_V,
    W,
    D,
    tw,
    tf,
    A,
    B,
    H,
    t,
    s,
    s_in,
    s_out,
    location,
    dz,
    W2,
    D3,
    tf2,
    tw2,
    s_edge,
    s_middle,
    W3,
    D4,
    tf3,
    tw3,
    location2,
    s_edge2,
    s_middle2,
    D5,
    tf4,
    tw4,
    s_edge3,
    s_middle3,
    s_BP,
    s_EP,
    L,
    interval_H
    )

    fliePath = './data/Box.obj'
    pv.save_meshio(fliePath, Model)

    vertices = []
    faces = []

    for line in open(fliePath, "r"):
        vals = line.split()

        if len(vals) == 0:
            continue

        if vals[0] == "v":
            v = list(map(float, vals[1:4]))
            vertices.append(v)

        if vals[0] == "f":
            fvID = []
            for f in vals[1:]:
                w = f.split("/")
                fvID.append(int(w[0])-1)
            faces.append(fvID)

    return exchangeIFC(vertices, faces)


def exchangeIFC(vertices, faces):
    # ifcファイルを生成
    ifc = ifcProject()
    # 階を生成
    Floor1 = ifc.create_place("Floor 1")
    Slab = ifcObj(ifc)

    Slab.add_Slab(vertices, faces, Floor1)
    return ifc.file


if __name__ == "__main__":

    ifcFile = test_Obj()
    ifcFile.write("./data/sample_pyVista.ifc")


    # # objファイルを作成
    # Model = test_createModel()
    # filename = './data/testGirder.obj'
    # pv.save_meshio(filename, Model)

    # mesh = pv.read(filename)
    # mesh.plot(show_edges=True)
