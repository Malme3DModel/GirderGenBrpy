import os
from src.comon.ifcProject import ifcProject
from src.comon.ifcObj import ifcObj

def createIfcGirder(body):

    # 送られた引数から値を取り出す
    ProjectName = body['ProjectName'] if 'ProjectName' in body else 'sample Project'
    Name1 = body['Name1'] if 'Name1' in body else 'sample Name1'
    Name2 = body['Name2'] if 'Name2' in body else 'sample Name2'
    Name3 = body['Name3'] if 'Name3' in body else 'sample Name3'
    ## obj ファイル情報を抽出
    if not 'obj' in body:
        raise 'obj not found'
    strObj = body['obj']

    # obj ファイルを読む
    vertices = []
    faces = []

    rows = strObj.split('\n')
    for line in rows:
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

    # obj ファイルを ifc に変換
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

    return data1


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
    
    return ifc.file