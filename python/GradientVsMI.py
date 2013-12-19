from BetaArrestin import *

# MI vs Gradient {{{
sim = gradient_response( )
simGrad = sim.groupby(['slevel', 'grad']).mean()
simGrad.to_csv( 'gradient_response.csv' )

simGrad = pd.read_csv( 'gradient_response.csv', index_col=[0,1] )


fig, ax = genfig()
ax.clear()
ax.set_xlim(auto=True)
ax.set_ylim(auto=True)
ax.set_title("Gradient repsonse, avg across dose")
fig.add_axes(
    simGrad['MI']['StotNative'].plot( label='Native' ) )
fig.add_axes(
    simGrad['MI']['StotOpt'].plot( label='Optimal' ) )
ax.set_xlabel("Gradient")
ax.set_ylabel("MI")
ax.legend()
showfig()
fig.savefig( "GradientVsMI.pdf", transparent=True )
# }}}
