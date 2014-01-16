from BetaArrestin import *
from FigDisplay import *

sim = pd.read_csv( 'SmemVsp3.csv' )

fig, ax = genfig()

ax.clear()
ax.set_xlabel("Smem")
ax.set_ylabel("p3")
ax.set_xlim(auto=True)
ax.set_ylim(0, 0.4)
ax.set_title("p3: Smem to Sves transport")
ax.plot( Smem, p3, color='lime', label="p3()" )
fig.savefig( "SmemVsp3.pdf", transparent=True )
showfig()
