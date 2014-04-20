from BetaArrestin import *

sim = dose_response({'lbl' : 'model'   , 'slevel' : 'StotNative' }).append(
      dose_response({'lbl' : 'model'   , 'slevel' : 'StotOE'     })).append(
      dose_response({'lbl' : 'flat'    , 'slevel' : 'StotNative' , 'p4a' : 0 })).append(
      dose_response({'lbl' : 'flat'    , 'slevel' : 'StotOE'     , 'p4a' : 0 })).append(
      dose_response({'lbl' : 'highsig' , 'slevel' : 'StotNative' , 'p4n' : 0 , 'p4m' : 150 })).append(
      dose_response({'lbl' : 'highsig' , 'slevel' : 'StotOE'     , 'p4n' : 0 , 'p4m' : 150 })).append(
      dose_response({'lbl' : 'lowsig'  , 'slevel' : 'StotNative' , 'p4n' : 0 , 'p4m' : 0.1 })).append(
      dose_response({'lbl' : 'lowsig'  , 'slevel' : 'StotOE'     , 'p4n' : 0 , 'p4m' : 0.1 }))


sim = sim[ ['lbl', 'slevel', 'MAPKpp', 'MI', 'p4a', 'p4b', 'p4m','p4n'] ]
sim.index.name = 'Input'

sim.to_csv( 'p4effects.csv' )
