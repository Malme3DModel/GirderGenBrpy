import pyvista as pv
import numpy as np
import math
from src.pvRotate import Rotate
from src.pvTranlate import Move

#対傾構を１断面分作成
class Lsteel():
    pv.rcParams['transparent_background'] = True
    
    def __init__(self):
        pass
    
    def Create_Lsteel_R(self, A, B, t, L):
        pointlist = []
        Mesh = []

        b0 = [0.0, 0.0, 0.0]
        b1 = [B, 0.0, 0.0]
        b2 = [B, t, 0.0]
        b3 = [t, t, 0.0]
        b4 = [t, A, 0.0]
        b5 = [0.0, A, 0.0]
        pointlist.append([b0, b1, b2, b3, b4, b5])

        a0 = [0.0, 0.0, L]
        a1 = [B, 0.0, L]
        a2 = [B, t, L]
        a3 = [t, t, L]
        a4 = [t, A, L]
        a5 = [0.0, A, L]
        pointlist.append([a0, a1, a2, a3, a4, a5])

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

        Lib1 = pointlist[0]
        Lib2 = pointlist[len(pointlist)-1]
        p1 = [Lib1[0],Lib1[1],Lib1[2]]
        p2 = [Lib1[0],Lib1[2],Lib1[3]]
        p3 = [Lib1[0],Lib1[3],Lib1[4]]
        p4 = [Lib1[0],Lib1[4],Lib1[5]]
        p5 = [Lib2[0],Lib2[1],Lib2[2]]
        p6 = [Lib2[0],Lib2[2],Lib2[3]]
        p7 = [Lib2[0],Lib2[3],Lib2[4]]
        p8 = [Lib2[0],Lib2[4],Lib2[5]]
        m1 = pv.PolyData(p1, [3, 0, 1, 2])
        m2 = pv.PolyData(p2, [3, 0, 1, 2])
        m3 = pv.PolyData(p3, [3, 0, 1, 2])
        m4 = pv.PolyData(p4, [3, 0, 1, 2])
        m5 = pv.PolyData(p5, [3, 0, 1, 2])
        m6 = pv.PolyData(p6, [3, 0, 1, 2])
        m7 = pv.PolyData(p7, [3, 0, 1, 2])
        m8 = pv.PolyData(p8, [3, 0, 1, 2])

        Lib = m1+m2+m3+m4+m5+m6+m7+m8
        Obj += Lib
        return Obj

    def Create_Lsteel_L(self, A, B, t, L):
        pointlist = []
        Mesh = []

        b0 = [0.0, 0.0, 0.0]
        b1 = [-B, 0.0, 0.0]
        b2 = [-B, t, 0.0]
        b3 = [-t, t, 0.0]
        b4 = [-t, A, 0.0]
        b5 = [0.0, A, 0.0]
        pointlist.append([b0, b1, b2, b3, b4, b5])

        a0 = [0.0, 0.0, L]
        a1 = [-B, 0.0, L]
        a2 = [-B, t, L]
        a3 = [-t, t, L]
        a4 = [-t, A, L]
        a5 = [0.0, A, L]
        pointlist.append([a0, a1, a2, a3, a4, a5])

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

        Lib1 = pointlist[0]
        Lib2 = pointlist[len(pointlist)-1]
        p1 = [Lib1[0],Lib1[1],Lib1[2]]
        p2 = [Lib1[0],Lib1[2],Lib1[3]]
        p3 = [Lib1[0],Lib1[3],Lib1[4]]
        p4 = [Lib1[0],Lib1[4],Lib1[5]]
        p5 = [Lib2[0],Lib2[1],Lib2[2]]
        p6 = [Lib2[0],Lib2[2],Lib2[3]]
        p7 = [Lib2[0],Lib2[3],Lib2[4]]
        p8 = [Lib2[0],Lib2[4],Lib2[5]]
        m1 = pv.PolyData(p1, [3, 0, 1, 2])
        m2 = pv.PolyData(p2, [3, 0, 1, 2])
        m3 = pv.PolyData(p3, [3, 0, 1, 2])
        m4 = pv.PolyData(p4, [3, 0, 1, 2])
        m5 = pv.PolyData(p5, [3, 0, 1, 2])
        m6 = pv.PolyData(p6, [3, 0, 1, 2])
        m7 = pv.PolyData(p7, [3, 0, 1, 2])
        m8 = pv.PolyData(p8, [3, 0, 1, 2])

        Lib = m1+m2+m3+m4+m5+m6+m7+m8
        Obj += Lib
        return Obj

    def exchange(self, obj, y_rotate, coordinate):
        Mesh = Rotate.rotate(Rotate, obj=obj, origine=(0.0,0.0,0.0), x_rotate=0.0, y_rotate=y_rotate, z_rotate=0.0)
        Model = Move.MoveObject(Move, obj=Mesh, coordinate=coordinate)
        return Model

    def add_LSteel_R(self, A, B, t, H, D, s_in, s_out, dz, tf): #Dは対傾構のx方向の長さ、Dは対傾構のy方向の長さ
        L = math.sqrt(H**2.0 + D**2.0) - (s_in + s_out) #s_cは内側の離隔 s_eは外側の離隔
        x = (s_in*D)/(L+s_in)
        z = (s_in*H)/(L+s_in) + dz + tf
        Obj = self.Create_Lsteel_R(self, A, B, t, L)
        y_rotate_R = np.round(np.degrees(np.arctan(D/H)),1)
        Model_R = self.exchange(self, obj=Obj, y_rotate=y_rotate_R, coordinate=(x,0.0,z))
        return Model_R

    def add_LSteel_L(self, A, B, t, H, D, s_in, s_out, dz, tf):
        L = math.sqrt(H**2.0 + D**2.0) - (s_in + s_out)
        x = -(s_in*D)/(L+s_in)
        z = (s_in*H)/(L+s_in) + dz + tf
        Obj = self.Create_Lsteel_L(self, A, B, t, L)
        y_rotate_L = -np.round(np.degrees(np.arctan(D/H)),1)
        Model_L = self.exchange(self, obj=Obj, y_rotate=y_rotate_L, coordinate=(x,0.0,z))
        return Model_L

    def add_LSteel_T(self, A, B, t, s, H, D, dz, tf):
        L = D * 2.0 - (s * 2.0)
        x = L / 2.0
        z = H + dz + tf
        Obj = self.Create_Lsteel_L(self, A, B, t, L)
        Model_T = self.exchange(self, obj=Obj, y_rotate=-90.0, coordinate=(x,0.0,z))
        return Model_T

    def add_LSteel_D(self, A, B, t, s, D, dz, tf):
        L = D * 2.0 - (s * 2.0)
        x = L / 2.0
        z = dz + tf
        Obj = self.Create_Lsteel_L(self, A, B, t, L)
        Model_T = self.exchange(self, obj=Obj, y_rotate=90.0, coordinate=(-x,0.0,z))
        return Model_T

    def add_LSteel(self, A, B, t, H, D, s, s_in, s_out, dz, tf):
        Model_R = self.add_LSteel_R(self, A, B, t, H, D, s_in, s_out, dz, tf)
        Model_L = self.add_LSteel_L(self, A, B, t, H, D, s_in, s_out, dz, tf)
        Model_T = self.add_LSteel_T(self, A, B, t, s, H, D, dz, tf)
        Model_D = self.add_LSteel_D(self, A, B, t, s, D, dz, tf)

        Model = Model_L + Model_R + Model_T + Model_D
        return Model
