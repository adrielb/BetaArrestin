from BetaArrestin import *

p3a = DEFAULT_PARAMS['p3a']
p3b = DEFAULT_PARAMS['p3b']
p3c = DEFAULT_PARAMS['p3c']
p3d = DEFAULT_PARAMS['p3d']
p3e = DEFAULT_PARAMS['p3e']
Smem = np.arange( 0, 3, 0.01)
p3 = p3_func( Smem, p3a, p3b, p3c, p3d, p3e )

sim = pd.DataFrame( index=Smem, data=p3, columns=['p3'] )
sim.index.name='Smem'

sim.to_csv( 'SmemVsp3.csv' )


