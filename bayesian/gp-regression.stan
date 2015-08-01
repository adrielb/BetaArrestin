functions { # {{{

} # }}}

data { #{{{
  int<lower=1> N;
  vector[N] x;
  real<lower=0> eta_sq;
  real<lower=0> rho_sq;
  real<lower=0> sig_sq;
  real<lower=0> k1;
  real          mu;
} #}}}

transformed data { #{{{
  matrix[N,N] L;
  cov_matrix[N] Sigma;
  for (i in 1:(N-1)) {
    for (j in (i+1):N) {
      Sigma[i,j] <- k1 * eta_sq * exp( -rho_sq * pow( x[i] - x[j], 2));
      Sigma[j,i] <- Sigma[i,j];
    }
  }
  for (i in 1:N) {
    Sigma[i,i] <- k1 * eta_sq + sig_sq;
  }
  L <- cholesky_decompose(Sigma);
} #}}}

parameters { #{{{
  vector[N] z;
} #}}}

transformed parameters { #{{{
} #}}}

model { #{{{
  z ~ normal( 0, 1 );
} #}}}

generated quantities { #{{{
  vector[N] y;
  y <- mu + (L * z) / sqrt(k1);
} #}}}
