from src.Girder import Girder

# H鋼の生成テスト
def test_Hsteel():
    girder = Girder()
    girder.add_Beam(W=0.2, D=0.3, tw=0.012, tf=0.012, r = 2*0.012,
                    L=4.00, position=(0.0,2.0,0.0), direction=(1.0,0.0,0.0))

    girder.add_Beam(W=0.2, D=0.3, tw=0.012, tf=0.012, r = 2*0.012,
                    L=4.00, position=(0.0,0.5,0.0), direction=(1.0,0.0,0.0))

    girder.add_Beam(W=0.2, D=0.3, tw=0.012, tf=0.012, r = 2*0.012,
                    L=4.00, position=(0.0,1.0,0.0), direction=(1.0,0.0,0.0))


    return girder.ifc.file


# スラブの生成テスト
def test_Slab():
    girder = Girder()
    point_list_extrusion_area = [
            (0.0, 0.0, 0.0),
            (0.0, 1.0, 0.0),
            (5.0, 1.0, 0.0),
            (5.0, 0.0, 0.0)
            ]
    girder.add_Slab(point_list_extrusion_area=point_list_extrusion_area,
                    position=(0.0,0.0,0.0) , direction=(1.0,0.0,0.0))
    return girder.ifc.file


# 鉄筋の生成テスト
def test_Rebar():
    girder = Girder()
    girder.add_Rebar(position=(0.0,0.0,0.0) , direction=(1.0,0.0,0.0))

    return girder.ifc.file


if __name__ == "__main__":

    #ifcFile = test_Hsteel()
    ifcFile = test_Slab()
    ifcFile.write("./data/sample_new55.ifc")

