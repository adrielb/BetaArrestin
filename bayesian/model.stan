/* Simulator
 */
functions { #{{{
  real p3_func( real Smem
              , real a
              , real b
              , real c
              , real d
              , real e
              ) {
    return (a + b * Smem) * ( (1-d) / (1 + exp( (Smem - e) * c) ) + d );
  }
  real p4_func( real x
              , real a
              , real b
              , real m
              , real n
              , real Sves
              , real dSves
              ) {
    real Sn;
    real A;

    Sn <- n * Sves + m;
    if (Sn < 0.1)
      Sn <- 0.1;
    if (Sn > 1e3)
      Sn <- 1e3;

    A <- a * tanh( dSves / Sn );
    return x * (b-A) + (1-x) * (b+A);
  }
  real[] barr_model( real t
                    , real[] y
                    , real[] theta
                    , real[] x_r
                    , int[] x_i
                    ) {
    // real var; {{{
    real dydt[50];

    real Scyto[2];
    real MEK[2];
    real MEKRAFp[2];
    real MEKp[2];
    real MEKpMEKPh[2];
    real MEKpRAFp[2];
    real MEKpp[2];
    real MEKppMEKPh[2];
    real MAPK[2];
    real MAPKMEKpp[2];
    real MAPKp[2];
    real MAPKpMEKpp[2];
    real MAPKpp[2];
    real MAPKpMAPKPh[2];
    real MAPKppMAPKPh[2];
    real C1[2];
    real C2[2];
    real C3[2];
    real C4[2];
    real C5[2];
    real C6[2];
    real C7[2];
    real C8[2];
    real C9[2];
    real Smem[2];

    vector[2] x;
    real tp;
    vector[2] p1;
    real p3[2];
    real p4[2];
    vector[2] dose;
    real grad;
    real maxdose;
    real l;
    real dX;
    real slevel;
    real Stot;
    real p2;
    real p5;
    real p3a;
    real p3b;
    real p3c;
    real p3d;
    real p3e;
    real p4a;
    real p4b;
    real p4m;
    real p4n;
    real Di;
    //}}}
    // Fixed MAPK-params:a1 <- 1 {{{
    real a1;
    real a10;
    real a2;
    real a3;
    real a4;
    real a5;
    real a6;
    real a7;
    real a8;
    real a9;
    real d1;
    real d10;
    real d2;
    real d3;
    real d4;
    real d5;
    real d6;
    real d7;
    real d8;
    real d9;
    real k1;
    real k10;
    real k2;
    real k3;
    real k4;
    real k5;
    real k6;
    real k7;
    real k8;
    real k9;
    real MAPKPhtot;
    real MAPKtot;
    real MEKPhtot;
    real MEKtot;
    real of1;
    real of2;
    real of3;
    real of4;
    real on1;
    real on2;
    real RAFp;
    real RAFPhtot;
    real RAFtot;

    a1 <- 1;
    a10 <- 5;
    a2 <- 0.5;
    a3 <- 3.3;
    a4 <- 10;
    a5 <- 3.3;
    a6 <- 10;
    a7 <- 20;
    a8 <- 5;
    a9 <- 20;
    d1 <- 0.4;
    d10 <- 0.4;
    d2 <- 0.5;
    d3 <- 0.42;
    d4 <- 0.8;
    d5 <- 0.4;
    d6 <- 0.8;
    d7 <- 0.6;
    d8 <- 0.4;
    d9 <- 0.6;
    k1 <- 0.1;
    k10 <- 0.1;
    k2 <- 0.1;
    k3 <- 0.1;
    k4 <- 0.1;
    k5 <- 0.1;
    k6 <- 0.1;
    k7 <- 0.1;
    k8 <- 0.1;
    k9 <- 0.1;
    MAPKPhtot <- 0.3;
    MAPKtot <- 0.4;
    MEKPhtot <- 0.2;
    MEKtot <- 0.2;
    of1 <- 0.05;
    of2 <- 0.05;
    of3 <- 0.05;
    of4 <- 0.5;
    on1 <- 10;
    on2 <- 10;
    RAFp <- 0.14;
    RAFPhtot <- 0.3;
    RAFtot <- 0.3;
    //}}}
    // unpacking params: Di <- theta[19] {{{
    tp      <- theta[1];
    grad    <- theta[2];
    maxdose <- theta[3];
    l       <- theta[4];
    dX      <- theta[5];
    slevel  <- theta[6];
    Stot    <- theta[7];
    p2      <- theta[8];
    p5      <- theta[9];
    p3a     <- theta[10];
    p3b     <- theta[11];
    p3c     <- theta[12];
    p3d     <- theta[13];
    p3e     <- theta[14];
    p4a     <- theta[15];
    p4b     <- theta[16];
    p4m     <- theta[17];
    p4n     <- theta[18];
    Di      <- theta[19];
//}}}
    // unpacking state   Smem[1] <- y[50] {{{
    Scyto[0]        <- y[1];
    MEK[0]          <- y[2];
    MEKRAFp[0]      <- y[3];
    MEKp[0]         <- y[4];
    MEKpMEKPh[0]    <- y[5];
    MEKpRAFp[0]     <- y[6];
    MEKpp[0]        <- y[7];
    MEKppMEKPh[0]   <- y[8];
    MAPK[0]         <- y[9];
    MAPKMEKpp[0]    <- y[10];
    MAPKp[0]        <- y[11];
    MAPKpMEKpp[0]   <- y[12];
    MAPKpp[0]       <- y[13];
    MAPKpMAPKPh[0]  <- y[14];
    MAPKppMAPKPh[0] <- y[15];
    C1[0]           <- y[16];
    C2[0]           <- y[17];
    C3[0]           <- y[18];
    C4[0]           <- y[19];
    C5[0]           <- y[20];
    C6[0]           <- y[21];
    C7[0]           <- y[22];
    C8[0]           <- y[23];
    C9[0]           <- y[24];
    Smem[0]         <- y[25];
    Scyto[1]        <- y[26];
    MEK[1]          <- y[27];
    MEKRAFp[1]      <- y[28];
    MEKp[1]         <- y[29];
    MEKpMEKPh[1]    <- y[30];
    MEKpRAFp[1]     <- y[31];
    MEKpp[1]        <- y[32];
    MEKppMEKPh[1]   <- y[33];
    MAPK[1]         <- y[34];
    MAPKMEKpp[1]    <- y[35];
    MAPKp[1]        <- y[36];
    MAPKpMEKpp[1]   <- y[37];
    MAPKpp[1]       <- y[38];
    MAPKpMAPKPh[1]  <- y[39];
    MAPKppMAPKPh[1] <- y[40];
    C1[1]           <- y[41];
    C2[1]           <- y[42];
    C3[1]           <- y[43];
    C4[1]           <- y[44];
    C5[1]           <- y[45];
    C6[1]           <- y[46];
    C7[1]           <- y[47];
    C8[1]           <- y[48];
    C9[1]           <- y[49];
    Smem[1]         <- y[50];
    //}}}
    // evaluations {{{
    x[1] <- 0;
    x[2] <- 1;

    dose <- grad * maxdose * (l + dX * x);
    p1 <- p5 * dose;
    p1 <- tp * p1;
    p2 <- tp * p2;
    p3[1] <- p3_func( Smem, p3a, p3b, p3c, p3d, p3e );
    p3[2] <- p3_func( Smem, p3a, p3b, p3c, p3d, p3e );

    Sves[1] <- C1[1] + C2[1] + C3[1] + C4[1] + C5[1] + C6[1] + C7[1] + C8[1] + C9[1];
    Sves[2] <- C1[2] + C2[2] + C3[2] + C4[2] + C5[2] + C6[2] + C7[2] + C8[2] + C9[2];

    gdm = ( grad * dX * maxdose );
    dSves = (Sves[2]-Sves[1]) / gdm;

    p4 <- p4_func( x, p4a, p4b, p4m, p4n, Sves, dSves  );

    p3 <- tp * p3;
    p4 <- tp * p4;
    //}}}
    // state equations:  dydt[50] <- f(.) {{{
    dydt[1]  <- C1[0]*p4[0] - p1[0]*Scyto[0] + Di*(-Scyto[0] + Scyto[1]) + p2*Smem[0];
    dydt[2]  <- of1*(C2[0] + C6[0] + C9[0]) - a3*RAFp*MEK[0] - on1*(C1[0] + C4[0] + C5[0])*MEK[0] + Di*(-MEK[0] + MEK[1]) + k4*MEKpMEKPh[0] + d3*MEKRAFp[0];
    dydt[3]  <- a3*RAFp*MEK[0] + (-d3 - k3)*MEKRAFp[0] + Di*(-MEKRAFp[0] + MEKRAFp[1]);
    dydt[4]  <- -(a5*RAFp*MEKp[0]) + Di*(-MEKp[0] + MEKp[1]) + d4*MEKpMEKPh[0] - a4*MEKp[0]*(MEKPhtot - MEKpMEKPh[0] - MEKppMEKPh[0]) + k6*MEKppMEKPh[0] + d5*MEKpRAFp[0] + k3*MEKRAFp[0];
    dydt[5]  <- (-d4 - k4)*MEKpMEKPh[0] + Di*(-MEKpMEKPh[0] + MEKpMEKPh[1]) + a4*MEKp[0]*(MEKPhtot - MEKpMEKPh[0] - MEKppMEKPh[0]);
    dydt[6]  <- a5*RAFp*MEKp[0] + (-d5 - k5)*MEKpRAFp[0] + Di*(-MEKpRAFp[0] + MEKpRAFp[1]);
    dydt[7]  <- of3*(C3[0] + C7[0] + C8[0]) + (d7 + k7)*MAPKMEKpp[0] + (d9 + k9)*MAPKpMEKpp[0] - a7*MAPK[0]*MEKpp[0] - a9*MAPKp[0]*MEKpp[0] + Di*(-MEKpp[0] + MEKpp[1]) - a6*MEKpp[0]*(MEKPhtot - MEKpMEKPh[0] - MEKppMEKPh[0]) + d6*MEKppMEKPh[0] + k5*MEKpRAFp[0];
    dydt[8]  <- a6*MEKpp[0]*(MEKPhtot - MEKpMEKPh[0] - MEKppMEKPh[0]) - (d6 + k6)*MEKppMEKPh[0] + Di*(-MEKppMEKPh[0] + MEKppMEKPh[1]);
    dydt[9]  <- of2*(C4[0] + C6[0] + C7[0]) - on2*(C1[0] + C2[0] + C3[0])*MAPK[0] + Di*(-MAPK[0] + MAPK[1]) + d7*MAPKMEKpp[0] + k8*MAPKpMAPKPh[0] - a7*MAPK[0]*MEKpp[0];
    dydt[10] <- (-d7 - k7)*MAPKMEKpp[0] + Di*(-MAPKMEKpp[0] + MAPKMEKpp[1]) + a7*MAPK[0]*MEKpp[0];
    dydt[11] <- k7*MAPKMEKpp[0] + Di*(-MAPKp[0] + MAPKp[1]) + d8*MAPKpMAPKPh[0] + d9*MAPKpMEKpp[0] - a8*MAPKp[0]*(MAPKPhtot - MAPKpMAPKPh[0] - MAPKppMAPKPh[0]) + k10*MAPKppMAPKPh[0] - a9*MAPKp[0]*MEKpp[0];
    dydt[12] <- (-d9 - k9)*MAPKpMEKpp[0] + Di*(-MAPKpMEKpp[0] + MAPKpMEKpp[1]) + a9*MAPKp[0]*MEKpp[0];
    dydt[13] <- of4*(C5[0] + C8[0] + C9[0]) + k9*MAPKpMEKpp[0] + Di*(-MAPKpp[0] + MAPKpp[1]) - a10*MAPKpp[0]*(MAPKPhtot - MAPKpMAPKPh[0] - MAPKppMAPKPh[0]) + d10*MAPKppMAPKPh[0];
    dydt[14] <- (-d8 - k8)*MAPKpMAPKPh[0] + Di*(-MAPKpMAPKPh[0] + MAPKpMAPKPh[1]) + a8*MAPKp[0]*(MAPKPhtot - MAPKpMAPKPh[0] - MAPKppMAPKPh[0]);
    dydt[15] <- a10*MAPKpp[0]*(MAPKPhtot - MAPKpMAPKPh[0] - MAPKppMAPKPh[0]) - (d10 + k10)*MAPKppMAPKPh[0] + Di*(-MAPKppMAPKPh[0] + MAPKppMAPKPh[1]);
    dydt[16] <- of1*C2[0] + of3*C3[0] + of2*C4[0] + of4*C5[0] - C1[0]*(on2*MAPK[0] + on1*MEK[0]) - C1[0]*p4[0] + p3[0]*Smem[0];
    dydt[17] <- -(k5*RAFp*C2[0]) + of2*C6[0] + of4*C9[0] - C2[0]*(of1 + on2*MAPK[0]) + on1*C1[0]*MEK[0];
    dydt[18] <- k5*RAFp*C2[0] - of3*C3[0] + of2*C7[0] + of4*C8[0] - on2*C3[0]*MAPK[0];
    dydt[19] <- of1*C6[0] + of3*C7[0] + on2*C1[0]*MAPK[0] - C4[0]*(of2 + on1*MEK[0]);
    dydt[20] <- of3*C8[0] + of1*C9[0] - C5[0]*(of4 + on1*MEK[0]);
    dydt[21] <- (-of1 - of2)*C6[0] - k5*RAFp*C6[0] + on2*C2[0]*MAPK[0] + on1*C4[0]*MEK[0];
    dydt[22] <- k5*RAFp*C6[0] - k9*C7[0] - of2*C7[0] - of3*C7[0] + on2*C3[0]*MAPK[0];
    dydt[23] <- k9*C7[0] - (of3 + of4)*C8[0] + k5*RAFp*C9[0];
    dydt[24] <- (-of1 - of4)*C9[0] - k5*RAFp*C9[0] + on1*C5[0]*MEK[0];
    dydt[25] <- p1[0]*Scyto[0] - p2*Smem[0] - p3[0]*Smem[0];
    dydt[26] <- C1[1]*p4[1] + Di*(Scyto[0] - Scyto[1]) - p1[1]*Scyto[1] + p2*Smem[1];
    dydt[27] <- of1*(C2[1] + C6[1] + C9[1]) + Di*(MEK[0] - MEK[1]) - a3*RAFp*MEK[1] - on1*(C1[1] + C4[1] + C5[1])*MEK[1] + k4*MEKpMEKPh[1] + d3*MEKRAFp[1];
    dydt[28] <- a3*RAFp*MEK[1] + Di*(MEKRAFp[0] - MEKRAFp[1]) + (-d3 - k3)*MEKRAFp[1];
    dydt[29] <- Di*(MEKp[0] - MEKp[1]) - a5*RAFp*MEKp[1] + d4*MEKpMEKPh[1] - a4*MEKp[1]*(MEKPhtot - MEKpMEKPh[1] - MEKppMEKPh[1]) + k6*MEKppMEKPh[1] + d5*MEKpRAFp[1] + k3*MEKRAFp[1];
    dydt[30] <- Di*(MEKpMEKPh[0] - MEKpMEKPh[1]) + (-d4 - k4)*MEKpMEKPh[1] + a4*MEKp[1]*(MEKPhtot - MEKpMEKPh[1] - MEKppMEKPh[1]);
    dydt[31] <- a5*RAFp*MEKp[1] + Di*(MEKpRAFp[0] - MEKpRAFp[1]) + (-d5 - k5)*MEKpRAFp[1];
    dydt[32] <- of3*(C3[1] + C7[1] + C8[1]) + (d7 + k7)*MAPKMEKpp[1] + (d9 + k9)*MAPKpMEKpp[1] + Di*(MEKpp[0] - MEKpp[1]) - a7*MAPK[1]*MEKpp[1] - a9*MAPKp[1]*MEKpp[1] - a6*MEKpp[1]*(MEKPhtot - MEKpMEKPh[1] - MEKppMEKPh[1]) + d6*MEKppMEKPh[1] + k5*MEKpRAFp[1];
    dydt[33] <- a6*MEKpp[1]*(MEKPhtot - MEKpMEKPh[1] - MEKppMEKPh[1]) + Di*(MEKppMEKPh[0] - MEKppMEKPh[1]) - (d6 + k6)*MEKppMEKPh[1];
    dydt[34] <- of2*(C4[1] + C6[1] + C7[1]) + Di*(MAPK[0] - MAPK[1]) - on2*(C1[1] + C2[1] + C3[1])*MAPK[1] + d7*MAPKMEKpp[1] + k8*MAPKpMAPKPh[1] - a7*MAPK[1]*MEKpp[1];
    dydt[35] <- Di*(MAPKMEKpp[0] - MAPKMEKpp[1]) + (-d7 - k7)*MAPKMEKpp[1] + a7*MAPK[1]*MEKpp[1];
    dydt[36] <- k7*MAPKMEKpp[1] + Di*(MAPKp[0] - MAPKp[1]) + d8*MAPKpMAPKPh[1] + d9*MAPKpMEKpp[1] - a8*MAPKp[1]*(MAPKPhtot - MAPKpMAPKPh[1] - MAPKppMAPKPh[1]) + k10*MAPKppMAPKPh[1] - a9*MAPKp[1]*MEKpp[1];
    dydt[37] <- Di*(MAPKpMEKpp[0] - MAPKpMEKpp[1]) + (-d9 - k9)*MAPKpMEKpp[1] + a9*MAPKp[1]*MEKpp[1];
    dydt[38] <- of4*(C5[1] + C8[1] + C9[1]) + k9*MAPKpMEKpp[1] + Di*(MAPKpp[0] - MAPKpp[1]) - a10*MAPKpp[1]*(MAPKPhtot - MAPKpMAPKPh[1] - MAPKppMAPKPh[1]) + d10*MAPKppMAPKPh[1];
    dydt[39] <- Di*(MAPKpMAPKPh[0] - MAPKpMAPKPh[1]) + (-d8 - k8)*MAPKpMAPKPh[1] + a8*MAPKp[1]*(MAPKPhtot - MAPKpMAPKPh[1] - MAPKppMAPKPh[1]);
    dydt[40] <- a10*MAPKpp[1]*(MAPKPhtot - MAPKpMAPKPh[1] - MAPKppMAPKPh[1]) + Di*(MAPKppMAPKPh[0]- MAPKppMAPKPh[1]) - (d10 + k10)*MAPKppMAPKPh[1];
    dydt[41] <- of1*C2[1] + of3*C3[1] + of2*C4[1] + of4*C5[1] - C1[1]*(on2*MAPK[1] + on1*MEK[1]) - C1[1]*p4[1] + p3[1]*Smem[1];
    dydt[42] <- -(k5*RAFp*C2[1]) + of2*C6[1] + of4*C9[1] - C2[1]*(of1 + on2*MAPK[1]) + on1*C1[1]*MEK[1];
    dydt[43] <- k5*RAFp*C2[1] - of3*C3[1] + of2*C7[1] + of4*C8[1] - on2*C3[1]*MAPK[1];
    dydt[44] <- of1*C6[1] + of3*C7[1] + on2*C1[1]*MAPK[1] - C4[1]*(of2 + on1*MEK[1]);
    dydt[45] <- of3*C8[1] + of1*C9[1] - C5[1]*(of4 + on1*MEK[1]);
    dydt[46] <- (-of1 - of2)*C6[1] - k5*RAFp*C6[1] + on2*C2[1]*MAPK[1] + on1*C4[1]*MEK[1];
    dydt[47] <- k5*RAFp*C6[1] - k9*C7[1] - of2*C7[1] - of3*C7[1] + on2*C3[1]*MAPK[1];
    dydt[48] <- k9*C7[1] - (of3 + of4)*C8[1] + k5*RAFp*C9[1];
    dydt[49] <- (-of1 - of4)*C9[1] - k5*RAFp*C9[1] + on1*C5[1]*MEK[1];
    dydt[50] <- p1[1]*Scyto[1] - p2*Smem[1] - p3[1]*Smem[1];
    //}}}

    return dydt;
  }
} # }}}
data {/*{{{*/
  int<lower=1> T;// 
  real y0[50];    // initial state
  real t0;       // initial time
  real ts[T];    // observation times
  real theta[2]; // System parameter
  real noise;    // Observation noise
}/*}}}*/
transformed data {/*{{{*/
  real x_r[0];
  int x_i[0];
}/*}}}*/
parameters {/*{{{*/
  
}
model {

}/*}}}*/
generated quantities { # {{{
  real y_hat[T,50];
  y_hat <- integrate_ode(barr_model, y0, t0, ts, theta, x_r, x_i );

  // add measurement error
  for (t in 1:T) {
    y_hat[t,1] <- y_hat[t,1] + normal_rng(0,noise);
    y_hat[t,2] <- y_hat[t,2] + normal_rng(0,noise);
  }
}
