from BetaArrestin import *

sim = gradient_response( start=0.5 )

simGrad = sim[ ['slevel', 'grad', 'MI'] ]

simGrad = simGrad.groupby(['slevel', 'grad']).mean()

simGrad.to_csv( 'GradientVsMI.csv' )



