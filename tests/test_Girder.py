import pyvista as pv
pv.rcParams['transparent_background'] = True

# 自作モジュール
from girder_02 import Girder

def test_girder():
    girder = Girder()
    Model = girder.parameter( 690, 1200, 4500, 4500, 500, 2, 2, 1000, 500, 100000, 50, 70, 3, 4000 )

    # objファイルを作成
    filename = 'Girder.obj'
    pv.save_meshio(filename, Model)

    return filename


if __name__ == "__main__":

    filename = test_girder()

    mesh = pv.read(filename)
    mesh.plot(show_edges=True)
