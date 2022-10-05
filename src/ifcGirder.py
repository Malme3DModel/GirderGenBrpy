import os
from src.comon.comon import *
from src.comon.ifcProject import ifcProject
from src.comon.ifcObj import ifcObj

def createObject(obj):
    ## obj ファイル情報を抽出
    if not 'obj' in obj:
        raise 'obj not found'
    strObj = obj['obj']

    # obj ファイルを読む
    vertices = []
    faces = []

    for i in range(len(strObj)):
        v_list = []
        f_list = []
        rows = strObj[i].split('\n')
        for line in rows:
            vals = line.split()

            if len(vals) == 0:
                continue

            if vals[0] == "v":
                v = list(map(float, vals[1:4]))
                v_list.append(v)

            if vals[0] == "f":
                fvID = []
                for f in vals[1:]:
                    w = f.split("/")
                    fvID.append(int(w[0])-1)
                f_list.append(fvID)

        vertices.append(v_list)
        faces.append(f_list)
    return vertices, faces

def createIfcGirder(body):
    # 送られた引数から値を取り出す
    ProjectName = body['ProjectName']
    beam = body['beam']
    v_beam ,f_beam = createObject(beam)
    mid_l = body['mid_l']
    v_mid_l ,f_mid_l = createObject(mid_l)
    mid_u = body['mid_u']
    v_mid_u ,f_mid_u = createObject(mid_u)
    endbeam = body['endbeam']
    v_endbeam ,f_endbeam = createObject(endbeam)
    crossbeam = body['crossbeam']
    v_crossbeam ,f_crossbeam = createObject(crossbeam)

    # obj ファイルを ifc に変換
    # ifcファイルを生成
    # プロジェクト名と階層1のオブジェクト名を指定
    ifc = ifcProject(ProjectName, "橋梁")
    # モデル空間を作成
    # 階層2のオブジェクト名を指定
    Container = ifc.create_place("上部構造")
    Obj = ifcObj(ifc)
        # 主桁を格納する場所を追加
    import ifcopenshell
    B0 = ifc.file.create_entity(
        "IfcBuildingElementProxy",
        GlobalId = create_guid(),
        Name = "主桁を格納する場所"
    )
    B0_Placement = ifc.file.createIfcLocalPlacement(Container.ObjectPlacement)
    B0.ObjectPlacement=B0_Placement

    Flr1_Container = ifc.file.createIfcRelContainedInSpatialStructure(create_guid(), ifc.owner_hist)
    Flr1_Container.RelatedElements=[B0]
    Flr1_Container.RelatingStructure= Container

    #モデルの追加
    # 階層3のオブジェクト名を指定
    for i in range(len(v_beam)):
        Info = '主桁{:0=2}'.format(i+1)
        Obj.add_Obj(vertices=v_beam[i], faces=f_beam[i], Container=Container, Name3="主桁", ID=str(i), Class='主桁', Info=Info, Type='鋼橋鈑桁')

    ID_mid = 0
    for i in range(len(v_mid_u)):
        Info_l = '下横構{:0=2}'.format(i+1)
        Info_u = '上横構{:0=2}'.format(i+1)
        Obj.add_Obj(vertices=v_mid_l[i], faces=f_mid_l[i], Container=Container, Name3="横構", ID=str(ID_mid), Class='下横構', Info=Info_l, Type='')
        Obj.add_Obj(vertices=v_mid_u[i], faces=f_mid_u[i], Container=Container, Name3="横構", ID=str(ID_mid+1), Class='上横構', Info=Info_u, Type='')
        ID_mid += 2

    for i in range(len(v_endbeam)):
        Info = '端横桁{:0=2}'.format(i+1)
        Obj.add_Obj(vertices=v_endbeam[i], faces=f_endbeam[i], Container=Container, Name3="端横桁", ID=str(i), Class='端横桁', Info=Info, Type='')

    for i in range(len(v_endbeam)):
        Info = '端横桁{:0=2}'.format(i+1)
        Obj.add_Obj(vertices=v_endbeam[i], faces=f_endbeam[i], Container=Container, Name3="端横桁", ID=str(i), Class='端横桁', Info=Info, Type='')


    ifcFile = ifc.file
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
