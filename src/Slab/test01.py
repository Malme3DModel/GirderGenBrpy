import pyvista as pv

x = 0.0
y = 0.0
z = 0.0

L = 10.0

dx1 = 0.012 / 2.0
dx2 = 0.2 / 2.0
dz1 = 0.3 / 2.0
dz2 = dz1 + 0.012

a1 = [x-dx1, y, z-dz1]
a2 = [x-dx2, y, z-dz1]
a3 = [x-dx2, y, z-dz2]
a4 = [x+dx2, y, z-dz2]
a5 = [x+dx2, y, z-dz1]
a6 = [x+dx1, y, z-dz1]
a7 = [x+dx1, y, z+dz1]
a8 = [x+dx2, y, z+dz1]
a9 = [x+dx2, y, z+dz2]
a10 = [x-dx2, y, z+dz2]
a11 = [x-dx2, y, z+dz1]
a12 = [x-dx1, y, z+dz1]

b1 = [x-dx1, y+L, z-dz1]
b2 = [x-dx2, y+L, z-dz1]
b3 = [x-dx2, y+L, z-dz2]
b4 = [x+dx2, y+L, z-dz2]
b5 = [x+dx2, y+L, z-dz1]
b6 = [x+dx1, y+L, z-dz1]
b7 = [x+dx1, y+L, z+dz1]
b8 = [x+dx2, y+L, z+dz1]
b9 = [x+dx2, y+L, z+dz2]
b10 = [x-dx2, y+L, z+dz2]
b11 = [x-dx2, y+L, z+dz1]
b12 = [x-dx1, y+L, z+dz1]

A = [a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12]
B = [b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12]
pointlist = [A,B]

Mesh = []
for i in range(len(pointlist)-1):
    A = pointlist[i]
    B = pointlist[i+1]
    C = A[1:]+A[:1]
    D = B[1:]+B[:1]
    for j in range(len(A)):
        Apoints = [A[j], C[j], B[j]]
        Bpoints = [B[j], D[j], C[j]]
        Mesh_A = pv.PolyData(Apoints, [3, 0, 1, 2])
        Mesh.append(Mesh_A)
        Mesh_B = pv.PolyData(Bpoints, [3, 0, 1, 2])
        Mesh.append(Mesh_B)
    Model = Mesh[0]
    for k in range(len(Mesh)-1):
        Model += Mesh[k+1]

Model.plot(cpos='xy', show_edges=True)
