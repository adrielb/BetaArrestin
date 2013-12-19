from BetaArrestin import *

# MI vs Scaffold {{{
sim = scaffold_response( )

sim.to_csv( '/tmp/scaffold_response.csv', index=False )

sim = pd.read_csv( '/tmp/scaffold_response.csv' )
sim = sim[sim['MAPKpp'] < 1]

simStot = sim.groupby( 'Stot' ).mean()
simStot['MAPKpp_Norm'] = simStot['MAPKpp'] / simStot['MAPKpp'].max()
simStot['MI_Norm']     = simStot['MI']     / simStot['MI'].max()
simStot.index = simStot.index / simStot['StotNative']

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
# }}}

