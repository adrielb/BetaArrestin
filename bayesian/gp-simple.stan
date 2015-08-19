functions { # {{{
  matrix GenereateCovMatrix( vector x, int N,
    real k1, real rho_sq, real eta_sq, real sig_sq ) {
    matrix[N,N] Sigma;
    for (i in 1:(N-1)) {
      for (j in (i+1):N) {
        Sigma[i,j] <- k1 * eta_sq * exp( -rho_sq * pow( x[i] - x[j], 2));
        Sigma[j,i] <- Sigma[i,j];
      }
    }
    for (i in 1:N) {
      Sigma[i,i] <- k1 * eta_sq + sig_sq;
    }
    return Sigma;
  }
} # }}}

data { #{{{
  int<lower=0> N;
  row_vector[N] l;
  real<lower=0> dl;
  vector[N] MI_obs;

  real<lower=0> sigma;
  real<lower=0> eta_sq;
  real<lower=0> rho_sq;
  real<lower=0> sig_sq;
  real<lower=0> dXmin;
  real<lower=0> dXmax;
  real<lower=0> k1;
} #}}}

transformed data { #{{{
  matrix[N*2,N*2] Sigma_l2;
  matrix[N*2,N*2] L;
  vector[N*2] l2;
  vector[N*2] zero;
  int N2;
  N2 <- N*2;

  zero <- rep_vector( 0, N2);

  for (i in 1:N) {
    l2[i] <- l[i];
    l2[i+N] <- l[i] + dl;
  }

  Sigma_l2 <- GenereateCovMatrix( l2, N2, k1, rho_sq, eta_sq, sig_sq);
  L <- cholesky_decompose(Sigma_l2);
} #}}}

parameters { #{{{
  vector[N2] z;
  vector[N2] MAPKppVec;
  real<lower=dXmin,upper=dXmax> dX;
} #}}}

transformed parameters { #{{{
  vector[N2] SvesVec;
  matrix[2,N] MAPKpp;
  row_vector[N] MI;

  SvesVec    <- zero + (L * z) / sqrt(k1);
  MAPKpp[1]  <- to_row_vector(head( MAPKppVec, N ));
  MAPKpp[2]  <- to_row_vector(tail( MAPKppVec, N ));
  MI         <- (MAPKpp[2] - MAPKpp[1]) / (dX);
} #}}}

model { #{{{
  matrix[N2,N2] Sigma_Sves;
  Sigma_Sves <- GenereateCovMatrix( SvesVec, N2, k1, rho_sq, eta_sq, sig_sq);

  dX ~ normal( 0, 1e-1 );
  z ~ normal( 0, 1 );
  MAPKppVec ~ multi_normal( zero, Sigma_Sves );
  MI_obs ~ normal( MI, sigma );
} #}}}

generated quantities { #{{{

} #}}}
