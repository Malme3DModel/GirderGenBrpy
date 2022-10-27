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
    slab = body['slab']
    v_slab ,f_slab = createObject(slab)
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
    cross_L = body['cross_L']
    v_cross_L ,f_cross_L = createObject(cross_L)
    cross_R = body['cross_R']
    v_cross_R ,f_cross_R = createObject(cross_R)
    cross_T = body['cross_T']
    v_cross_T ,f_cross_T = createObject(cross_T)
    cross_D = body['cross_D']
    v_cross_D ,f_cross_D = createObject(cross_D)
    gusset01 = body['gusset01']
    v_gusset01 ,f_gusset01 = createObject(gusset01)
    gusset02 = body['gusset02']
    v_gusset02 ,f_gusset02 = createObject(gusset02)
    gusset03 = body['gusset03']
    v_gusset03 ,f_gusset03 = createObject(gusset03)

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
    # 階層3を作成
    slabBox = Obj.CreateBox(Container=Container, Name='スラブ',ID="1", Class='スラブ', Info='', Type="RC床版")
    beamBox = Obj.CreateBox(Container=Container, Name='主桁',ID="2", Class='主桁', Info='', Type="鋼橋鈑桁")
    midBox = Obj.CreateBox(Container=Container, Name='横構',ID="3", Class='横構', Info='', Type="鋼橋鈑桁")
    crossBox = Obj.CreateBox(Container=Container, Name='対傾構',ID="4", Class='対傾構', Info='', Type="鋼橋鈑桁")
    crossbeamBox = Obj.CreateBox(Container=Container, Name='横桁',ID="5", Class='横桁', Info='', Type="鋼橋鈑桁")
    # 階層3にモデルを追加
    for i in range(len(v_slab)):
        Name_s = 'スラブ{:0=2}'.format(i+1)
        Obj.add_Obj(vertices=v_slab[i], faces=f_slab[i], Container=slabBox, Name3=Name_s, ID=str(i+1), Class=Name_s, Info='', Type='')
    
    for i in range(len(v_beam)):
        Name_b = '主桁{:0=2}'.format(i+1)
        Obj.add_Obj(vertices=v_beam[i], faces=f_beam[i], Container=beamBox, Name3=Name_b, ID=str(i+1), Class=Name_b, Info='', Type='')

    ID=0
    for i in range(len(v_mid_u)):
        Name_u = '上横構{:0=2}'.format(i+1)
        Obj.add_Obj(vertices=v_mid_u[i], faces=f_mid_u[i], Container=midBox, Name3=Name_u, ID=str(ID+1), Class=Name_u, Info='', Type='')
        ID += 1
    for i in range(len(v_mid_l)):
        Name_l = '下横構{:0=2}'.format(i+1)
        Obj.add_Obj(vertices=v_mid_l[i], faces=f_mid_l[i], Container=midBox, Name3=Name_l, ID=str(ID+1), Class=Name_l, Info='', Type='')
        ID += 1

    ID=0
    for i in range(int(len(v_endbeam)/2)):
        Name_e = '端横桁01-{:0=2}'.format(i+1)
        Obj.add_Obj(vertices=v_endbeam[i], faces=f_endbeam[i], Container=crossbeamBox, Name3="端横桁01", ID=str(ID+1), Class=Name_e, Info='', Type='')
        ID += 1
    n = int(len(v_endbeam)/2)
    for i in range(int(len(v_endbeam)/2)):
        Name_e = '端横桁02-{:0=2}'.format(i+1)
        Obj.add_Obj(vertices=v_endbeam[n], faces=f_endbeam[n], Container=crossbeamBox, Name3="端横桁02", ID=str(ID+1), Class=Name_e, Info='', Type='')
        n += 1
        ID += 1

    ID = 0
    for i in range(int(len(v_crossbeam)/len(v_endbeam))):
        Name_c = '荷重分配横桁{:0=2}'.format(i+1)
        for j in range(len(v_endbeam)):
            Name_cc = Name_c + '-{:0=2}'.format(j+1)
            Obj.add_Obj(vertices=v_crossbeam[j*(i+1)], faces=f_crossbeam[j*(i+1)], Container=crossbeamBox, Name3=Name_c, ID=str(ID+1), Class=Name_cc, Info='', Type='')
            ID += 1

    ID = 0
    for i in range(len(v_cross_L)):
        Name_r = '対傾構{:0=2}'.format(i+1)
        Name_rl = '左斜材{:0=2}'.format(i+1)
        Name_rr = '右斜材{:0=2}'.format(i+1)
        Name_rt = '上弦材{:0=2}'.format(i+1)
        Name_rd = '下弦材{:0=2}'.format(i+1)
        Obj.add_Obj(vertices=v_cross_L[i], faces=f_cross_L[i], Container=crossBox, Name3=Name_r, ID=str(ID+1), Class=Name_rl, Info='', Type='')
        Obj.add_Obj(vertices=v_cross_R[i], faces=f_cross_R[i], Container=crossBox, Name3=Name_r, ID=str(ID+1), Class=Name_rr, Info='', Type='')
        Obj.add_Obj(vertices=v_cross_T[i], faces=f_cross_T[i], Container=crossBox, Name3=Name_r, ID=str(ID+1), Class=Name_rt, Info='', Type='')
        Obj.add_Obj(vertices=v_cross_D[i], faces=f_cross_D[i], Container=crossBox, Name3=Name_r, ID=str(ID+1), Class=Name_rd, Info='', Type='')
        ID += 1

    Name_g = 'ガセットプレート（中間対傾構）'
    ID = 0
    for i in range(len(v_gusset01)):
        Name_g1 = 'ガセットプレート01-{:0=2}'.format(i+1)
        Obj.add_Obj(vertices=v_gusset01[i], faces=f_gusset01[i], Container=crossBox, Name3=Name_g1, ID=str(ID+1), Class=Name_g, Info='斜材接合用', Type='')
        ID += 1

    ID = 0
    for i in range(len(v_gusset02)):
        Name_g2 = 'ガセットプレート02-{:0=2}'.format(i+1)
        Obj.add_Obj(vertices=v_gusset02[i], faces=f_gusset02[i], Container=crossBox, Name3=Name_g2, ID=str(ID+1), Class=Name_g, Info='下弦材接合用', Type='')
        ID += 1

    ID = 0
    for i in range(len(v_gusset01)):
        Name_g3 = 'ガセットプレート03-{:0=2}'.format(i+1)
        Obj.add_Obj(vertices=v_gusset03[i], faces=f_gusset03[i], Container=crossBox, Name3=Name_g3, ID=str(ID+1), Class=Name_g, Info='上弦材接合用', Type='')
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