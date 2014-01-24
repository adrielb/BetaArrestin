from BetaArrestin import *

sim = dose_response({'slevel' : 'StotNative' }).append(
      dose_response({'slevel' : 'StotOE' }) )

sim = sim[ ['slevel', 'MAPKpp', 'MI', 'Smem[0]', 'Smem[1]', 'gdm' ] ]
sim.index.name = 'Input'

sim.to_csv( 'InputVsMAPKpp.csv' )

