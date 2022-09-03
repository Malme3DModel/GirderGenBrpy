import pyvista as pv

from src.comon.ifcProject import ifcProject
from src.pvGirder import createGirder
from src.ifcObj import ifcObj

def createIfcGirder(
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
    ):

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

    fliePath = './tmp/Box.obj'
    pv.save_meshio(fliePath, Model.triangulate())

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

    ifcFile = exchangeIFC(vertices, faces)

    # ifc ファイルをテキストに変換する
    fliePath = "./tmp/sample_pyVista.ifc"
    ifcFile.write(fliePath)

    f = open(fliePath, "r")
    data1 = f.read() 
    f.close()

    return data1


def exchangeIFC(vertices, faces):
    # ifcファイルを生成
    ifc = ifcProject()
    # 階を生成
    Floor1 = ifc.create_place("Floor 1")
    Slab = ifcObj(ifc)

    Slab.add_Slab(vertices, faces, Floor1)
    return ifc.file