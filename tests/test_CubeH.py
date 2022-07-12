import pyvista as pv
pv.rcParams['transparent_background'] = True

from src.cube_01 import Cube


def test_Cube():
    cube = Cube()
    poly = cube.createH( 50, 100, 5, 7, 1000 )

    plotter = pv.Plotter(off_screen=False, window_size=(1000,1000))
    plotter.camera.position = (1000.0, 1000.0, 3000.0)
    plotter.add_mesh(poly ,color="FFFFFF", show_edges=True)

    plotter.show()


if __name__ == "__main__":
    test_Cube()