from src.Hsteel.Array_Hsteel01 import ArrayH1
from src.Hsteel.Array_Hsteel02 import ArrayH2
from src.Hsteel.Array_Hsteel03 import ArrayH3
from src.Hsteel.Array_Hsteel04 import ArrayH4
from src.Lsteel.Array_Lsteel import ArrayL
from src.Slab.pvSlab import AddSlab
from src.pvTranlate import Move
import pyvista as pv

def createGirder(
    b1,
    b2,
    b3,
    i1,
    i2,
    SH,
    T1,
    T2,
    n,
    Ss,
    amount_V,
    W,
    D,
    tw,
    tf,
    A,
    B,
    H,
    t,
    s,
    s_in,
    s_out,
    location,
    dz,
    W2,
    D3,
    tf2,
    tw2,
    s_edge,
    s_middle,
    W3,
    D4,
    tf3,
    tw3,
    location2,
    s_edge2,
    s_middle2,
    D5,
    tf4,
    tw4,
    s_edge3,
    s_middle3,
    s_BP,
    s_EP,
    L,
    interval_H
    ):

    #スラブのパラメータ
    # b1 = 4.25
    # b2 = 4.25
    # b3 = 0.6
    # i1 = 0.02
    # i2 = 0.02
    # SH = 0.55
    # T1 = 0.2
    # T2 = 0.35
    # n = 3.0 #1:n
    # Ss = 1.0 #端部から主桁中心までの離隔
    SB = b1 + b2 + b3


    #主桁のパラメータ
    # amount_V = 3.0 #主桁の本数
    interval_V = (SB-2*Ss)/(amount_V-1.0) #主桁の配置間隔
    # W = 1.70
    # D = 0.31
    # tw = 0.028
    # tf = 0.024

    #中間対傾構のパラメータ
    # A = 0.15
    # B = 0.15
    # H = 1.38
    # t = 0.009
    # s = 0.1 #離隔
    D2 = interval_V / 2.0 - s
    # s_in = 0.16
    # s_out = 0.16
    # location = [1,2,4,5] #中間対傾構を配置する列番号（起点側から0）
    # dz = 0.30 #ウェブから対傾構までの離隔

    #横構のパラメータ
    # W2 = 0.12
    # D3 = 0.18
    # tf2 = 0.012
    # tw2 = 0.012
    # s_edge = 0.2 #端部における主桁からの離隔
    # s_middle = 0.2 #中間部における主桁からの離隔
    z = (dz + H + tf) - (W2 + tf2 * 2.0)

    #荷重分配横桁のパラメータ
    # W3 = 1.28
    # D4 = 0.25
    # tf3 = 0.012
    # tw3 = 0.012
    # location2 = [3] #荷重分配横桁を配置する列番号（起点側から0）
    # s_edge2 = 0.0 #端部における主桁からの離隔
    # s_middle2 = 0.0 #中間部における主桁からの離隔

    #端横桁のパラメータ
    # D5 = 0.25
    # tf4 = 0.012
    # tw4 = 0.012
    W4 = W + tf - dz
    # s_edge3 = 0.0 #端部における主桁からの離隔
    # s_middle3 = 0.0 #中間部における主桁からの離隔

    #その他配置に関するパラメータ
    # s_BP = 0.4 #始点側端部から端横構までの離隔
    # s_EP = 0.4 #終点側端部から端横構までの離隔
    # L = 33.0 #支間長
    L2 = L + (s_BP + s_EP)
    # interval_H = 5.5 #対傾構の配置間隔
    amount_H = L / interval_H + 1.0
    z2 = tf * 2.0 + W + T2
    y2 = (s_BP + s_EP) / 2.0


    MainGirader = ArrayH1.Array(ArrayH1, L2, D, W, tf, tw, s_BP, s_EP, amount=amount_V, interval=interval_V)
    IntermediateSwayBracing = ArrayL.Array(ArrayL, A, B, t, s, s_in, s_out, H, W, D2, tf, dz, amount_H, amount_V, interval_H, interval_V, location)
    CrossBeam01_T = ArrayH3.Array(ArrayH3, D3, W2, tf2, tw2, s_edge, s_middle, amount_H, amount_V, interval_H, interval_V, dz, reverse=False)
    CrossBeam01_D = ArrayH3.Array(ArrayH3, D3, W2, tf2, tw2, s_edge, s_middle, amount_H, amount_V, interval_H, interval_V, z, reverse=True)
    CrossBeam02 = ArrayH2.Array(ArrayH2, D4, W3, tf3, tw3, s_edge2, s_middle2, dz, amount_H, amount_V, interval_H, interval_V, location2)
    CrossBeam03 = ArrayH4.Array(ArrayH4, D5, W4, tf4, tw4, s_edge3, s_middle3, dz, L, amount_V, interval_V)

    Slab = AddSlab.add_Slab(AddSlab, b1, b2, b3, i1, i2, SH, T1, T2, n, Ss, D, L2, amount_V, interval_V)
    Girder_0 = MainGirader + IntermediateSwayBracing + CrossBeam01_T + CrossBeam01_D + CrossBeam02 + CrossBeam03
    Girder = Move.MoveObject(Move, obj=Girder_0, coordinate=(0.0, y2,-z2))

    point = [0.0,L/2.0,0.0]
    P1 = pv.PolyData(point)

    Girder += P1

    Model = Slab + Girder + P1

    return Model

# Model.plot(cpos='xy', show_edges=True)