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
  vector[N] MI_obs;
  int Sexp[N];   // Expression level: 1 - native, 2 - overexpressed

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
  real<upper=0> w;
  real<lower=0> b;
  real<lower=0> b2;
  real<lower=0> dX;
} #}}}

transformed parameters { #{{{
  matrix[2,N] Sves;
  row_vector[N] MI;
  matrix[2,N] MAPKpp;

  Sves[1]   <- b + w * (l);
  Sves[2]   <- b + w * (l) + b2;
  MAPKpp[1] <- biphasicMAPKpp( Sves[1] );
  MAPKpp[2] <- biphasicMAPKpp( Sves[2] );
  MI        <- (MAPKpp[2] - MAPKpp[1]) / (dX);
} #}}}

model { #{{{
  dX ~ normal( 0, 1e-1 );
  w ~ normal( 0, 1e-1 );
  b ~ normal( 0, 1e-1 );
  b2 ~ normal( 0, 1e-1 );
  MI_obs ~ normal( MI, sigma );
} #}}}

generated quantities { #{{{

} #}}}
