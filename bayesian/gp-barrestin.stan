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
  int<lower=0> N;
  row_vector[N] l;
  real<lower=0> dl;
  vector[N] MI_obs;
  int Sexp[N];   // Expression level: 1 - native, 2 - overexpressed

  int<lower=0> N1;
  vector[N1] SvesX;

  real<lower=0> sigma;
  real<lower=0> rho;
} #}}}

transformed data { #{{{
  matrix[N1,N1] Sigma;
  matrix[N*2,N*2] L;
  matrix[N*2,N1] K_transpose_div_Sigma;
  vector[N*2] l2;
  vector[2] x;
  int N2;
  N2 <- 2*N;

  for (i in 1:N) {
    l2[i] <- l[i];
    l2[i+N] <- l[i] + dl;
  }
  
  {
    matrix[N2,N2] Omega;
    matrix[N1,N2] K;
    
    matrix[N2,N2] Tau;

    for (i in 1:N1)
      for (j in 1:N1)
        Sigma[i,j] <- exp(-rho*pow(SvesX[i] - SvesX[j],2));
    for (i in 1:N2)
      for (j in 1:N2)
        Omega[i,j] <- exp(-rho*pow(l2[i] - l2[j],2));
    for (i in 1:N1)
      for (j in 1:N2)
        K[i,j] <- exp(-rho*pow(SvesX[i] - l2[j],2));
    K_transpose_div_Sigma <- K' / Sigma;
    Tau <- Omega - K_transpose_div_Sigma * K;
    for (i in 1:N2)
      for (j in (i+1):N2)
        Tau[i,j] <- Tau[j,i];

    L <- cholesky_decompose(Tau);
  }
} #}}}

parameters { #{{{
  vector[N2] z;
  vector<lower=0, upper=2>[N1] SvesY;
  real<lower=1e-3,upper=1e3> dX;
} #}}}

transformed parameters { #{{{
  vector[N2] mu;
  vector[N2] SvesVec;
  matrix[2,N] Sves;
  row_vector[N] MI;
  matrix[2,N] MAPKpp;

  SvesY <- 

  mu <- K_transpose_div_Sigma * SvesY;
  SvesVec   <- mu + L * z;
  Sves[1]   <- to_row_vector(head( SvesVec, N ));
  Sves[2]   <- to_row_vector(tail( SvesVec, N ));
  MAPKpp[1] <- biphasicMAPKpp( Sves[1] );
  MAPKpp[2] <- biphasicMAPKpp( Sves[2] );
  MI        <- (MAPKpp[2] - MAPKpp[1]) / (dX);
} #}}}

model { #{{{
  z ~ normal( 0, 1 );
  dX ~ normal( 0, 1e-1 );
  MI_obs ~ normal( MI, sigma );
} #}}}

generated quantities { #{{{

} #}}}
