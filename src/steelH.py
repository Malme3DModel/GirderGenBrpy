import pyvista as pv

class steelH():

    def __init__(self):
        pv.rcParams['transparent_background'] = True


    def createCube(self) -> str:

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

        return "lua"