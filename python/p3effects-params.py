from BetaArrestin import *
from FigDisplay import *

#displayfig()

p3funcs = pd.read_csv('p3effects-params.csv', index_col=0)
Smem = p3funcs.index

fig, ax = genfig( 3 )
ax.set_xlabel("Smem")
ax.set_ylabel("p3")
ax.set_xlim(auto=True)
ax.set_ylim(0, 0.6)
ax.set_title("p3: Smem to Sves transport")
for k in p3funcs.keys():
    ax.plot( Smem, p3funcs[ k ], label=k )
ax.legend()
showfig( 3 )

fig.savefig( "p3effects-params.pdf", transparent=True )
