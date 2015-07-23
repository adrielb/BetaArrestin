// Predict from Gaussian Process w. analytic posterior
data {
  int<lower=1> N1;
  vector[N1] x1;
  int<lower=1> N2;
  vector[N2] x2;
  
  real<lower=0> rho;
}
transformed data {
  vector[N2] mu;
  matrix[N1,N1] L1;
  matrix[N2,N2] L2;
  matrix[N1,N1] Sigma;
  matrix[N1,N2] K;
  matrix[N2,N1] K_transpose_div_Sigma;
  {
    matrix[N2,N2] Omega;
    
    matrix[N2,N2] Tau;

    for (i in 1:N1)
      for (j in 1:N1)
        Sigma[i,j] <- exp(-rho*pow(x1[i] - x1[j],2));
    for (i in 1:N2)
      for (j in 1:N2)
        Omega[i,j] <- exp(-rho*pow(x2[i] - x2[j],2));
    for (i in 1:N1)
      for (j in 1:N2)
        K[i,j] <- exp(-rho*pow(x1[i] - x2[j],2));

    K_transpose_div_Sigma <- K' / Sigma;
    // Tau <- Omega - K_transpose_div_Sigma * K;
    Tau <- Omega - K' * (Sigma \ K);
    for (i in 1:N2)
      for (j in (i+1):N2)
        Tau[i,j] <- Tau[j,i];

    L1 <- cholesky_decompose(Sigma);
    L2 <- cholesky_decompose(Tau);
  }
}
parameters {
  vector[N1] z1;
  vector[N2] z2;
}
transformed parameters {
  vector[N1] y1;
  vector[N2] y2;    // y2 ~ multi_normal(Kt.invS, Tau);
  y1 <- L1 * z1;
  y2 <- K' * (Sigma \ y1) + L2 * z2;
  // y2 <- K_transpose_div_Sigma * y1 + L2 * z2;
}
model {
  z1 ~ normal(0,1);
  z2 ~ normal(0,1);
}
generated quantities {

}
