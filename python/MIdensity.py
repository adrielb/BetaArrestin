from BetaArrestin import *
from FigDisplay import *

kde = pd.read_csv('MIdensity.csv')


colorN = 'blue'
colorO = 'red'

fig, ax = genfig()
fig.set_size_inches( 5,6 )
ax.plot( kde['StotNative'] , kde['MI'] , color=colorN , label='Native' )
ax.plot( kde['StotOE']     , kde['MI'] , color=colorO , label='Overexpressed' )
ax.set_xlabel('freq')
ax.set_ylabel('MI')
ax.legend(loc='lower right')
showfig()

fig.savefig( "MIdensity.pdf", transparent=True )

