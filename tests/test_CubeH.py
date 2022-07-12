import pytest
import pyvista as pv
pv.rcParams['transparent_background'] = True

# 自作モジュール
from src.cube_01 import Cube

def test_Cube():
    cube = Cube()
    poly = cube.createH( 50, 100, 5, 7, 1000 )

    # objファイルを作成
    filename = 'tests/dist/' + 'cube.obj'
    pv.save_meshio(filename, poly)

    return filename


if __name__ == "__main__":

    filename = test_Cube()

    mesh = pv.read(filename)
    mesh.plot(show_edges=True)
