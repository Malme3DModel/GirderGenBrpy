import pyvista as pv

class Rotate():
    def __init__(self):
        pass
    
    def rotate(self, obj, origine, x_rotate, y_rotate, z_rotate):
        x = int(x_rotate)
        y = int(y_rotate)
        z = int(z_rotate)
        Mesh = obj
        Model_x = Mesh.rotate_x(x, point = origine)
        Model_xy = Model_x.rotate_y(y, point = origine)
        Model = Model_xy.rotate_z(z, point = origine)
        return Model
