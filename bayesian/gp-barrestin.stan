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

  real          SvesMu;
  real<lower=0> sigma;
  real<lower=0> eta_sq;
  real<lower=0> rho_sq;
  real<lower=0> sig_sq;
  real<lower=0> dXmin;
  real<lower=0> dXmax;
  real<lower=0> k1;
} #}}}

transformed data { #{{{
  cov_matrix[N*2] Sigma;
  matrix[N*2,N*2] L;
  vector[N*2] l2;
  int N2;
  N2 <- N*2;

  for (i in 1:N) {
    l2[i] <- l[i];
    l2[i+N] <- l[i] + dl;
  }

  for (i in 1:(N2-1)) {
    for (j in (i+1):N2) {
      Sigma[i,j] <- k1 * eta_sq * exp( -rho_sq * pow( l2[i] - l2[j], 2));
      Sigma[j,i] <- Sigma[i,j];
    }
  }
  for (i in 1:N2) {
    Sigma[i,i] <- k1 * eta_sq + sig_sq;
  }
  L <- cholesky_decompose(Sigma);
  
} #}}}

parameters { #{{{
  vector[N2] z;
  real<lower=dXmin,upper=dXmax> dX;
} #}}}

transformed parameters { #{{{
  vector[N2] SvesVec;
  matrix[2,N] Sves;
  row_vector[N] MI;
  matrix[2,N] MAPKpp;

  SvesVec   <- SvesMu + (L * z) / sqrt(k1);
  for (i in 1:N2) {
    SvesVec[i] <- pow( 10, SvesVec[i] );
  }
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
