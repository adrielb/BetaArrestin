from BetaArrestin import *
from FigDisplay import *

displayfig()

p4a = DEFAULT_PARAMS['p4a']
p4b = DEFAULT_PARAMS['p4b']
p4m = DEFAULT_PARAMS['p4m']
p4n = DEFAULT_PARAMS['p4n']

Sves = np.arange(0, 0.5, 0.001)
Sn = p4n * Sves + p4m
Sn = np.clip( Sn, 0.1, 1e3 )
Ss = 200 / ( 1 + np.exp( -(Sves-0.35)*10 ) )

fig, ax = genfig()
ax.set_title("")
ax.set_xlabel("Sves")
ax.set_ylabel("S_")
ax.set_xlim(auto=True)
ax.set_ylim(auto=True)
ax.plot( Sves, Sn, label='Sn' )
ax.plot( Sves, Ss, label='Ss' )
ax.legend(loc='upper left')
showfig()


p4
