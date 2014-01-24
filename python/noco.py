from BetaArrestin import *
from FigDisplay import *

mapkpp = pd.read_csv( 'noco.csv' )
mapkpp = mapkpp.set_index( ['name', 'Input'] )

displayfig()

fig, ax = genfig()

ax.plot( mapkpp.loc['ctrl'].index , mapkpp.loc['ctrl'] , color='blue', label='MAPKpp-ctrl' )
ax.plot( mapkpp.loc['noco'].index , mapkpp.loc['noco'] , color='red' , label='MAPKpp-noco' )

ax.set_title('Nocodazole treatment')
ax.set_ylabel('MAPKpp')
ax.set_xlabel('Input')
ax.legend(loc='lower right')
showfig()
fig.savefig( "noco.pdf", transparent=True )
