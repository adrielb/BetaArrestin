functions { # {{{
  matrix CovY( vector x, real rho_sq, real eta_sq, real sigma_sq ) {
    int N;
    N <- num_elements( x );
    {
      matrix[N,N] Sigma;
      for (i in 1:N)
        for (j in 1:N)
          Sigma[i,j] <- exp( -0.5 * rho_sq * pow( x[i] - x[j], 2)) * eta_sq;
      for (i in 1:N) {
        Sigma[i,i] <- Sigma[i,i] + sigma_sq;
      }
      return Sigma;
    }
  }
  matrix CovWY( vector w, vector x, real rho_sq, real eta_sq ) {
    int Nw;
    int Nx;
    Nw <- num_elements( w );
    Nx <- num_elements( x );
    {
      matrix[Nw,Nx] Sigma;
      for (m in 1:Nw)
        for (n in 1:Nx)
          Sigma[m,n] <- exp( -0.5 * rho_sq * pow( w[m] - x[n], 2)) * eta_sq * (w[m] - x[n]) * -rho_sq;
      return Sigma;
    }
  }
  matrix CovW( vector w, real rho_sq, real eta_sq, real sigma_sq ) {
    real norm;
    int N;
    N <- num_elements( w );
    {
      matrix[N,N] Sigma;
      for (i in 1:N)
        for (j in 1:N) {
          norm <- pow(w[i] - w[j], 2);
          Sigma[i,j] <- exp( -0.5 * rho_sq * norm) * eta_sq * (1 - rho_sq * norm) * rho_sq;
        }
      for (i in 1:N) {
        Sigma[i,i] <- Sigma[i,i] + sigma_sq;
      }
      return Sigma;
    }
  }
  matrix CovWW( vector w1, vector w2, real rho_sq, real eta_sq ) {
    int N1;
    int N2;
    N1 <- num_elements( w1 );
    N2 <- num_elements( w2 );
    {
      matrix[N1,N2] Sigma;
      real norm;
      for (i in 1:N1)
        for (j in 1:N2) {
          norm <- pow(w1[i] - w2[j], 2);
          Sigma[i,j] <- exp( -0.5 * rho_sq * norm) * eta_sq * (1 - rho_sq * norm) * rho_sq;
        }
      return Sigma;
    }
  }
} # }}}

data { #{{{
  int<lower=0> N;
  vector[N] l;
  vector[N] MI_obs;

  real<lower=0> sigma;
  real<lower=0> eta_sq;
  real<lower=0> rho_sq_l;
  real<lower=0> rho_sq_s;
  real<lower=0> sig_sq;
} #}}}

transformed data { #{{{
  matrix[N*2,N*2] L; // [w1, y1]
  vector[N] zero;
  int N2;
  N2 <- N*2;

  zero <- rep_vector( 0, N);

  {
    matrix[N2,N2] Sigma_l;  // [w1]
    matrix[N,N] Kww; // kw  [w1, w1]
    matrix[N,N] Kwy; // kwy [w1,y1]
    matrix[N,N] Kyy; // ky  [y1,y1]

    Kww <- CovW( l, rho_sq_l, eta_sq, sig_sq );
    Kwy <- CovWY( l, l, rho_sq_l, eta_sq);
    Kyy <- CovY( l, rho_sq_l, eta_sq, sig_sq );

    Sigma_l <- append_row( 
      append_col( Kww , Kwy ),
      append_col( Kwy', Kyy));

    L <- cholesky_decompose(Sigma_l);
  }
} #}}}

parameters { #{{{
  vector[N2] z_Sves;
  vector[N] dMAPKpp_dSves;
} #}}}

transformed parameters { #{{{
  vector[N2] SvesVec;
  vector[N] dSves_dl;
  vector[N] Sves_l;
  vector[N] MI_l;
  matrix[N,N] Sigma_Sves;

  SvesVec <- (L * z_Sves);
  dSves_dl <- head(SvesVec, N);
  Sves_l <- tail(SvesVec, N);
  Sigma_Sves <- CovW( Sves_l, rho_sq_s, eta_sq, sig_sq );
  MI_l <- dMAPKpp_dSves .* dSves_dl;
} #}}}

model { #{{{
  z_Sves ~ normal( 0, 1 );
  dMAPKpp_dSves ~ multi_normal( zero, Sigma_Sves );
  MI_obs ~ normal( MI_l, sigma );
} #}}}

generated quantities { #{{{
  vector[N] MAPKpp;
  {
    matrix[N,N] K;
    matrix[N,N] Kt_divSigma;
    matrix[N,N] Omega;
    matrix[N,N] Tau;

    K <- CovWY( Sves_l, Sves_l, rho_sq_s, eta_sq);
    Omega <- CovY( Sves_l, rho_sq_s, eta_sq, sig_sq);

    Kt_divSigma <- K' / Sigma_Sves;
    Tau <- Omega - Kt_divSigma * K;
    MAPKpp <- multi_normal_rng( Kt_divSigma * dMAPKpp_dSves, Tau );
  }
} #}}}
