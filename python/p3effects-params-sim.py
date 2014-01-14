from BetaArrestin import *

Smem = np.arange( 0, 3, 0.01)

def p3_eval( params ):
    p = DEFAULT_PARAMS.copy()
    p.update( params )
    p3a  = p['p3a']
    p3b  = p['p3b']
    p3c  = p['p3c']
    p3d  = p['p3d']
    p3e  = p['p3e']
    p3   = p3_func( Smem, p3a, p3b, p3c, p3d, p3e )
    return p3

p3_bell = { 'name' : 'Bell' }
p3_const = {'name' : 'Constant',
            'p3a'  : 0.3,
            'p3b'  : 0,
            'p3d'  : 1 }
p3_rise = { 'name' : 'Rising',
            'p3d'  : 1}
p3_fall = { 'name' : 'Falling',
            'p3a'  : 0.5,
            'p3b'  : 0.0,
            'p3e'  : 2.0}

p3s = [p3_bell, p3_const, p3_rise, p3_fall ]

p3funcs = pd.DataFrame( index = Smem )
p3funcs.index.name = 'Smem'
for p in p3s:
    p3funcs[p['name']] = p3_eval( p )
p3funcs.to_csv('p3effects-params.csv' )

import pickle
with open( 'p3effects-params.pickle', 'w' ) as f:
    pickle.dump( p3s, f )

