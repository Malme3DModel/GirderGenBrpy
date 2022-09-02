import pyvista as pv

pv.rcParams['transparent_background'] = True


class Hsteel():

    def __init__(self):
        pass
    
    def CreateBeam(self, L, D, W, tf, tw, position):
        position = list(position)
        x = position[0]
        y = position[1]
        z = position[2]
        
        dx1 = tw / 2.0
        dx2 = D / 2.0
        dz1 = W / 2.0
        dz2 = dz1 + tf
        
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
        
        p1 = [a1,a2,b1]
        p2 = [a2,a3,b2]
        p3 = [a3,a4,b3]
        p4 = [a4,a5,b4]
        p5 = [a5,a6,b5]
        p6 = [a6,a7,b6]
        p7 = [a7,a8,b7]
        p8 = [a8,a9,b8]
        p9 = [a9,a10,b9]
        p10 = [a10,a11,b10]
        p11 = [a11,a12,b11]
        p12 = [a12,a1,b12]
        p13 = [b2,b1,a2]
        p14 = [b3,b2,a3]
        p15 = [b4,b3,a4]
        p16 = [b5,b4,a5]
        p17 = [b6,b5,a6]
        p18 = [b7,b6,a7]
        p19 = [b8,b7,a8]
        p20 = [b9,b8,a9]
        p21 = [b10,b9,a10]
        p22 = [b11,b10,a11]
        p23 = [b12,b11,a12]
        p24 = [b1,b12,a1]
        
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
        m15 = pv.PolyData(p15, [3, 0, 1, 2])
        m16 = pv.PolyData(p16, [3, 0, 1, 2])
        m17 = pv.PolyData(p17, [3, 0, 1, 2])
        m18 = pv.PolyData(p18, [3, 0, 1, 2])
        m19 = pv.PolyData(p19, [3, 0, 1, 2])
        m20 = pv.PolyData(p20, [3, 0, 1, 2])
        m21 = pv.PolyData(p21, [3, 0, 1, 2])
        m22 = pv.PolyData(p22, [3, 0, 1, 2])
        m23 = pv.PolyData(p23, [3, 0, 1, 2])
        m24 = pv.PolyData(p24, [3, 0, 1, 2])
        
        l1 = [a2,a3,a4]
        l2 = [a2,a4,a5]
        l3 = [a1,a6,a7]
        l4 = [a1,a7,a12]
        l5 = [a8,a9,a10]
        l6 = [a8,a10,a11]
        l7 = [b2,b3,b4]
        l8 = [b2,b4,b5]
        l9 = [b1,b6,b7]
        l10 = [b1,b7,b12]
        l11 = [b8,b9,b10]
        l12 = [b8,b10,b11]
        
        m25 = pv.PolyData(l1, [3, 0, 1, 2])
        m26 = pv.PolyData(l2, [3, 0, 1, 2])
        m27 = pv.PolyData(l3, [3, 0, 1, 2])
        m28 = pv.PolyData(l4, [3, 0, 1, 2])
        m29 = pv.PolyData(l5, [3, 0, 1, 2])
        m30 = pv.PolyData(l6, [3, 0, 1, 2])
        m31 = pv.PolyData(l7, [3, 0, 1, 2])
        m32 = pv.PolyData(l8, [3, 0, 1, 2])
        m33 = pv.PolyData(l9, [3, 0, 1, 2])
        m34 = pv.PolyData(l10, [3, 0, 1, 2])
        m35 = pv.PolyData(l11, [3, 0, 1, 2])
        m36 = pv.PolyData(l12, [3, 0, 1, 2])
        
        Model = m1+m2+m3+m4+m5+m6+m7+m8+m9+m10+m11+m12+m13+m14+m15+m16+m17+m18+m19+m20+m21+m22+m23+m24
        patch = m25+m26+m27+m28+m29+m30+m31+m32+m33+m34+m35+m36
        Model = Model + patch
        return Model