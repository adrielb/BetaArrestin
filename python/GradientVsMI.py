from BetaArrestin import *
from FigDisplay import *

simGrad = pd.read_csv( 'GradientVsMI.csv' )

simGrad = simGrad.set_index( ['slevel','grad'] )

#displayfig()

fig, ax = genfig()
ax.clear()
ax.set_xlim(auto=True)
ax.set_ylim(auto=True)
ax.set_title("Gradient repsonse, avg across dose")
fig.add_axes( simGrad['MI']['StotNative'].plot( label='Native' ) )
fig.add_axes( simGrad['MI']['StotOpt'].plot( label='Optimal' ) )
ax.set_xlabel("Gradient")
ax.set_ylabel("MI")
ax.legend()
showfig()
fig.savefig( "GradientVsMI.pdf", transparent=True )
