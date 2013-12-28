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

fig, ax = genfig()
ax.set_title("Open loop scaffold response")
ax.set_xlabel("Stot")
ax.set_ylabel("MAPKpp")
ax.set_xlim(auto=True)
ax.set_ylim(0,1.01)
ax.plot( sim['Stot'], sim['MAPKpp'])
fig.show()

fig.savefig( "StotVsMAPKpp.pdf", transparent=True )
