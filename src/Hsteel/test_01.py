import pyvista as pv

pv.rcParams['transparent_background'] = True

L = 10.0

point1 = [0.0, 0.0, 0.0]
point2 = [1.0, 0.0, 1.0]
point3 = [1.0, 0.0, 0.0]

points = [point1, point2, point3]

point4 = [0.0, L, 0.0]
point5 = [1.0, L, 1.0]
point6 = [1.0, L, 0.0]

points02 = [point4, point5, point6]

m1 = pv.PolyData(points, [3, 0, 1, 2])
m2 = pv.PolyData(points02, [3, 0, 1, 2])


pointlist = [points, points02]
Mesh = []

for i in range(len(pointlist)-1):
    A1 = pointlist[i]
    A2 = pointlist[i+1]
    A3 = A1[1:]+A1[:1]
    A4 = A2[1:]+A2[:1]
    for j in range(len(A1)):
        Apoints = [A1[j], A3[j], A2[j]]
        Bpoints = [A2[j], A4[j], A3[j]]
        Mesh_A = pv.PolyData(Apoints, [3, 0, 1, 2])
        Mesh.append(Mesh_A)
        Mesh_B = pv.PolyData(Bpoints, [3, 0, 1, 2])
        Mesh.append(Mesh_B)
    Obj = Mesh[0]
    for k in range(len(Mesh)-1):
        Obj += Mesh[k+1]

Obj += m1 + m2

Obj.plot(show_edges=True)