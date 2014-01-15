from BetaArrestin import *
from FigDisplay import *

#displayfig()

sim = pd.read_csv( 'StotVsMAPKpp.csv' )

fig, ax = genfig()
ax.set_title("Open loop scaffold response")
ax.set_xlabel("Stot")
ax.set_ylabel("MAPKpp")
ax.set_xlim(auto=True)
ax.set_ylim(0,1.01)
ax.plot( sim['Stot'], sim['MAPKpp'])
fig.savefig( "StotVsMAPKpp.pdf", transparent=True )

showfig(True)
