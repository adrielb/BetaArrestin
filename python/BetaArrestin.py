import numpy  as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from multiprocessing import Pool
from math import exp

# model {{{
nproc = 1

DEFAULT_PARAMS = {
    'grad'    : 1.0 ,
    'maxdose' : 0.0085 ,
    'l'       : 1.0 ,
    'dX'      : 0.0001,
    'Stot'    : 0.0 ,
    'p1'      : 0.1 ,
    'p2'      : 0.89 ,
    'p3'      : 0.1 ,
    'p4'      : 0.1 ,
    'p5'      : 7.7 ,
    'p3a'     : 0.00088 ,
    'p3b'     : 0.48 ,
    'p3c'     : 110.0 ,
    'p3d'     : 0.02 ,
    'p3e'     : 1.5 ,
    'p3f'     : 2.1 ,
    'p4a'     : 0.01 ,
    'p4b'     : 6.5 ,
    'Di'      : 0.0001
}

def gen_equ( params={} ):
    d = 2
    x = np.arange(0,d)
    p1 = np.zeros(d)
    p3 = np.zeros(d)
    p4 = np.zeros(d)
    dose = np.zeros(d)
    grad = params['grad']
    maxdose = params['maxdose']
    l = params['l']
    dX = params['dX']
    Stot = params['Stot']
    p1[0] = params['p1']
    p1[1] = params['p1']
    p2    = params['p2']
    p3[0] = params['p3']
    p3[1] = params['p3']
    p4[0] = params['p4']
    p4[1] = params['p4']
    p5    = params['p5']
    p3a = params['p3a']
    p3b = params['p3b']
    p3c = params['p3c']
    p3d = params['p3d']
    p3e = params['p3e']
    p3f = params['p3f']
    p4a = params['p4a']
    p4b = params['p4b']
    Di = 0.0001
    # mapk scaffold parameters
    # {{{
    a1 = 1
    a10 = 5
    a2 = 0.5
    a3 = 3.3
    a4 = 10
    a5 = 3.3
    a6 = 10
    a7 = 20
    a8 = 5
    a9 = 20
    d1 = 0.4
    d10 = 0.4
    d2 = 0.5
    d3 = 0.42
    d4 = 0.8
    d5 = 0.4
    d6 = 0.8
    d7 = 0.6
    d8 = 0.4
    d9 = 0.6
    k1 = 0.1
    k10 = 0.1
    k2 = 0.1
    k3 = 0.1
    k4 = 0.1
    k5 = 0.1
    k6 = 0.1
    k7 = 0.1
    k8 = 0.1
    k9 = 0.1
    MAPKPhtot = 0.3
    MAPKtot = 0.4
    MEKPhtot = 0.2
    MEKtot = 0.2
    of1 = 0.05
    of2 = 0.05
    of3 = 0.05
    of4 = 0.5
    on1 = 10
    on2 = 10
    RAFp = 0.14
    RAFPhtot = 0.3
    RAFtot = 0.3
    #}}}
    # state variables
    #{{{
    MEK          = np.zeros(d)
    MEKRAFp      = np.zeros_like(MEK)
    MEKp         = np.zeros_like(MEK)
    MEKpMEKPh    = np.zeros_like(MEK)
    MEKpRAFp     = np.zeros_like(MEK)
    MEKpp        = np.zeros_like(MEK)
    MEKppMEKPh   = np.zeros_like(MEK)
    MAPK         = np.zeros_like(MEK)
    MAPKMEKpp    = np.zeros_like(MEK)
    MAPKp        = np.zeros_like(MEK)
    MAPKpMEKpp   = np.zeros_like(MEK)
    MAPKpp       = np.zeros_like(MEK)
    MAPKpMAPKPh  = np.zeros_like(MEK)
    MAPKppMAPKPh = np.zeros_like(MEK)
    C1           = np.zeros_like(MEK)
    C2           = np.zeros_like(MEK)
    C3           = np.zeros_like(MEK)
    C4           = np.zeros_like(MEK)
    C5           = np.zeros_like(MEK)
    C6           = np.zeros_like(MEK)
    C7           = np.zeros_like(MEK)
    C8           = np.zeros_like(MEK)
    C9           = np.zeros_like(MEK)
    Smem         = np.zeros_like(MEK)
    Scyto        = np.zeros_like(MEK)
    #}}}
    # initial conditions
    #{{{
    for i in xrange(d):
        Scyto[i] = Stot
        MEK[i] = MEKtot
        MAPK[i] = MAPKtot

    ic = np.array([
            Scyto[0], MEK[0], MEKRAFp[0], MEKp[0], MEKpMEKPh[0], MEKpRAFp[0], MEKpp[0], MEKppMEKPh[0], MAPK[0], MAPKMEKpp[0], MAPKp[0], MAPKpMEKpp[0], MAPKpp[0], MAPKpMAPKPh[0], MAPKppMAPKPh[0], C1[0], C2[0], C3[0], C4[0], C5[0], C6[0], C7[0], C8[0], C9[0], Smem[0],
            Scyto[1], MEK[1], MEKRAFp[1], MEKp[1], MEKpMEKPh[1], MEKpRAFp[1], MEKpp[1], MEKppMEKPh[1], MAPK[1], MAPKMEKpp[1], MAPKp[1], MAPKpMEKpp[1], MAPKpp[1], MAPKpMAPKPh[1], MAPKppMAPKPh[1], C1[1], C2[1], C3[1], C4[1], C5[1], C6[1], C7[1], C8[1], C9[1], Smem[1]
        ])
    #}}}
    def dX_dt( X, t ):
        # unpack X into components
        (   #      0,      1,          2,       3,            4,           5,        6,             7,       8,            9,       10,            11,        12,             13,              14,    15,    16,    17,    18,    19,    20,    21,    22,    23,      24,
        # {{{
            Scyto[0], MEK[0], MEKRAFp[0], MEKp[0], MEKpMEKPh[0], MEKpRAFp[0], MEKpp[0], MEKppMEKPh[0], MAPK[0], MAPKMEKpp[0], MAPKp[0], MAPKpMEKpp[0], MAPKpp[0], MAPKpMAPKPh[0], MAPKppMAPKPh[0], C1[0], C2[0], C3[0], C4[0], C5[0], C6[0], C7[0], C8[0], C9[0], Smem[0],
            Scyto[1], MEK[1], MEKRAFp[1], MEKp[1], MEKpMEKPh[1], MEKpRAFp[1], MEKpp[1], MEKppMEKPh[1], MAPK[1], MAPKMEKpp[1], MAPKp[1], MAPKpMEKpp[1], MAPKpp[1], MAPKpMAPKPh[1], MAPKppMAPKPh[1], C1[1], C2[1], C3[1], C4[1], C5[1], C6[1], C7[1], C8[1], C9[1], Smem[1]
        # }}}
        ) = X

        dose = grad * maxdose * (l + dX * x)
        p1 = p5 * dose
        p3 = p3_func( Smem, p3a, p3b, p3c, p3d, p3e, p3f )
        p4 = p4_func( x, p4a, p4b)

        rhs = np.array( [
            #{{{
            C1[0]*p4[0] - p1[0]*Scyto[0] + Di*(-Scyto[0] + Scyto[1]) + p2*Smem[0],
            of1*(C2[0] + C6[0] + C9[0]) - a3*RAFp*MEK[0] - on1*(C1[0] + C4[0] + C5[0])*MEK[0] + Di*(-MEK[0] + MEK[1]) + k4*MEKpMEKPh[0] + d3*MEKRAFp[0],
            a3*RAFp*MEK[0] + (-d3 - k3)*MEKRAFp[0] + Di*(-MEKRAFp[0] + MEKRAFp[1]),
            -(a5*RAFp*MEKp[0]) + Di*(-MEKp[0] + MEKp[1]) + d4*MEKpMEKPh[0] - a4*MEKp[0]*(MEKPhtot - MEKpMEKPh[0] - MEKppMEKPh[0]) + k6*MEKppMEKPh[0] + d5*MEKpRAFp[0] + k3*MEKRAFp[0],
            (-d4 - k4)*MEKpMEKPh[0] + Di*(-MEKpMEKPh[0] + MEKpMEKPh[1]) + a4*MEKp[0]*(MEKPhtot - MEKpMEKPh[0] - MEKppMEKPh[0]),
            a5*RAFp*MEKp[0] + (-d5 - k5)*MEKpRAFp[0] + Di*(-MEKpRAFp[0] + MEKpRAFp[1]),
            of3*(C3[0] + C7[0] + C8[0]) + (d7 + k7)*MAPKMEKpp[0] + (d9 + k9)*MAPKpMEKpp[0] - a7*MAPK[0]*MEKpp[0] - a9*MAPKp[0]*MEKpp[0] + Di*(-MEKpp[0] + MEKpp[1]) - a6*MEKpp[0]*(MEKPhtot - MEKpMEKPh[0] - MEKppMEKPh[0]) + d6*MEKppMEKPh[0] + k5*MEKpRAFp[0],
            a6*MEKpp[0]*(MEKPhtot - MEKpMEKPh[0] - MEKppMEKPh[0]) - (d6 + k6)*MEKppMEKPh[0] + Di*(-MEKppMEKPh[0] + MEKppMEKPh[1]),
            of2*(C4[0] + C6[0] + C7[0]) - on2*(C1[0] + C2[0] + C3[0])*MAPK[0] + Di*(-MAPK[0] + MAPK[1]) + d7*MAPKMEKpp[0] + k8*MAPKpMAPKPh[0] - a7*MAPK[0]*MEKpp[0],
            (-d7 - k7)*MAPKMEKpp[0] + Di*(-MAPKMEKpp[0] + MAPKMEKpp[1]) + a7*MAPK[0]*MEKpp[0],
            k7*MAPKMEKpp[0] + Di*(-MAPKp[0] + MAPKp[1]) + d8*MAPKpMAPKPh[0] + d9*MAPKpMEKpp[0] - a8*MAPKp[0]*(MAPKPhtot - MAPKpMAPKPh[0] - MAPKppMAPKPh[0]) + k10*MAPKppMAPKPh[0] - a9*MAPKp[0]*MEKpp[0],
            (-d9 - k9)*MAPKpMEKpp[0] + Di*(-MAPKpMEKpp[0] + MAPKpMEKpp[1]) + a9*MAPKp[0]*MEKpp[0],
            of4*(C5[0] + C8[0] + C9[0]) + k9*MAPKpMEKpp[0] + Di*(-MAPKpp[0] + MAPKpp[1]) - a10*MAPKpp[0]*(MAPKPhtot - MAPKpMAPKPh[0] - MAPKppMAPKPh[0]) + d10*MAPKppMAPKPh[0],
            (-d8 - k8)*MAPKpMAPKPh[0] + Di*(-MAPKpMAPKPh[0] + MAPKpMAPKPh[1]) + a8*MAPKp[0]*(MAPKPhtot - MAPKpMAPKPh[0] - MAPKppMAPKPh[0]),
            a10*MAPKpp[0]*(MAPKPhtot - MAPKpMAPKPh[0] - MAPKppMAPKPh[0]) - (d10 + k10)*MAPKppMAPKPh[0] + Di*(-MAPKppMAPKPh[0] + MAPKppMAPKPh[1]),
            of1*C2[0] + of3*C3[0] + of2*C4[0] + of4*C5[0] - C1[0]*(on2*MAPK[0] + on1*MEK[0]) - C1[0]*p4[0] + p3[0]*Smem[0],
            -(k5*RAFp*C2[0]) + of2*C6[0] + of4*C9[0] - C2[0]*(of1 + on2*MAPK[0]) + on1*C1[0]*MEK[0],
            k5*RAFp*C2[0] - of3*C3[0] + of2*C7[0] + of4*C8[0] - on2*C3[0]*MAPK[0],
            of1*C6[0] + of3*C7[0] + on2*C1[0]*MAPK[0] - C4[0]*(of2 + on1*MEK[0]),
            of3*C8[0] + of1*C9[0] - C5[0]*(of4 + on1*MEK[0]),
            (-of1 - of2)*C6[0] - k5*RAFp*C6[0] + on2*C2[0]*MAPK[0] + on1*C4[0]*MEK[0],
            k5*RAFp*C6[0] - k9*C7[0] - of2*C7[0] - of3*C7[0] + on2*C3[0]*MAPK[0],
            k9*C7[0] - (of3 + of4)*C8[0] + k5*RAFp*C9[0],
            (-of1 - of4)*C9[0] - k5*RAFp*C9[0] + on1*C5[0]*MEK[0],
            p1[0]*Scyto[0] - p2*Smem[0] - p3[0]*Smem[0],
            C1[1]*p4[1] + Di*(Scyto[0] - Scyto[1]) - p1[1]*Scyto[1] + p2*Smem[1],
            of1*(C2[1] + C6[1] + C9[1]) + Di*(MEK[0] - MEK[1]) - a3*RAFp*MEK[1] - on1*(C1[1] + C4[1] + C5[1])*MEK[1] + k4*MEKpMEKPh[1] + d3*MEKRAFp[1],
            a3*RAFp*MEK[1] + Di*(MEKRAFp[0] - MEKRAFp[1]) + (-d3 - k3)*MEKRAFp[1],
            Di*(MEKp[0] - MEKp[1]) - a5*RAFp*MEKp[1] + d4*MEKpMEKPh[1] - a4*MEKp[1]*(MEKPhtot - MEKpMEKPh[1] - MEKppMEKPh[1]) + k6*MEKppMEKPh[1] + d5*MEKpRAFp[1] + k3*MEKRAFp[1],
            Di*(MEKpMEKPh[0] - MEKpMEKPh[1]) + (-d4 - k4)*MEKpMEKPh[1] + a4*MEKp[1]*(MEKPhtot - MEKpMEKPh[1] - MEKppMEKPh[1]),
            a5*RAFp*MEKp[1] + Di*(MEKpRAFp[0] - MEKpRAFp[1]) + (-d5 - k5)*MEKpRAFp[1],
            of3*(C3[1] + C7[1] + C8[1]) + (d7 + k7)*MAPKMEKpp[1] + (d9 + k9)*MAPKpMEKpp[1] + Di*(MEKpp[0] - MEKpp[1]) - a7*MAPK[1]*MEKpp[1] - a9*MAPKp[1]*MEKpp[1] - a6*MEKpp[1]*(MEKPhtot - MEKpMEKPh[1] - MEKppMEKPh[1]) + d6*MEKppMEKPh[1] + k5*MEKpRAFp[1],
            a6*MEKpp[1]*(MEKPhtot - MEKpMEKPh[1] - MEKppMEKPh[1]) + Di*(MEKppMEKPh[0] - MEKppMEKPh[1]) - (d6 + k6)*MEKppMEKPh[1],
            of2*(C4[1] + C6[1] + C7[1]) + Di*(MAPK[0] - MAPK[1]) - on2*(C1[1] + C2[1] + C3[1])*MAPK[1] + d7*MAPKMEKpp[1] + k8*MAPKpMAPKPh[1] - a7*MAPK[1]*MEKpp[1],
            Di*(MAPKMEKpp[0] - MAPKMEKpp[1]) + (-d7 - k7)*MAPKMEKpp[1] + a7*MAPK[1]*MEKpp[1],
            k7*MAPKMEKpp[1] + Di*(MAPKp[0] - MAPKp[1]) + d8*MAPKpMAPKPh[1] + d9*MAPKpMEKpp[1] - a8*MAPKp[1]*(MAPKPhtot - MAPKpMAPKPh[1] - MAPKppMAPKPh[1]) + k10*MAPKppMAPKPh[1] - a9*MAPKp[1]*MEKpp[1],
            Di*(MAPKpMEKpp[0] - MAPKpMEKpp[1]) + (-d9 - k9)*MAPKpMEKpp[1] + a9*MAPKp[1]*MEKpp[1],
            of4*(C5[1] + C8[1] + C9[1]) + k9*MAPKpMEKpp[1] + Di*(MAPKpp[0] - MAPKpp[1]) - a10*MAPKpp[1]*(MAPKPhtot - MAPKpMAPKPh[1] - MAPKppMAPKPh[1]) + d10*MAPKppMAPKPh[1],
            Di*(MAPKpMAPKPh[0] - MAPKpMAPKPh[1]) + (-d8 - k8)*MAPKpMAPKPh[1] + a8*MAPKp[1]*(MAPKPhtot - MAPKpMAPKPh[1] - MAPKppMAPKPh[1]),
            a10*MAPKpp[1]*(MAPKPhtot - MAPKpMAPKPh[1] - MAPKppMAPKPh[1]) + Di*(MAPKppMAPKPh[0]- MAPKppMAPKPh[1]) - (d10 + k10)*MAPKppMAPKPh[1],
            of1*C2[1] + of3*C3[1] + of2*C4[1] + of4*C5[1] - C1[1]*(on2*MAPK[1] + on1*MEK[1]) - C1[1]*p4[1] + p3[1]*Smem[1],
            -(k5*RAFp*C2[1]) + of2*C6[1] + of4*C9[1] - C2[1]*(of1 + on2*MAPK[1]) + on1*C1[1]*MEK[1],
            k5*RAFp*C2[1] - of3*C3[1] + of2*C7[1] + of4*C8[1] - on2*C3[1]*MAPK[1],
            of1*C6[1] + of3*C7[1] + on2*C1[1]*MAPK[1] - C4[1]*(of2 + on1*MEK[1]),
            of3*C8[1] + of1*C9[1] - C5[1]*(of4 + on1*MEK[1]),
            (-of1 - of2)*C6[1] - k5*RAFp*C6[1] + on2*C2[1]*MAPK[1] + on1*C4[1]*MEK[1],
            k5*RAFp*C6[1] - k9*C7[1] - of2*C7[1] - of3*C7[1] + on2*C3[1]*MAPK[1],
            k9*C7[1] - (of3 + of4)*C8[1] + k5*RAFp*C9[1],
            (-of1 - of4)*C9[1] - k5*RAFp*C9[1] + on1*C5[1]*MEK[1],
            p1[1]*Scyto[1] - p2*Smem[1] - p3[1]*Smem[1]
        #}}}
        ])
        return rhs
    return ic, dX_dt

