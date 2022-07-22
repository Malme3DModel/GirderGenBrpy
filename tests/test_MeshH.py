import pyvista as pv
pv.rcParams['transparent_background'] = True

from src.mesh_01 import Mesh


def test_Mesh():
    msh = Mesh()
    poly = msh.createH( 50, 100, 5, 7, 1000 )

    return poly

if __name__ == "__main__":
    poly = test_Mesh()

    # objファイルを作成
    filename = 'tests/dist/' + 'msh.obj'
    pv.save_meshio(filename, poly)

    mesh = pv.read(filename)
    mesh.plot(show_edges=True)