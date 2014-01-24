from BetaArrestin import *
from FigDisplay import *

simStot = pd.read_csv( 'ScaffoldVsMAPKppMI.csv' )

#displayfig()

fig, ax = genfig()
ax.set_xlabel("Relative Scaffold")
ax.set_ylabel("Normalized to Max")
ax.set_xlim(auto=True)
ax.set_ylim(-0.3,1.05)
ax.set_title("Scaffold repsonse, avg across dose")
ax.plot( simStot.index, simStot['MAPKpp_Norm'], color='red', label='MAPKpp' )
ax.plot( simStot.index, simStot['MI_Norm'],     color='black', label='MI' )
ax.legend()
showfig()
fig.savefig( "ScaffoldVsMAPKppMI.pdf", transparent=True )

