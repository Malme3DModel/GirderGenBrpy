import os
from src.comon.comon import *
from src.comon.ifcProject import ifcProject
from src.comon.ifcObj import ifcObj

def createObject(obj):
    ## obj ファイル情報を抽出
    strObj = obj

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
    ProjectName = body["ProjectName"]
    Name_R = body["RouteName"]
    Class_R = body["RoadClass"]
    Milepost_B = body["Milepost_B"]
    Milepost_E = body["Milepost_E"]
    BP = body["BP"]
    EP = body["EP"]
    # obj ファイルを ifc に変換
    # ifcファイルを生成
    # 階層1を作成
    ifc = ifcProject(ProjectName, '橋梁', Name_R, Class_R, Milepost_B, Milepost_E, BP, EP)
    # モデル空間を作成
    # 階層2を作成
    Container = ifc.create_place(Name="上部構造", ID="1", Class='上部構造', Info='', Type="単径間鋼橋鈑桁")
    Obj = ifcObj(ifc)

    #フロントから受け取ったモデル情報をIFCに変換
    # 舗装
    pavement = body["pavement"]
    # 階層3を作成
    ID = 1
    for j in range(len(pavement['obj'])):
        v_model ,f_model = createObject(pavement['obj'][j])
        for i in range(len(v_model)):
            Name_s = pavement['Name_s'][j] + '{:0=2}'.format(i+1)
            Obj.add_Obj2(vertices=v_model[i], faces=f_model[i], Container=Container, ObjectType=pavement['Name'], Name3=Name_s, ID=str(ID), Class=Name_s, Info='', Type='')
            ID += 1

    # 床版
    slab = body["slab"]
    # 階層3を作成
    slabBox = Obj.CreateBox(Container=Container, Name=slab['Name'], ObjectType=slab['Name'], ID='1', Class=slab['Class'], Info=slab['Info'], Type=slab['Type'])
    # 階層3にモデルを追加（階層4）
    for j in range(len(slab['obj'])):
        v_model ,f_model = createObject(slab['obj'][j])
        for i in range(len(v_model)):
            Name_s = slab['Name_s'][j] + '{:0=2}'.format(i+1)
            Obj.add_Obj2(vertices=v_model[i], faces=f_model[i], Container=slabBox, Name3=Name_s, ObjectType=slab['Name_s'][j], ID=str(i+1), Class=Name_s, Info='', Type='')
    # 主桁
    beam = body["beam"]
    # 階層3を作成
    ID = 1
    for j in range(len(beam['obj'])):
        v_model ,f_model = createObject(beam['obj'][j])
        for i in range(len(v_model)):
            Name_s = beam['Name_s'][j] + '{:0=2}'.format(i+1)
            Obj.add_Obj(vertices=v_model[i], faces=f_model[i], Container=Container, ObjectType=beam['Name'], Name3=Name_s, ID=str(ID), Class=Name_s, Info='', Type='')
            ID += 1
    # 横構
    cross = body["cross"]
    # 階層3を作成
    crossBox = Obj.CreateBox(Container=Container, Name=cross['Name'], ObjectType=cross['Name'], ID='3', Class=cross['Class'], Info=cross['Info'], Type=cross['Type'])
    # 階層3にモデルを追加（階層4）
    ID = 1
    for j in range(len(cross['obj'])):
        v_model ,f_model = createObject(cross['obj'][j])
        for i in range(len(v_model)):
            Name_s = cross['Name_s'][j] + '{:0=2}'.format(i+1)
            Obj.add_Obj(vertices=v_model[i], faces=f_model[i], Container=crossBox, Name3=Name_s, ObjectType=cross['Name_s'][j], ID=str(ID), Class=Name_s, Info='', Type='')
            ID += 1
    # 対傾構
    mid = body["mid"]
    # 階層3を作成
    midBox = Obj.CreateBox(Container=Container, Name=mid['Name'], ObjectType=mid['Name'], ID='4', Class=mid['Class'], Info=mid['Info'], Type=mid['Type'])
    # 階層3にモデルを追加（階層4）
    ID = 1
    for j in range(len(mid['obj'])):
        v_model ,f_model = createObject(mid['obj'][j])
        for i in range(len(v_model)):
            Name_s = mid['Name_s'][j] + '{:0=2}'.format(i+1)
            Obj.add_Obj(vertices=v_model[i], faces=f_model[i], Container=midBox, Name3=Name_s, ObjectType=mid['Name_s'][j], ID=str(ID), Class=Name_s, Info='', Type='')
            ID += 1
    # 横桁
    crossbeam = body["crossbeam"]
    # 階層3を作成
    crossbeamBox = Obj.CreateBox(Container=Container, Name=crossbeam['Name'], ObjectType=crossbeam['Name'], ID='3', Class=crossbeam['Class'], Info=crossbeam['Info'], Type=crossbeam['Type'])
    # 階層3にモデルを追加（階層4）
    ID = 1
    for j in range(len(crossbeam['obj'])):
        v_model ,f_model = createObject(crossbeam['obj'][j])
        for i in range(len(v_model)):
            Name_s = crossbeam['Name_s'][j] + '{:0=2}'.format(i+1)
            Obj.add_Obj(vertices=v_model[i], faces=f_model[i], Container=crossbeamBox, Name3=Name_s, ObjectType=crossbeam['Name_s'][j], ID=str(i+1), Class=Name_s, Info='', Type='')
            ID += 1

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