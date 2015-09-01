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
  int<lower=0> Nx;
  vector[N] l;
  vector[N] MI_obs;
  vector[Nx] x2;

  real<lower=0> sigma;
  real<lower=0> eta_sq;
  real<lower=0> rho_sq;
  real<lower=0> sig_sq;
} #}}}

transformed data { #{{{
  matrix[N+Nx,N+Nx] L;
  vector[N+Nx*2]zero;
  int NNx;
  int NNx2;

  NNx <- N + Nx;
  NNx2<- N + Nx*2;

  zero <- rep_vector( 0, NNx2);

  {
    matrix[NNx,NNx] Sigma_l;  // [w1, y2]
    matrix[N,N] Kww;   // kw  [x1, x1]
    matrix[N,Nx] Kwy;  // kwy [x1, x2]
    matrix[Nx,Nx] Kyy; // ky  [x2, x2]

    Kww <- CovW( l, rho_sq, eta_sq, sig_sq );
    Kwy <- CovWY( l, x2, rho_sq, eta_sq);
    Kyy <- CovY( x2, rho_sq, eta_sq, sig_sq );

    Sigma_l <- append_row( 
      append_col( Kww , Kwy ),
      append_col( Kwy', Kyy));
    L <- cholesky_decompose(Sigma_l);
  }
} #}}}

parameters { #{{{
  vector[NNx] z_Sves;
  vector[NNx2] MAPKppVec;
} #}}}

transformed parameters { #{{{
  vector[NNx] SvesVec; // [w1, y2]
  vector[N] dSves_dl;
  vector[N] dMAPKpp_dSves;
  vector[N] MI_l;

  SvesVec <- (L * z_Sves);
  dSves_dl <- head(SvesVec, N);
  dMAPKpp_dSves <- head(MAPKppVec,N);
  MI_l <- dMAPKpp_dSves .* dSves_dl;
} #}}}

model { #{{{
  matrix[NNx2,NNx2] Sigma_Sves;
  int N1;
  int N2;
  N1 <- N;
  N2 <- Nx;
  { 
    matrix[N1,N1] Kww;     // kw(x1,x1)
    matrix[N1,N2] Ky;      // kwy(x1,x2)
    matrix[N1,N2] Kw;      // kww(x1,x2)
    matrix[N2,N2] Omega11; // kyy(x1,x1)
    matrix[N2,N2] Omega22; // kww(x2,x2)
    matrix[N2,N2] Omega12; // kwy(x2,x2)

    Kww     <- CovW(  l, rho_sq, eta_sq, sig_sq );
    Omega11 <- CovY( x2, rho_sq, eta_sq, sig_sq );
    Omega22 <- CovW( x2, rho_sq, eta_sq, sig_sq );
    Omega12 <- CovWY(x2, x2, rho_sq, eta_sq);
    Ky      <- CovWY( l, x2, rho_sq, eta_sq);
    Kw      <- CovWW( l, x2, rho_sq, eta_sq);

    Sigma_Sves <- append_row( append_row( 
        append_col( append_col( Kww,      Ky ),      Kw )
      , append_col( append_col( Ky', Omega11 ),-Omega12 ))
      , append_col( append_col( Kw',-Omega12'), Omega22 ));

  }

  z_Sves ~ normal( 0, 1 );
  MAPKppVec ~ multi_normal( zero, Sigma_Sves );
  MI_obs ~ normal( MI_l, sigma );
} #}}}

generated quantities { #{{{
  // vector[Nx] MI;
  vector[Nx] MAPKpp;
  vector[Nx] Sves;
  
  MAPKpp <- segment(MAPKppVec,N+1,Nx);
  Sves <- tail(SvesVec,Nx);

} #}}}
