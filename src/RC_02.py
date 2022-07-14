from tkinter import Y
import pyvista as pv

#パラメータの計算
H = 1.2
h1 = 0.6
h2 = H - h1
B = 10.0
b1 = 4.5
b2 = 4.5
b3 = (B - b1 - b2) / 2
i1 = 2.0
i2 = 2.0
l = 100
d = 5

dh1 = b1 * i1 / 1000
dh2 = b2 * i2 / 1000

Lh1 = h1 - dh1
Lh2 = dh1
Lh3 = -(dh1 + h2)
Rh1 = h1 - dh2
Rh2 = dh2
Rh3 = -(dh2 + h2)

Lb = b1 + b3
Rb = b2 + b3

#点のプロット
n = int(l / d)
i = 0
y = 0

origin = []
C1 = []
L1 = []
L2 = []
L3 = []
L4 = []
L5 = []
R1 = []
R2 = []
R3 = []
R4 = []
R5 = []

for i in range(n):
    
    origin.append([0, y, 0])
    C1.append([0, y, Lh3])
    L1.append([-b1, y, Lh2])
    L2.append([-b1, y, Lh1])
    L3.append([-Lb, y, Lh1])
    L4.append([-Lb, y, Lh3])
    L5.append([-b1, y, Lh3])
    R1.append([b2, y, Rh2])
    R2.append([b2, y, Rh1])
    R3.append([Rb, y, Rh1])
    R4.append([Rb, y, Rh3])
    R5.append([b2, y, Rh3])
    
    y += d

#構成面を作成
face1 = L3 + L4
face2 = L2 + L3
face3 = L1 + L2
face4 = origin + L1
face5 = origin + R1
face6 = R1 + R2
face7 = R2 + R3
face8 = R3 + R4
face9 = L4 + R4

cloud1 = pv.PolyData(face1)
cloud2 = pv.PolyData(face2)
cloud3 = pv.PolyData(face3)
cloud4 = pv.PolyData(face4)
cloud5 = pv.PolyData(face5)
cloud6 = pv.PolyData(face6)
cloud7 = pv.PolyData(face7)
cloud8 = pv.PolyData(face8)
cloud9 = pv.PolyData(face9)

surf1 = cloud1.delaunay_2d()
surf2 = cloud2.delaunay_2d()
surf3 = cloud3.delaunay_2d()
surf4 = cloud4.delaunay_2d()
surf5 = cloud5.delaunay_2d()
surf6 = cloud6.delaunay_2d()
surf7 = cloud7.delaunay_2d()
surf8 = cloud8.delaunay_2d()
surf9 = cloud9.delaunay_2d()

#蓋を作成
def patch(a):
    L =L1[a] + L2[a] + L3[a] + L4[a] + L5[a]
    R = R1[a] + R2[a] + R3[a] + R4[a] + R5[a]
    C = origin[a] + L1[a] + L5[a] + C1[a] + R5[a] + R1[a]

    Lcloud = pv.PolyData(L)
    Rcloud = pv.PolyData(R)
    Ccloud = pv.PolyData(C)

    Lsurf = Lcloud.delaunay_2d()
    Rsurf = Rcloud.delaunay_2d()
    Csurf = Ccloud.delaunay_2d()

    surfs = Lsurf + Rsurf + Csurf
    return surfs

surf0 = patch(0)
surf10 = patch(n-1)

#構成面を一つにまとめる
surf = surf0 + surf1 + surf2 + surf3 + surf4 + surf5 + surf6 + surf7 + surf8 + surf9 + surf10

surf.plot(show_edges=True)