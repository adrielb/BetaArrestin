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
  matrix SvesCov( vector l, real rho_sq, real eta_sq, real sig_sq ) {
    int N;
    N <- num_elements( l );
    {
      matrix[N*2,N*2] L; // [w1, y1]
      matrix[N*2,N*2] Sigma_l;  // [w1]
      matrix[N,N] Kww; // kw  [w1, w1]
      matrix[N,N] Kwy; // kwy [w1,y1]
      matrix[N,N] Kyy; // ky  [y1,y1]

      Kww <- CovW( l, rho_sq, eta_sq, sig_sq );
      Kwy <- CovWY( l, l, rho_sq, eta_sq);
      Kyy <- CovY( l, rho_sq, eta_sq, sig_sq );

      Sigma_l <- append_row( 
        append_col( Kww , Kwy ),
        append_col( Kwy', Kyy));

      L <- cholesky_decompose(Sigma_l);
      return L;
    }
  }
} # }}}

data { #{{{
  int<lower=0> N[2];
  vector[N[1]] l_Native;
  vector[N[2]] l_OE;
  vector[N[1]+N[2]] MI_obs;

  real<lower=0> sigma;
  real<lower=0> eta_sq;
  real<lower=0> rho_sq_l;
  real<lower=0> rho_sq_s;
  real<lower=0> sig_sq;
  real<lower=0> OE_diff;
  real<lower=0> OE_sig;
} #}}}

transformed data { #{{{
  matrix[N[1]*2,N[1]*2] L_Native; // [w1, y1]
  matrix[N[2]*2,N[2]*2] L_OE; // [w1, y1]
  vector[N[1]+N[2]] zero;
  int N_both;
  N_both <- N[1]+N[2];

  zero <- rep_vector( 0, N_both);

  L_Native <- SvesCov( l_Native, rho_sq_l, eta_sq, sig_sq );
  L_OE <- SvesCov( l_OE, rho_sq_l, eta_sq, sig_sq );
} #}}}

parameters { #{{{
  vector[2*N[1]] z_Sves_Native;
  vector[2*N[2]] z_Sves_OE;
  vector[N[1]+N[2]] dMAPKpp_dSves; // [w_N, w_OE]
} #}}}

transformed parameters { #{{{
  vector[2*N[1]] SvesVec_Native;// [w_N , y_N]
  vector[2*N[2]] SvesVec_OE;    // [w_OE, y_OE]
  vector[N[1]] dSves_dl_Native; // [w_N]
  vector[N[2]] dSves_dl_OE;     // [w_OE]
  vector[N_both] dSves_dl;      // [w_N, w_OE]
  vector[N_both] MI;   // [w_N * w_N, w_OE * w_OE]
  vector[N[1]] Sves_l_Native; // [y_N]
  vector[N[2]] Sves_l_OE;     // [y_OE]
  vector[N[1]] dMAPKpp_dSves_Native; // [w_N]
  vector[N[2]] dMAPKpp_dSves_OE;     // [w_OE]
  vector[N_both] Sves_l;      // [y_N, y_OE]
  matrix[N_both,N_both] Sigma_Sves;
  real Sves_diff;

  SvesVec_Native <- (L_Native * z_Sves_Native);
  dSves_dl_Native <- head(SvesVec_Native, N[1]);
  Sves_l_Native   <- tail(SvesVec_Native, N[1]);
  SvesVec_OE     <- (L_OE * z_Sves_OE);
  dSves_dl_OE     <- head(SvesVec_OE, N[2]);
  Sves_l_OE       <- tail(SvesVec_OE, N[2]);
  dMAPKpp_dSves_Native <- head(dMAPKpp_dSves,N[1]);
  dMAPKpp_dSves_OE     <- tail(dMAPKpp_dSves,N[2]);
  for (i in 1:N[1]) { 
    Sves_l[i] <- Sves_l_Native[i];
    dSves_dl[i] <- dSves_dl_Native[i];
  }
  for (i in 1:N[2]) { 
    Sves_l[i+N[1]] <- Sves_l_OE[i];
    dSves_dl[i+N[1]] <- dSves_dl_OE[i];
  }
  Sigma_Sves <- CovW( Sves_l, rho_sq_s, eta_sq, sig_sq );
  MI <- dMAPKpp_dSves .* dSves_dl;
  Sves_diff <- mean( Sves_l_OE ) - mean( Sves_l_Native );
} #}}}

model { #{{{
  z_Sves_Native ~ normal( 0, 1 );
  z_Sves_OE ~ normal( 0, 1 );
  dMAPKpp_dSves ~ multi_normal( zero, Sigma_Sves ); // [w_N, w_OE]
  MI_obs ~ normal( MI, sigma );
  Sves_diff ~ normal(OE_diff, OE_sig);
} #}}}

generated quantities { #{{{
  vector[N_both] MAPKpp;
  {
    matrix[N_both,N_both] K;
    matrix[N_both,N_both] Kt_divSigma;
    matrix[N_both,N_both] Omega;
    matrix[N_both,N_both] Tau;

    K <- CovWY( Sves_l, Sves_l, rho_sq_s, eta_sq);
    Omega <- CovY( Sves_l, rho_sq_s, eta_sq, sig_sq);

    Kt_divSigma <- K' / Sigma_Sves;
    Tau <- Omega - Kt_divSigma * K;
    MAPKpp <- multi_normal_rng( Kt_divSigma * dMAPKpp_dSves, Tau );
  }
} #}}}
