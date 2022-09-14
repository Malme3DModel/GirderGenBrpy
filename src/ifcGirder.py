import os
import pyvista as pv
import ifcopenshell
import ifcopenshell.api

from src.comon.ifcProject import ifcProject
from src.pvGirder import createGirder
from src.ifcObj import ifcObj

def createIfcGirder(plam, ProjectName, Name1, Name2, Name3):

    Model = createGirder(plam)

    fliePath = './tmp'
    if 'PYVISTA_USERDATA_PATH' in os.environ:
        fliePath = os.environ['PYVISTA_USERDATA_PATH']
    fliePath += '/Box.obj'

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

    ifcFile = exchangeIFC(vertices, faces, ProjectName, Name1, Name2, Name3)

    # ifc ファイルをテキストに変換する
    fliePath = './tmp'
    if 'PYVISTA_USERDATA_PATH' in os.environ:
        fliePath = os.environ['PYVISTA_USERDATA_PATH']
    fliePath += "/sample_pyVista.ifc"

    ifcFile.write(fliePath)

    f = open(fliePath, "r")
    data1 = f.read()
    f.close()

    return ifcFile


def exchangeIFC(vertices, faces, ProjectName, Name1, Name2, Name3):
    # ifcファイルを生成
    # プロジェクト名と階層1のオブジェクト名を指定
    ifc = ifcProject(ProjectName, Name1)
    # モデル空間を作成
    # 階層2のオブジェクト名を指定
    Container = ifc.create_place(Name2)
    Obj = ifcObj(ifc)
    #モデルの追加
    # 階層3のオブジェクト名を指定
    Obj.add_Obj(vertices, faces, Container, Name3)
    
    pset = ifcopenshell.api.run("pset.add_pset", ifc, product=ifc, name="Property Set Name")
    ifcopenshell.api.run("pset.edit_pset", ifc, pset=pset, properties={"ID": "固有のID番号", "オブジェクト分類名": Name3})
    return ifc.file