from BetaArrestin import *

sim = gradient_response( )

simGrad = sim[ ['slevel', 'grad', 'MI'] ]

simGrad = simGrad.groupby(['slevel', 'grad']).mean()

simGrad.to_csv( 'GradientVsMI.csv' )



