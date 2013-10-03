from numpy import *
from scipy.integrate import odeint

class BetaArrestin:
    """
    doc string
    """
    def __init__(self):
        self.nproc = 1
        self.d = 2

    def gen_equ(self, newparams={} ):
        # parameters
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
        Stot = 0
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
        p2 = 0.1
        Di = 0.0001
        p1 = zeros(self.d)
        p3 = zeros(self.d)
        p4 = zeros(self.d)
        p1[0] = 0.1
        p3[0] = 0.1
        p4[0] = 0.1
        p1[1] = 0.1
        p3[1] = 0.1
        p4[1] = 0.1
        #}}}
        # state variables
        #{{{
        MEK          = zeros(self.d)
        MEKRAFp      = zeros_like(MEK)
        MEKp         = zeros_like(MEK)
        MEKpMEKPh    = zeros_like(MEK)
        MEKpRAFp     = zeros_like(MEK)
        MEKpp        = zeros_like(MEK)
        MEKppMEKPh   = zeros_like(MEK)
        MAPK         = zeros_like(MEK)
        MAPKMEKpp    = zeros_like(MEK)
        MAPKp        = zeros_like(MEK)
        MAPKpMEKpp   = zeros_like(MEK)
        MAPKpp       = zeros_like(MEK)
        MAPKpMAPKPh  = zeros_like(MEK)
        MAPKppMAPKPh = zeros_like(MEK)
        C1           = zeros_like(MEK)
        C2           = zeros_like(MEK)
        C3           = zeros_like(MEK)
        C4           = zeros_like(MEK)
        C5           = zeros_like(MEK)
        C6           = zeros_like(MEK)
        C7           = zeros_like(MEK)
        C8           = zeros_like(MEK)
        C9           = zeros_like(MEK)
        Smem         = zeros_like(MEK)
        Scyto        = zeros_like(MEK)
        #}}}
        # initial conditions
        #{{{
        for i in xrange(self.d):
            Scyto[i] = Stot
            MEK[i] = MEKtot
            MAPK[i] = MAPKtot

        ic = array([
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
            rhs = array( [
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

    def state_to_vec(self):
        pass

    def vec_to_state(self, vec):
        return dict( zip( [
            "Scyto[0]", "MEK[0]", "MEKRAFp[0]", "MEKp[0]", "MEKpMEKPh[0]", "MEKpRAFp[0]", "MEKpp[0]", "MEKppMEKPh[0]", "MAPK[0]", "MAPKMEKpp[0]", "MAPKp[0]", "MAPKpMEKpp[0]", "MAPKpp[0]", "MAPKpMAPKPh[0]", "MAPKppMAPKPh[0]", "C1[0]", "C2[0]", "C3[0]", "C4[0]", "C5[0]", "C6[0]", "C7[0]", "C8[0]", "C9[0]", "Smem[0]",
            "Scyto[1]", "MEK[1]", "MEKRAFp[1]", "MEKp[1]", "MEKpMEKPh[1]", "MEKpRAFp[1]", "MEKpp[1]", "MEKppMEKPh[1]", "MAPK[1]", "MAPKMEKpp[1]", "MAPKp[1]", "MAPKpMEKpp[1]", "MAPKpp[1]", "MAPKpMAPKPh[1]", "MAPKppMAPKPh[1]", "C1[1]", "C2[1]", "C3[1]", "C4[1]", "C5[1]", "C6[1]", "C7[1]", "C8[1]", "C9[1]", "Smem[1]"
        ], vec ) )

    def solve_to_steady_state( self, newparams={} ):
        tend = 1000
        MAXITER = 30
        TOL = 1e-8
        dtzero = 2*TOL
        tspan = linspace(0, tend, 100)

        ic, equ = self.gen_equ( newparams )

        numiter = 0
        tsol = [ic]
        while dtzero > TOL:
            tsol = odeint( equ, tsol[-1], tspan )
            ss = equ( tsol[-1], tend )
            dtzero = amax( abs( ss ) )
            numiter += 1
            if numiter >= MAXITER:
                break

        sol = self.vec_to_state( tsol[-1] )
        sol.update( newparams )
        sol['numiter'] = numiter
        sol['dtzero'] = dtzero
        return sol

    def runsim( self, param_list=[{}] ):
        if self.nproc == 1:
            return map( self.solve_to_steady_state, param_list )
        return pool.map( self.solve_to_steady_state, param_list )

if __name__ == "__main__":
    ba = BetaArrestin()
    sim = ba.runsim()
    print "Finished"

