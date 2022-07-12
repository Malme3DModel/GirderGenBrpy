import pyvista as pv
pv.rcParams['transparent_background'] = True

from src.mesh_01 import Mesh


def test_Mesh():
    msh = Mesh()
    poly = msh.createH( 50, 100, 5, 7, 1000 )

    # objファイルを作成
    filename = 'tests/dist/' + 'msh.obj'
    pv.save_meshio(filename, poly)

    return filename


if __name__ == "__main__":
    filename = test_Mesh()

    mesh = pv.read(filename)
    mesh.plot(show_edges=True)