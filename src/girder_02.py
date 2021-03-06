from inspect import Parameter
from pyexpat import model
from tkinter.messagebox import NO
from pandas import NA
import pyvista as pv

pv.rcParams['transparent_background'] = True


class Girder():

    def __init__(self):
        pass

    def parameter(self, T1, T2, B1, B2, B3, i1, i2, h, b, L, t1, t2, n ,d):
                   
        # スラブの作成
        slab = self.create_slab(T1, T2, B1, B2, B3, i1, i2, L)

        # H鋼の作成
        HHH = self.create_HHH(T1, h, b, L, t1, t2, n ,d)
    
        # 合成
        Model =  slab + HHH
        
        return Model


    #鋼桁の作成
    def create_HHH(self, T1, h, b, L, t1, t2, n ,d):
        h1 = h - t2 * 2
        x1 = -(d * (n-1)) / 2
        z1 = -(T1 + h - (t2 / 2))
        z2 = -(T1 + t2 + (h1 / 2))
        z3 = -(T1 + (t2 / 2))
        y1 = L / 2
        Model = None

        for i in range(n):
            obj0 = pv.Cube(
                center=(x1, y1, z1), 
                x_length=b, 
                y_length=L, 
                z_length=t2, 
                bounds=None
            )
            obj1 = pv.Cube(
                center=(x1, y1, z2), 
                x_length=t1, 
                y_length=L, 
                z_length=h1, 
                bounds=None
            )
            obj2 = pv.Cube(
                center=(x1, y1, z3), 
                x_length=b, 
                y_length=L, 
                z_length=t2, 
                bounds=None
            )
            x1 = x1 + d

            obj = obj0 + obj1 + obj2
            if Model == None:
                Model = obj
            else:
                Model += obj

        return Model


    #床版の作成
    def create_slab(self, T1, T2, B1, B2, B3, i1, i2, L):
        dh1 = B1 * i1 / 1000
        dh2 = B2 * i2 / 1000
        H2 = T1 - dh1
        H1 = T2 - H2

        Lh1 = H1 - dh1
        Lh2 = dh1
        Lh3 = -(dh1 + H2)
        Rh1 = H1 - dh2
        Rh2 = dh2
        Rh3 = -(dh2 + H2)

        Lb = B1 + B3
        Rb = B2 + B3

        #点のプロット
        N = 10
        D = int(L / (N-1))
        I = 0
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

        for I in range(N):
            
            origin.append([0, y, 0])
            C1.append([0, y, Lh3])
            L1.append([-B1, y, Lh2])
            L2.append([-B1, y, Lh1])
            L3.append([-Lb, y, Lh1])
            L4.append([-Lb, y, Lh3])
            L5.append([-B1, y, Lh3])
            R1.append([B2, y, Rh2])
            R2.append([B2, y, Rh1])
            R3.append([Rb, y, Rh1])
            R4.append([Rb, y, Rh3])
            R5.append([B2, y, Rh3])
            
            y += D

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
        surf10 = patch(N-1)

        #構成面を一つにまとめる
        Model = surf0 + surf1 + surf2 + surf3 + surf4 + surf5 + surf6 + surf7 + surf8 + surf9 + surf10
        
        return Model