def p3_func( Smem, a, b, c, d, e, f ):
    return (a + b * Smem) * ( (1-d) / (1 + np.exp( (Smem - e) * f) ) + d )

def p4_func( x, a, b ):
    return b - a * x

def state_to_vec():
    pass

def vec_to_state(vec):
    return dict( zip( [
        "Scyto[0]", "MEK[0]", "MEKRAFp[0]", "MEKp[0]", "MEKpMEKPh[0]", "MEKpRAFp[0]", "MEKpp[0]", "MEKppMEKPh[0]", "MAPK[0]", "MAPKMEKpp[0]", "MAPKp[0]", "MAPKpMEKpp[0]", "MAPKpp[0]", "MAPKpMAPKPh[0]", "MAPKppMAPKPh[0]", "C1[0]", "C2[0]", "C3[0]", "C4[0]", "C5[0]", "C6[0]", "C7[0]", "C8[0]", "C9[0]", "Smem[0]",
        "Scyto[1]", "MEK[1]", "MEKRAFp[1]", "MEKp[1]", "MEKpMEKPh[1]", "MEKpRAFp[1]", "MEKpp[1]", "MEKppMEKPh[1]", "MAPK[1]", "MAPKMEKpp[1]", "MAPKp[1]", "MAPKpMEKpp[1]", "MAPKpp[1]", "MAPKpMAPKPh[1]", "MAPKppMAPKPh[1]", "C1[1]", "C2[1]", "C3[1]", "C4[1]", "C5[1]", "C6[1]", "C7[1]", "C8[1]", "C9[1]", "Smem[1]"
    ], vec ) )

