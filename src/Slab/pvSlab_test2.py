import pyvista as pv
import numpy as np

pv.rcParams['transparent_background'] = True


class pvSlab():

    def __init__(self):
        pass
    
    def sectional(self, H, T, b1, b2, b3, i1, i2, position):
        position = list(position)
        x = position[0]
        y = position[1]
        z = position[2]
        dx1 = -b1
        dx2 = -(b1+b3)
        dx3 = b2+b3
        dx4 = b2
        dz1 = -b1*i1
        dz2 = H-T
        dz3 = -T
        dz4 = -b2*i2
        x1 = x + dx1
        x2 = x + dx2
        x3 = x + dx3
        x4 = x + dx4
        z1 = z + dz1
        z2 = z + dz2
        z3 = z + dz3
        z4 = z + dz4
        a0 = [x, y, z]
        a1 = [x1, y, z1]
        a2 = [x1, y, z2]
        a3 = [x2, y, z2]
        a4 = [x2, y, z3]
        a5 = [x3, y, z3]
        a6 = [x3, y, z2]
        a7 = [x4, y, z2]
        a8 = [x4, y, z4]
        points = [a0, a1, a2, a3, a4, a5, a6, a7, a8]
        return points

    def alignment(self, Stations, R, detail):
        BP = Stations[0]
        PVI = Stations[1]
        EP = Stations[2]
        
        x0 = BP[0]
        y0 = BP[1]
        z0 = BP[2]
        
        x1 = PVI[0]
        y1 = PVI[1]
        z1 = PVI[2]
        
        x2 = EP[0]
        y2 = EP[1]
        z2 = EP[2]
        
        #前面勾配の算出
        length2D1 = np.sqrt((x0-x1)**2.0 + (y0-y1)**2.0)
        length3D1 = np.sqrt(length2D1**2.0 + (z0-z1)**2.0)
        i1 = (z1-z0)/length2D1
        
        #背面勾配の算出
        length2D2 = np.sqrt((x1-x2)**2.0 + (y1-y2)**2.0)
        length3D2 = np.sqrt(length2D2**2.0 + (z1-z2)**2.0)
        i2 = (z2-z1)/length2D2
        
        #VCLを算出し、曲線の始終点を計算
        VCL = R*np.absolute(i1-i2)
        
        VCP = []
        for i in range(int(detail)):
            if z0 < z1:
                d_length2D1 = length2D1 - (VCL/2.0)+(VCL/detail/2.0)*i
                dx1 = (VCL/detail/2.0)*i
                dz = ((i1-i2)*(dx1)**2.0)/(200.0*VCL)
                xvc = x0 + (d_length2D1/length2D1)*(x1-x0)
                yvc = y0 + (d_length2D1/length2D1)*(y1-y0)
                zvc = z0 + ((d_length2D1/length2D1)*(z1-z0) - dz)
                point = [xvc, yvc, zvc]
            else:
                d_length2D1 = length2D1 - (VCL/2.0)+(VCL/detail/2.0)*i
                dz = ((i1-i2)*(d_length2D1)**2.0)/(200.0*VCL)
                xvc = x0 + (d_length2D1/length2D1)*(x1-x0)
                yvc = y0 + (d_length2D1/length2D1)*(y1-y0)
                zvc = z0 - ((d_length2D1/length2D1)*(z1-z0) - dz)
                point = [xvc, yvc, zvc]
            VCP.append(point)
        
        for i in range(int(detail+1)):
            if z1 > z2:
                d_length2D2 = length2D2 - (VCL/detail/2.0)*i
                dx2 = (VCL/2.0) - (VCL/detail/2.0)*i
                dz = ((i1-i2)*(dx2)**2.0)/(200.0*VCL)
                xvc = x2 + (d_length2D2/length2D2)*(x1-x2)
                yvc = y2 + (d_length2D2/length2D2)*(y1-y2)
                zvc = z2 + ((d_length2D2/length2D2)*(z1-z2) - dz)
                point = [xvc, yvc, zvc]
            else:
                d_length2D2 = length2D2 - (VCL/detail/2.0)*i
                dz = ((i1-i2)*(d_length2D2)**2.0)/(200.0*VCL)
                xvc = x2 + (d_length2D2/length2D2)*(x1-x2)
                yvc = y2 + (d_length2D2/length2D2)*(y1-y2)
                zvc = z2 - ((d_length2D2/length2D2)*(z1-z2) - dz)
                point = [xvc, yvc, zvc]
            VCP.append(point)
        CP = []
        CP.append(BP)
        CP.insert(1,VCP)
        CP.append(EP)
        return CP
    
    def create_pointlist(self, H, T, b1, b2, b3, i1, i2, points, R, detail):
        CP = self.alignment(points, R, detail)
        pointlist = []
        for i in range(len(CP)-1):
            points = self.sectional(H, T, b1, b2, b3, i1, i2, position=CP[int(i)])
            pointlist.append(points)
        return pointlist

    def create_mesh(self, H, T, b1, b2, b3, i1, i2, points, R, detail):
        pointlist = self.create_pointlist(H, T, b1, b2, b3, i1, i2, points, R, detail)
        #筒状のメッシュを作成
        Mesh = []
        for i in range(len(pointlist)-1):
            A = pointlist[i]
            B = pointlist[i+1]
            C = A[1:]+A[:1]
            D = B[1:]+B[:1]
            for j in range(len(A)-1):
                Apoints = [A[j], C[j], B[j]]
                Bpoints = [B[j], D[j], C[j]]
                Mesh_A = pv.PolyData(Apoints, [3, 0, 1, 2])
                Mesh.append(Mesh_A)
                Mesh_B = pv.PolyData(Bpoints, [3, 0, 1, 2])
                Mesh.append(Mesh_B)
            Model = Mesh[0]
            for k in range(len(Mesh)-1):
                Model += Mesh[k+1]
        #蓋を作成(構造物ごとに作成)
        Lib1 = pointlist[0]
        Lib2 = pointlist[len(pointlist)-1]
        p1 = [Lib1[0],Lib1[1],Lib1[8]]
        p2 = [Lib1[1],Lib1[2],Lib1[3]]
        p3 = [Lib1[1],Lib1[3],Lib1[4]]
        p4 = [Lib1[1],Lib1[4],Lib1[5]]
        p5 = [Lib1[1],Lib1[5],Lib1[8]]
        p6 = [Lib1[5],Lib1[6],Lib1[8]]
        p7 = [Lib1[6],Lib1[7],Lib1[8]]
        p8 = [Lib2[0],Lib2[1],Lib2[8]]
        p9 = [Lib2[1],Lib2[2],Lib2[3]]
        p10 = [Lib2[1],Lib2[3],Lib2[4]]
        p11 = [Lib2[1],Lib2[4],Lib2[5]]
        p12 = [Lib2[1],Lib2[5],Lib2[8]]
        p13 = [Lib2[5],Lib2[6],Lib2[8]]
        p14 = [Lib2[6],Lib2[7],Lib2[8]]
        m1 = pv.PolyData(p1, [3, 0, 1, 2])
        m2 = pv.PolyData(p2, [3, 0, 1, 2])
        m3 = pv.PolyData(p3, [3, 0, 1, 2])
        m4 = pv.PolyData(p4, [3, 0, 1, 2])
        m5 = pv.PolyData(p5, [3, 0, 1, 2])
        m6 = pv.PolyData(p6, [3, 0, 1, 2])
        m7 = pv.PolyData(p7, [3, 0, 1, 2])
        m8 = pv.PolyData(p8, [3, 0, 1, 2])
        m9 = pv.PolyData(p9, [3, 0, 1, 2])
        m10 = pv.PolyData(p10, [3, 0, 1, 2])
        m11 = pv.PolyData(p11, [3, 0, 1, 2])
        m12 = pv.PolyData(p12, [3, 0, 1, 2])
        m13 = pv.PolyData(p13, [3, 0, 1, 2])
        m14 = pv.PolyData(p14, [3, 0, 1, 2])
        Model += m1+m2+m3+m4+m5+m6+m7+m8+m9+m10+m11+m12+m13+m14
        return Model

girder = pvSlab()
Model = girder.create_mesh(H=1.0, T=0.5, b1=10.0, b2=10.0, b3=0.5, i1=0.01, i2=0.01, points=[[0.0,0.0,0.0],[15.0,20.0,1.50],[30.0,40.0,0.0]], R=100.0, detail=10.0)
Model.plot(cpos='xy', show_edges=True)