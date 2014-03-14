from BetaArrestin import *

sim = dose_response({'lbl' : 'Nw', 'slevel'  : 'StotNative' }).append(
      dose_response({'lbl' : 'Ow', 'slevel'  : 'StotOE' }) ).append(
      dose_response({'lbl' : 'Nz' , 'slevel' : 'StotNative' , 'p4a'    : 0 }).append(
      dose_response({'lbl' : 'Oz' , 'slevel' : 'StotOE'     , 'p4a'    : 0 }))
      )


sim = sim[ ['lbl', 'slevel', 'MAPKpp', 'MI'] ]
sim.index.name = 'Input'

sim.to_csv( 'p4effects.csv' )
