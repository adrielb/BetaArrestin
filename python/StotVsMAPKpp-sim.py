from BetaArrestin import *

Stot = np.arange(0, 2, 0.01)
p = [ { 'StotOpt' : s,
        'slevel' : 'StotOpt',
        'p2'  : 0,
        'p4a' : 0,
        'p4b' : 0,
        'p3a' : 10,
        'p3b' : 0,
        'p3d' : 1 } for s in Stot ]
sim = runsim( p )

sim = sim.set_index( 'Stot' )

mapkpp = sim['MAPKpp']

mapkpp.to_csv( 'StotVsMAPKpp.csv', header=True )
