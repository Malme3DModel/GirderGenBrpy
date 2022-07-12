import pyvista as pv
pv.rcParams['transparent_background'] = True

obj0 = pv.Cube(
        center=(25.0, 2.5, 500.0), 
        x_length=50, 
        y_length=5, 
        z_length=1000, 
        bounds=None
    )
obj1 = pv.Cube(
        center=(25.0, 50.0, 500.0), 
        x_length=7, 
        y_length=90, 
        z_length=1000, 
        bounds=None
    )
obj2 = pv.Cube(
        center=(25.0, 97.5, 500.0), 
        x_length=50, 
        y_length=5, 
        z_length=1000, 
        bounds=None
    )

plotter = pv.Plotter(off_screen=False, window_size=(1000,1000))
plotter.camera.position    = (1000.0, 1000.0, 3000.0)

plotter.add_mesh(obj0 ,color="FFFFFF", show_edges=True)
plotter.add_mesh(obj1 ,color="red", show_edges=True)
plotter.add_mesh(obj2 ,color="FFFFFF", show_edges=True)

plotter.show()