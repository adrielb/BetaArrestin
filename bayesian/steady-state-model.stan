functions { # {{{
  row_vector biphasicMAPKpp( row_vector Sves ) {
    real a;
    real b;
    real c;
    real d;
    real g;
    a <- 6.06;
    b <- 1.02e3;
    c <- -4.54;
    d <- 5.;
    g <- 1.65e-1;
    return g + (a + b*Sves)./(1 + exp(-c + d*Sves));
  }
} # }}}

data { #{{{
  real Di;
  real grad;
  real maxdose;
  real dX;
  real eps;

  int<lower=0> N; 
  row_vector[N] l;
  vector[N] MI_obs;
  int Sexp[N];   // Expression level: 1 - native, 2 - overexpressed

  vector<lower=0>[2] Stot;
  real<lower=0> p2;
  vector<lower=0>[2] p3;
  real<lower=0> p4;
  real<lower=0> p5;
  real<lower=0> sigma;
} #}}}

transformed data { #{{{
  vector[2] x;
  real zero[N];  
  zero <- rep_array(0.0, N);
  x[1] <- 0;
  x[2] <- 1;
} #}}}

parameters { #{{{
  simplex[6] S[N]; // Stot = [Sves + Smem + Scyto] x [front, back]
} #}}}

transformed parameters { #{{{
  row_vector[N] MI;
  matrix[2,N] Sves;
  matrix[2,N] Scyto;
  matrix[2,N] Smem;
  matrix[2,N] MAPKpp;
  matrix[2,N] eqScyto;
  matrix[2,N] eqSmem;
  matrix<lower=0>[2,N] p1;
  real StotExp;

  for (n in 1:N) {
    StotExp     <- Stot[Sexp[n]]; 
    Sves[1][n]  <- StotExp * S[n][1];
    Smem[1][n]  <- StotExp * S[n][2];
    Scyto[1][n] <- StotExp * S[n][3];
    Sves[2][n]  <- StotExp * S[n][4];
    Smem[2][n]  <- StotExp * S[n][5];
    Scyto[2][n] <- StotExp * S[n][6];
  }

  p1[1]      <- p5 * grad * maxdose * (l + dX * x[1]);
  p1[2]      <- p5 * grad * maxdose * (l + dX * x[2]);
  eqScyto[1] <- Di*(-Scyto[1] + Scyto[2]) - p1[1].*Scyto[1] + p2*Smem[1] + p4*Sves[1];
  eqScyto[2] <- Di*( Scyto[1] - Scyto[2]) - p1[2].*Scyto[2] + p2*Smem[2] + p4*Sves[2];
  eqSmem[1]  <- p1[1].*Scyto[1] - p2*Smem[1] - p3[1]*Smem[1];
  eqSmem[2]  <- p1[2].*Scyto[2] - p2*Smem[2] - p3[2]*Smem[2];
  MAPKpp[1]  <- biphasicMAPKpp( Sves[1] );
  MAPKpp[2]  <- biphasicMAPKpp( Sves[2] );
  MI         <- (MAPKpp[2] - MAPKpp[1]) / (grad * maxdose * dX);
} #}}}

model { #{{{
  // Stot ~ normal( 3, 3);
  zero ~ normal( eqScyto[1], eps );
  zero ~ normal( eqScyto[2], eps );
  zero ~ normal( eqSmem[1], eps );
  zero ~ normal( eqSmem[2], eps );
  // MI_obs ~ normal( MI, sigma );
} #}}}

generated quantities { #{{{

} #}}}
