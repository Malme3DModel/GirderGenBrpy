import pyvista as pv

plotter = pv.Plotter(off_screen=False, window_size=(1000,1000))
plotter.camera.position    = (2500.0, 2500.0, 1000.0)

plotter.add_mesh(Model ,color="FFFFFF", show_edges=True)

plotter.show()