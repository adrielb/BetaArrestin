runsimODE[pp___] := Block[
  {sol, p = Flatten[{pp}], ic = icODE, dtzero, tol = 10^(-8), maxiter = 30, iter}, 
  iter = Catch[
    Do[
      sol = NDSolve[Join[equODE, ic] //. p /. params, varODE, {t, 0, tend}][[1]];
      dtzero = Max[Abs[equODE[[All,2]] //. p /. t -> tend /. sol /. params]]; 
      If[dtzero < tol, Throw[i]]; 
      ic = vars /. (x_)[s_] :> x[s][0] == (x[s][tend] /. sol); 
    ,{i, maxiter}]
  ]; 
  Join[{dd -> dtzero, runsim$maxiter -> (iter /. Null -> maxiter)}, p, sol]
]
