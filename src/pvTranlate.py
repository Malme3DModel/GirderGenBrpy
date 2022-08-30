import pyvista as pv

class Move():
    def __init__(self):
        pass

    def MoveObject(self, obj, coordinate):
        point = tuple(coordinate)
        Mesh = obj
        trans = Mesh.translate(point, inplace=False)
        return trans

