functions { # {{{

} # }}}

data { #{{{
  int<lower=1> N;
  vector[N] x;
  vector[N] y;
} #}}}

transformed data { #{{{
  vector[N] zero;
  zero <- rep_vector( 0, N);
} #}}}

parameters { #{{{
  real<lower=0> eta_2;
  real<lower=0> rho_2;
  real<lower=0> eta_sq;
  real<lower=0> rho_sq;
  real<lower=0> sig_sq;
} #}}}

transformed parameters { #{{{
} #}}}

model { #{{{
  matrix[N,N] Sigma;
  for (i in 1:(N-1)) {
    for (j in (i+1):N) {
      Sigma[i,j] <- eta_sq * exp( -rho_sq * pow( x[i] - x[j], 2)) + 
                    eta_2  * exp( -rho_2  * pow( x[i] - x[j], 2));
      Sigma[j,i] <- Sigma[i,j];
    }
  }
  for (i in 1:N) {
    Sigma[i,i] <- eta_2 + eta_sq + sig_sq;
  }

  y ~ multi_normal( zero, Sigma);
  eta_2 ~ cauchy( 0, 5 );
  rho_2 ~ cauchy( 0, 0.5 );
  eta_sq ~ cauchy( 0, 5 );
  rho_sq ~ cauchy( 0, 5 );
  sig_sq ~ cauchy( 0, 5 );
} #}}}

generated quantities { #{{{

} #}}}
