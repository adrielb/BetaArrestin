(* Created by Wolfram Mathematica 9.0 for Students - Personal Use Only : www.wolfram.com *)
{Derivative[1][Scyto[0]][t] == p4[0]*C1[0][t] - p1[0]*Scyto[0][t] + 
   Di*(-Scyto[0][t] + Scyto[1][t]) + p2*Smem[0][t], 
 Derivative[1][MEK[0]][t] == of1*(C2[0][t] + C6[0][t] + C9[0][t]) - 
   a3*RAFp*MEK[0][t] - on1*(C1[0][t] + C4[0][t] + C5[0][t])*MEK[0][t] + 
   Di*(-MEK[0][t] + MEK[1][t]) + k4*MEKpMEKPh[0][t] + d3*MEKRAFp[0][t], 
 Derivative[1][MEKRAFp[0]][t] == a3*RAFp*MEK[0][t] + 
   (-d3 - k3)*MEKRAFp[0][t] + Di*(-MEKRAFp[0][t] + MEKRAFp[1][t]), 
 Derivative[1][MEKp[0]][t] == -(a5*RAFp*MEKp[0][t]) + 
   Di*(-MEKp[0][t] + MEKp[1][t]) + d4*MEKpMEKPh[0][t] - 
   a4*MEKp[0][t]*(MEKPhtot - MEKpMEKPh[0][t] - MEKppMEKPh[0][t]) + 
   k6*MEKppMEKPh[0][t] + d5*MEKpRAFp[0][t] + k3*MEKRAFp[0][t], 
 Derivative[1][MEKpMEKPh[0]][t] == (-d4 - k4)*MEKpMEKPh[0][t] + 
   Di*(-MEKpMEKPh[0][t] + MEKpMEKPh[1][t]) + 
   a4*MEKp[0][t]*(MEKPhtot - MEKpMEKPh[0][t] - MEKppMEKPh[0][t]), 
 Derivative[1][MEKpRAFp[0]][t] == a5*RAFp*MEKp[0][t] + 
   (-d5 - k5)*MEKpRAFp[0][t] + Di*(-MEKpRAFp[0][t] + MEKpRAFp[1][t]), 
 Derivative[1][MEKpp[0]][t] == of3*(C3[0][t] + C7[0][t] + C8[0][t]) + 
   (d7 + k7)*MAPKMEKpp[0][t] + (d9 + k9)*MAPKpMEKpp[0][t] - 
   a7*MAPK[0][t]*MEKpp[0][t] - a9*MAPKp[0][t]*MEKpp[0][t] + 
   Di*(-MEKpp[0][t] + MEKpp[1][t]) - a6*MEKpp[0][t]*
    (MEKPhtot - MEKpMEKPh[0][t] - MEKppMEKPh[0][t]) + d6*MEKppMEKPh[0][t] + 
   k5*MEKpRAFp[0][t], Derivative[1][MEKppMEKPh[0]][t] == 
  a6*MEKpp[0][t]*(MEKPhtot - MEKpMEKPh[0][t] - MEKppMEKPh[0][t]) - 
   (d6 + k6)*MEKppMEKPh[0][t] + Di*(-MEKppMEKPh[0][t] + MEKppMEKPh[1][t]), 
 Derivative[1][MAPK[0]][t] == of2*(C4[0][t] + C6[0][t] + C7[0][t]) - 
   on2*(C1[0][t] + C2[0][t] + C3[0][t])*MAPK[0][t] + 
   Di*(-MAPK[0][t] + MAPK[1][t]) + d7*MAPKMEKpp[0][t] + 
   k8*MAPKpMAPKPh[0][t] - a7*MAPK[0][t]*MEKpp[0][t], 
 Derivative[1][MAPKMEKpp[0]][t] == (-d7 - k7)*MAPKMEKpp[0][t] + 
   Di*(-MAPKMEKpp[0][t] + MAPKMEKpp[1][t]) + a7*MAPK[0][t]*MEKpp[0][t], 
 Derivative[1][MAPKp[0]][t] == k7*MAPKMEKpp[0][t] + 
   Di*(-MAPKp[0][t] + MAPKp[1][t]) + d8*MAPKpMAPKPh[0][t] + 
   d9*MAPKpMEKpp[0][t] - a8*MAPKp[0][t]*(MAPKPhtot - MAPKpMAPKPh[0][t] - 
     MAPKppMAPKPh[0][t]) + k10*MAPKppMAPKPh[0][t] - 
   a9*MAPKp[0][t]*MEKpp[0][t], Derivative[1][MAPKpMEKpp[0]][t] == 
  (-d9 - k9)*MAPKpMEKpp[0][t] + Di*(-MAPKpMEKpp[0][t] + MAPKpMEKpp[1][t]) + 
   a9*MAPKp[0][t]*MEKpp[0][t], Derivative[1][MAPKpp[0]][t] == 
  of4*(C5[0][t] + C8[0][t] + C9[0][t]) + k9*MAPKpMEKpp[0][t] + 
   Di*(-MAPKpp[0][t] + MAPKpp[1][t]) - a10*MAPKpp[0][t]*
    (MAPKPhtot - MAPKpMAPKPh[0][t] - MAPKppMAPKPh[0][t]) + 
   d10*MAPKppMAPKPh[0][t], Derivative[1][MAPKpMAPKPh[0]][t] == 
  (-d8 - k8)*MAPKpMAPKPh[0][t] + Di*(-MAPKpMAPKPh[0][t] + 
     MAPKpMAPKPh[1][t]) + a8*MAPKp[0][t]*(MAPKPhtot - MAPKpMAPKPh[0][t] - 
     MAPKppMAPKPh[0][t]), Derivative[1][MAPKppMAPKPh[0]][t] == 
  a10*MAPKpp[0][t]*(MAPKPhtot - MAPKpMAPKPh[0][t] - MAPKppMAPKPh[0][t]) - 
   (d10 + k10)*MAPKppMAPKPh[0][t] + 
   Di*(-MAPKppMAPKPh[0][t] + MAPKppMAPKPh[1][t]), 
 Derivative[1][C1[0]][t] == -(p4[0]*C1[0][t]) + of1*C2[0][t] + of3*C3[0][t] + 
   of2*C4[0][t] + of4*C5[0][t] - C1[0][t]*(on2*MAPK[0][t] + on1*MEK[0][t]) + 
   p3[0]*Smem[0][t], Derivative[1][C2[0]][t] == 
  -(k5*RAFp*C2[0][t]) + of2*C6[0][t] + of4*C9[0][t] - 
   C2[0][t]*(of1 + on2*MAPK[0][t]) + on1*C1[0][t]*MEK[0][t], 
 Derivative[1][C3[0]][t] == k5*RAFp*C2[0][t] - of3*C3[0][t] + of2*C7[0][t] + 
   of4*C8[0][t] - on2*C3[0][t]*MAPK[0][t], Derivative[1][C4[0]][t] == 
  of1*C6[0][t] + of3*C7[0][t] + on2*C1[0][t]*MAPK[0][t] - 
   C4[0][t]*(of2 + on1*MEK[0][t]), Derivative[1][C5[0]][t] == 
  of3*C8[0][t] + of1*C9[0][t] - C5[0][t]*(of4 + on1*MEK[0][t]), 
 Derivative[1][C6[0]][t] == (-of1 - of2)*C6[0][t] - k5*RAFp*C6[0][t] + 
   on2*C2[0][t]*MAPK[0][t] + on1*C4[0][t]*MEK[0][t], 
 Derivative[1][C7[0]][t] == k5*RAFp*C6[0][t] - k9*C7[0][t] - of2*C7[0][t] - 
   of3*C7[0][t] + on2*C3[0][t]*MAPK[0][t], Derivative[1][C8[0]][t] == 
  k9*C7[0][t] - (of3 + of4)*C8[0][t] + k5*RAFp*C9[0][t], 
 Derivative[1][C9[0]][t] == (-of1 - of4)*C9[0][t] - k5*RAFp*C9[0][t] + 
   on1*C5[0][t]*MEK[0][t], Derivative[1][Smem[0]][t] == 
  p1[0]*Scyto[0][t] - p2*Smem[0][t] - p3[0]*Smem[0][t], 
 Derivative[1][Scyto[1]][t] == p4[1]*C1[1][t] + 
   Di*(Scyto[0][t] - Scyto[1][t]) - p1[1]*Scyto[1][t] + p2*Smem[1][t], 
 Derivative[1][MEK[1]][t] == of1*(C2[1][t] + C6[1][t] + C9[1][t]) + 
   Di*(MEK[0][t] - MEK[1][t]) - a3*RAFp*MEK[1][t] - 
   on1*(C1[1][t] + C4[1][t] + C5[1][t])*MEK[1][t] + k4*MEKpMEKPh[1][t] + 
   d3*MEKRAFp[1][t], Derivative[1][MEKRAFp[1]][t] == 
  a3*RAFp*MEK[1][t] + Di*(MEKRAFp[0][t] - MEKRAFp[1][t]) + 
   (-d3 - k3)*MEKRAFp[1][t], Derivative[1][MEKp[1]][t] == 
  Di*(MEKp[0][t] - MEKp[1][t]) - a5*RAFp*MEKp[1][t] + d4*MEKpMEKPh[1][t] - 
   a4*MEKp[1][t]*(MEKPhtot - MEKpMEKPh[1][t] - MEKppMEKPh[1][t]) + 
   k6*MEKppMEKPh[1][t] + d5*MEKpRAFp[1][t] + k3*MEKRAFp[1][t], 
 Derivative[1][MEKpMEKPh[1]][t] == Di*(MEKpMEKPh[0][t] - MEKpMEKPh[1][t]) + 
   (-d4 - k4)*MEKpMEKPh[1][t] + a4*MEKp[1][t]*(MEKPhtot - MEKpMEKPh[1][t] - 
     MEKppMEKPh[1][t]), Derivative[1][MEKpRAFp[1]][t] == 
  a5*RAFp*MEKp[1][t] + Di*(MEKpRAFp[0][t] - MEKpRAFp[1][t]) + 
   (-d5 - k5)*MEKpRAFp[1][t], Derivative[1][MEKpp[1]][t] == 
  of3*(C3[1][t] + C7[1][t] + C8[1][t]) + (d7 + k7)*MAPKMEKpp[1][t] + 
   (d9 + k9)*MAPKpMEKpp[1][t] + Di*(MEKpp[0][t] - MEKpp[1][t]) - 
   a7*MAPK[1][t]*MEKpp[1][t] - a9*MAPKp[1][t]*MEKpp[1][t] - 
   a6*MEKpp[1][t]*(MEKPhtot - MEKpMEKPh[1][t] - MEKppMEKPh[1][t]) + 
   d6*MEKppMEKPh[1][t] + k5*MEKpRAFp[1][t], 
 Derivative[1][MEKppMEKPh[1]][t] == 
  a6*MEKpp[1][t]*(MEKPhtot - MEKpMEKPh[1][t] - MEKppMEKPh[1][t]) + 
   Di*(MEKppMEKPh[0][t] - MEKppMEKPh[1][t]) - (d6 + k6)*MEKppMEKPh[1][t], 
 Derivative[1][MAPK[1]][t] == of2*(C4[1][t] + C6[1][t] + C7[1][t]) + 
   Di*(MAPK[0][t] - MAPK[1][t]) - on2*(C1[1][t] + C2[1][t] + C3[1][t])*
    MAPK[1][t] + d7*MAPKMEKpp[1][t] + k8*MAPKpMAPKPh[1][t] - 
   a7*MAPK[1][t]*MEKpp[1][t], Derivative[1][MAPKMEKpp[1]][t] == 
  Di*(MAPKMEKpp[0][t] - MAPKMEKpp[1][t]) + (-d7 - k7)*MAPKMEKpp[1][t] + 
   a7*MAPK[1][t]*MEKpp[1][t], Derivative[1][MAPKp[1]][t] == 
  k7*MAPKMEKpp[1][t] + Di*(MAPKp[0][t] - MAPKp[1][t]) + 
   d8*MAPKpMAPKPh[1][t] + d9*MAPKpMEKpp[1][t] - 
   a8*MAPKp[1][t]*(MAPKPhtot - MAPKpMAPKPh[1][t] - MAPKppMAPKPh[1][t]) + 
   k10*MAPKppMAPKPh[1][t] - a9*MAPKp[1][t]*MEKpp[1][t], 
 Derivative[1][MAPKpMEKpp[1]][t] == 
  Di*(MAPKpMEKpp[0][t] - MAPKpMEKpp[1][t]) + (-d9 - k9)*MAPKpMEKpp[1][t] + 
   a9*MAPKp[1][t]*MEKpp[1][t], Derivative[1][MAPKpp[1]][t] == 
  of4*(C5[1][t] + C8[1][t] + C9[1][t]) + k9*MAPKpMEKpp[1][t] + 
   Di*(MAPKpp[0][t] - MAPKpp[1][t]) - a10*MAPKpp[1][t]*
    (MAPKPhtot - MAPKpMAPKPh[1][t] - MAPKppMAPKPh[1][t]) + 
   d10*MAPKppMAPKPh[1][t], Derivative[1][MAPKpMAPKPh[1]][t] == 
  Di*(MAPKpMAPKPh[0][t] - MAPKpMAPKPh[1][t]) + (-d8 - k8)*MAPKpMAPKPh[1][t] + 
   a8*MAPKp[1][t]*(MAPKPhtot - MAPKpMAPKPh[1][t] - MAPKppMAPKPh[1][t]), 
 Derivative[1][MAPKppMAPKPh[1]][t] == 
  a10*MAPKpp[1][t]*(MAPKPhtot - MAPKpMAPKPh[1][t] - MAPKppMAPKPh[1][t]) + 
   Di*(MAPKppMAPKPh[0][t] - MAPKppMAPKPh[1][t]) - 
   (d10 + k10)*MAPKppMAPKPh[1][t], Derivative[1][C1[1]][t] == 
  -(p4[1]*C1[1][t]) + of1*C2[1][t] + of3*C3[1][t] + of2*C4[1][t] + 
   of4*C5[1][t] - C1[1][t]*(on2*MAPK[1][t] + on1*MEK[1][t]) + 
   p3[1]*Smem[1][t], Derivative[1][C2[1]][t] == 
  -(k5*RAFp*C2[1][t]) + of2*C6[1][t] + of4*C9[1][t] - 
   C2[1][t]*(of1 + on2*MAPK[1][t]) + on1*C1[1][t]*MEK[1][t], 
 Derivative[1][C3[1]][t] == k5*RAFp*C2[1][t] - of3*C3[1][t] + of2*C7[1][t] + 
   of4*C8[1][t] - on2*C3[1][t]*MAPK[1][t], Derivative[1][C4[1]][t] == 
  of1*C6[1][t] + of3*C7[1][t] + on2*C1[1][t]*MAPK[1][t] - 
   C4[1][t]*(of2 + on1*MEK[1][t]), Derivative[1][C5[1]][t] == 
  of3*C8[1][t] + of1*C9[1][t] - C5[1][t]*(of4 + on1*MEK[1][t]), 
 Derivative[1][C6[1]][t] == (-of1 - of2)*C6[1][t] - k5*RAFp*C6[1][t] + 
   on2*C2[1][t]*MAPK[1][t] + on1*C4[1][t]*MEK[1][t], 
 Derivative[1][C7[1]][t] == k5*RAFp*C6[1][t] - k9*C7[1][t] - of2*C7[1][t] - 
   of3*C7[1][t] + on2*C3[1][t]*MAPK[1][t], Derivative[1][C8[1]][t] == 
  k9*C7[1][t] - (of3 + of4)*C8[1][t] + k5*RAFp*C9[1][t], 
 Derivative[1][C9[1]][t] == (-of1 - of4)*C9[1][t] - k5*RAFp*C9[1][t] + 
   on1*C5[1][t]*MEK[1][t], Derivative[1][Smem[1]][t] == 
  p1[1]*Scyto[1][t] - p2*Smem[1][t] - p3[1]*Smem[1][t]}
