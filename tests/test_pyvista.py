import pyvista as pv

from src.comon.ifcProject import ifcProject
from src.Slab.pvObj import pvObj
from src.Slab.ifcObj import ifcObj

# スラブの生成テスト
def test_Obj():
    Model = test_createModel()
    vertices = []
    faces = []

    fliePath = './data/Box.obj'
    pv.save_meshio(fliePath, Model)

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

    # vertices = Model.points.astype(float)
    # vertices = vertices
    # faces = Model.faces.reshape(-1, 4)

    return exchangeIFC(vertices, faces)


def test_createModel():
    pv = pvObj()
    Model = pv.CreateObj(T1=690, T2=1200, B1=4500, B2=4500, B3=500, i1=2, i2=2, L=100000)
    return Model


def exchangeIFC(vertices, faces):
    # ifcファイルを生成
    ifc = ifcProject()
    # 階を生成
    Floor1 = ifc.create_place("Floor 1")
    Slab = ifcObj(ifc)

    # vertices = [
    # (-1.0, -1.0, -1.0),
    # ( 1.0, -1.0, -1.0),
    # (-1.0,  1.0, -1.0),
    # ( 1.0,  1.0, -1.0),
    # (-1.0, -1.0,  1.0),
    # ( 1.0, -1.0,  1.0),
    # (-1.0,  1.0,  1.0),
    # ( 1.0,  1.0,  1.0)
    # ]

    # faces = [
    # (0, 2, 3, 1),
    # (0, 4, 6, 2),
    # (1, 3, 7, 5),
    # (0, 1, 5, 4),
    # (2, 6, 7, 3),
    # (4, 5, 7, 6)
    # ]

    Slab.add_Slab(vertices, faces, Floor1)
    return ifc.file



if __name__ == "__main__":

    ifcFile = test_Obj()
    ifcFile.write("./data/sample_pyVista.ifc")
