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
    ID = 1;
    for key in ["pavement", "slab", "cross", "mid", "crossbeam"]:
        value = body[key]
        # 階層3を作成
        Box = Obj.CreateBox(Container=Container, Name=value['Name'], ObjectType=value['Name'], ID=str(ID), Class=value['Name'], Info=value['Info'], Type=value['Type'], Standard=value['Standard'])
        # 階層4を作成
        ID2 = 1
        N = 0
        for j in range(len(value['obj'])):
            v_model ,f_model = createObject(value['obj'][j])
            for i in range(len(v_model)):
                Name = value['Name_s']
                if len(Name) == 0:
                    Name = ""
                else :
                    Name = value['Name_s'][N]
                Type = value['Type_s']
                if len(Type) == 0:
                    Type = ""
                else :
                    Type = value['Type_s'][j]
                Info = value['Info_s']
                if len(Info) == 0:
                    Info = ""
                else :
                    Info = value['Info_s'][i]
                Standard = value['Standard_s']
                if len(Standard) == 0:
                    Standard = ""
                else :
                    Standard = value['Standard_s'][j]
                Obj.add_Obj(vertices=v_model[i], faces=f_model[i], Container=Box, Name3=Name, ObjectType=Type, ID=str(ID2), Class=Name, Info=Info, Standard=Standard)
                ID2 += 1
                N += 1
        ID += 1

    beam = body['beam']
    for i in range(len(beam['obj'])):
        # 階層3を作成
        beamBox = Obj.CreateBox(Container=Container, Name=beam['Name'], ObjectType=beam['Name'], ID=str(ID), Class=beam['Name'], Info=beam['Info'][i], Type='', Standard='')
        # 階層4を作成
        ID2 = 1
        v_model ,f_model = createObject(beam['obj'][i])
        for k in range(len(v_model)):
            Obj.add_Obj(vertices=v_model[k], faces=f_model[k], Container=beamBox, Name3=beam['Name_s'][k], ObjectType=beam['Type_s'][k], ID=str(ID2), Class=beam['Name_s'][k], Info='', Standard='')
            ID2 += 1
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