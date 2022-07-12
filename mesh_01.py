from asyncore import poll3
from ftplib import parse150
import pyvista

h = 100
b = 50
t1 = 7
t2 = 5

a = (b/2)-((t1)/2)
c = b - a
h1 = h - t1


p1 = [[0, 0, 0],
          [0, t2, 0],
          [b, 0, 0]]
p2 = [[0, t2, 0],
          [b, 0, 0],
          [b, t2, 0]]
p3 = [[a, t2, 0],
          [c, t2, 0],
          [a, h1, 0]]
p4 = [[c, t2, 0],
          [a, h1, 0],
          [c, h1, 0]]
p5 = [[0, h1, 0],
          [0, h, 0],
          [b, h1, 0]]
p6 = [[0, h, 0],
          [b, h1, 0],
          [b, h, 0]]



m1 = pyvista.PolyData(p1, [3, 0, 1, 2])
m2 = pyvista.PolyData(p2, [3, 0, 1, 2])
m3 = pyvista.PolyData(p3, [3, 0, 1, 2])
m4 = pyvista.PolyData(p4, [3, 0, 1, 2])
m5 = pyvista.PolyData(p5, [3, 0, 1, 2])
m6 = pyvista.PolyData(p6, [3, 0, 1, 2])
mesh = m1 + m2 + m3 + m4 + m5 + m6
mesh.plot(cpos='xy', show_edges=True)