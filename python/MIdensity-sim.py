from BetaArrestin import *
from scipy.stats import gaussian_kde

sim = pd.read_csv('InputVsMAPKpp.csv')
sim = sim[sim['Input'] > 0.5]
sim = sim.set_index( ['Input'] )

sim = sim.pivot( sim.index, 'slevel' )

mi = np.linspace(-4,6,200)

def computeKDE( name ):
    density = gaussian_kde( sim['MI'][name], bw_method=3e-1 )
    kde[name] = density( mi )


kde = pd.DataFrame( index = mi )
kde.index.name = 'MI'
computeKDE( 'StotNative' )
computeKDE( 'StotOE' )
kde.to_csv('MIdensity.csv')
