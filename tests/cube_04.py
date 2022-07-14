import pyvista as pv

pv.rcParams['transparent_background'] = True

plotter = pv.Plotter(off_screen=False, window_size=(1000,1000))
plotter.camera.position    = (100.0, 100.0, 100.0)

h = 100
b = 50
t1 = 7
t2 = 5
l = 1000
n = 10
d = 100



h1 = h - t2 * 2
x1 = b / 2
z1 = t2 / 2
z2 = t2 + (h1 / 2)
z3 = h - t2
y1 = l / 2
    
for i in range(n):
    obj0 = pv.Cube(
        center=(x1, y1, z1), 
        x_length=b, 
        y_length=l, 
        z_length=t2, 
        bounds=None
    )
    obj1 = pv.Cube(
        center=(x1, y1, z2), 
        x_length=t1, 
        y_length=l, 
        z_length=h1, 
        bounds=None
    )
    obj2 = pv.Cube(
         center=(x1, y1, z3), 
         x_length=b, 
         y_length=l, 
         z_length=t2, 
         bounds=None
    )
    
    x1 += d
    H = obj0 + obj1 + obj2
    plotter.add_mesh(H ,color="FFFFFF", show_edges=True)
        




plotter.show()