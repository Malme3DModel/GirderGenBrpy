from src.Hsteel.Array_Hsteel01 import ArrayH1
from src.Hsteel.Array_Hsteel02 import ArrayH2
from src.Hsteel.Array_Hsteel03 import ArrayH3
from src.Hsteel.Array_Hsteel04 import ArrayH4
from src.Lsteel.Array_Lsteel import ArrayL
from src.Slab.pvSlab import AddSlab
from src.pvTranlate import Move
import pyvista as pv

def createGirder(plam):

    #スラブのパラメータ
    pSlab = plam['slab']
    b1 = pSlab['b1']
    b2 = pSlab['b2']
    b3 = pSlab['b3']
    i1 = pSlab['i1']
    i2 = pSlab['i2']
    SH = pSlab['SH']
    T1 = pSlab['T1']
    T2 = pSlab['T2']
    n = pSlab['n'] #1:n
    Ss = pSlab['Ss'] #端部から主桁中心までの離隔
    SB = b1 + b2 + b3*2.0


    #主桁のパラメータ
    pBeam = plam['beam']
    amount_V = pBeam['amount_V'] #主桁の本数
    W = pBeam['W']
    D = pBeam['D']
    tw = pBeam['tw']
    tf = pBeam['tf']
    interval_V = (SB-2*Ss)/(amount_V-1.0) #主桁の配置間隔

    #中間対傾構のパラメータ
    pMid = plam['mid']
    A = pMid['A']
    B = pMid['B']
    H = pMid['H']
    t = pMid['t']
    s = pMid['s'] #離隔
    D2 = interval_V / 2.0 - s
    s_in = pMid['s_in']
    s_out = pMid['s_out']

    dz = pMid['dz'] #ウェブから対傾構までの離隔

    #横構のパラメータ
    pCross = plam['cross']
    W2 = pCross['W2']
    D3 = pCross['D3']
    tf2 = pCross['tf2']
    tw2 = pCross['tw2']
    s_edge = pCross['s_edge'] #端部における主桁からの離隔
    s_middle = pCross['s_middle']  #中間部における主桁からの離隔
    z = (dz + H + tf) - (W2 + tf2 * 2.0)

    #荷重分配横桁のパラメータ
    pCrossBeam = plam['crossbeam']
    W3 = pCrossBeam['W3']
    D4 = pCrossBeam['D4']
    tf3 = pCrossBeam['tf3']
    tw3 = pCrossBeam['tw3']
    location2 = pCrossBeam['location2'] #荷重分配横桁を配置する列番号（起点側から0）
    s_edge2 = pCrossBeam['s_edge2'] #端部における主桁からの離隔
    s_middle2 = pCrossBeam['s_middle2'] #中間部における主桁からの離隔

    #端横桁のパラメータ
    pEndBeam = plam['endbeam']
    D5 = pEndBeam['D5']
    tf4 = pEndBeam['tf4']
    tw4 = pEndBeam['tw4']
    W4 = W + tf - dz
    s_edge3 = pEndBeam['s_edge3'] #端部における主桁からの離隔
    s_middle3 = pEndBeam['s_middle3'] #中間部における主桁からの離隔

    #その他配置に関するパラメータ
    pOthers = plam['others']
    s_BP = pOthers['s_BP'] #始点側端部から端横構までの離隔
    s_EP =  pOthers['s_EP'] #終点側端部から端横構までの離隔
    L = pOthers['L'] #支間長
    L2 = L + (s_BP + s_EP) #桁長
    amount_H = pOthers['amount_H'] #列数
    interval_H = L / (amount_H - 1.0)  #対傾構の配置間隔(主桁長？)
    z2 = tf * 2.0 + W + T2
    y2 = (s_BP + s_EP) / 2.0
    column = [] #中間対傾構を配置する列番号（起点側から0）
    for i in range(int(amount_H)):
        column.append(i)
    column.append(amount_H)
    location = column
    for i in range(len(location2)):
        location.remove(location2[i])
    del location[0]
    del location[len(location)-1]


    MainGirader = ArrayH1.Array(ArrayH1, L2, D, W, tf, tw, s_BP, s_EP, amount=amount_V, interval=interval_V)
    IntermediateSwayBracing = ArrayL.Array(ArrayL, A, B, t, s, s_in, s_out, H, W, D2, tf, dz, amount_H, amount_V, interval_H, interval_V, location)
    CrossBeam01_T = ArrayH3.Array(ArrayH3, D3, W2, tf2, tw2, s_edge, s_middle, amount_H, amount_V, interval_H, interval_V, dz, reverse=False)
    CrossBeam01_D = ArrayH3.Array(ArrayH3, D3, W2, tf2, tw2, s_edge, s_middle, amount_H, amount_V, interval_H, interval_V, z, reverse=True)
    CrossBeam02 = ArrayH2.Array(ArrayH2, D4, W3, tf3, tw3, s_edge2, s_middle2, dz, amount_H, amount_V, interval_H, interval_V, location2)
    CrossBeam03 = ArrayH4.Array(ArrayH4, D5, W4, tf4, tw4, s_edge3, s_middle3, dz, L, amount_V, interval_V)

    Slab = AddSlab.add_Slab(AddSlab, b1, b2, b3, i1, i2, SH, T1, T2, n, Ss, D, L2, amount_V, interval_V)
    Girder_0 = MainGirader + IntermediateSwayBracing + CrossBeam01_T + CrossBeam01_D + CrossBeam02 + CrossBeam03
    Girder = Move.MoveObject(Move, obj=Girder_0, coordinate=(0.0, y2,-z2))

    Model = Slab + Girder

    # Model.plot(cpos='xy', show_edges=True)
    return Model