def solve_to_steady_state( newparams={} ):
    tend = 1000
    MAXITER = 30
    TOL = 1e-8
    dtzero = 2*TOL
    tspan = np.linspace(0, tend, 100)

    params = DEFAULT_PARAMS.copy()
    params.update( newparams )
    ic, equ = gen_equ( params )

    numiter = 0
    tsol = [ic]
    while dtzero > TOL:
        tsol = odeint( equ, tsol[-1], tspan )
        ss = equ( tsol[-1], tend )
        dtzero = np.amax( abs( ss ) )
        numiter += 1
        if numiter >= MAXITER:
            break

    sol = vec_to_state( tsol[-1] )
    sol.update( params )
    sol['numiter'] = numiter
    sol['dtzero'] = dtzero
    gdm = ( sol['grad'] * sol['dX'] * sol['maxdose'] )
    if gdm == 0.0:
        sol['MI'] = 0
    else:
        sol['MI'] = (sol['MAPKpp[1]'] - sol['MAPKpp[0]']) / gdm
    return sol

def runsim( param_list=[{}] ):
    if nproc == 1:
        sim = map( solve_to_steady_state, param_list )
    else:
        pool = Pool(processes=nproc)
        sim = pool.map( solve_to_steady_state, param_list )
        pool.close()
    return pd.DataFrame.from_dict( sim )

def dose_response( newparams={} ):
    lenX = np.arange( 0.01, 1.05, 0.05)
    param_list = [ { 'l' : l } for l in lenX ]
    for p in param_list:
        p.update( newparams )
    runsim( newparams )

# }}}

def genfig():
    fig = plt.figure()
    ax = fig.add_axes()
    ax = fig.add_subplot(1,1,1) # (nrows, ncols, axnum)
    fig.tight_layout()
    fig.show()
    return fig, ax

def max_mapk():
    p = [ {'Stot' : s, 'p1' : 100, 'p2' : 0, 'p4' : 0} for s in np.arange(0.192, .202, 0.0001) ]
    sim = runsim( p )
    MAXMAPKPP = sim['MAPKpp[0]'].max()
    return MAXMAPKPP

MAXMAPKPP = 0.0090974446462870496

