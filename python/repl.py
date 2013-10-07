import BetaArrestin as ba
import numpy as np

p = [ {'Stot' : s} for s in np.arange(0, 2, 0.01) ]
sim = ba.runsim( p )

