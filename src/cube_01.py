import pyvista as pv

class Cube():

    def __init__(self):
        pass

    def createH(self, b, h, t1, t2, length):

        obj0 = pv.Cube(
            center=(b/2, t1/2, length/2),
            x_length=b,
            y_length=t1,
            z_length=length,
            bounds=None
            )
        obj1 = pv.Cube(
                center=(b/2, h/2, length/2),
                x_length= t2,
                y_length= h - t1 - t1,
                z_length=length,
                bounds=None
            )
        obj2 = pv.Cube(
                center=(b/2, h-t1/2, length/2),
                x_length= b,
                y_length= t1,
                z_length=length,
                bounds=None
            )

        poly = obj0 + obj1 + obj2

        return poly