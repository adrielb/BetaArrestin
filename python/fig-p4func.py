from BetaArrestin import *

x = np.array( [0,1] )
p4a = DEFAULT_PARAMS['p4a']
p4b = DEFAULT_PARAMS['p4b']
p4n = DEFAULT_PARAMS['p4n']
p4a = 0.003
p4n = 200
w=600
dsves = np.linspace( -w, w, 100 )
p4 = np.array( [ p4_func( x, p4a, p4b, p4n, s ) for s in dsves ] )
p4 = p4.transpose()
fig, ax = genfig()
ax.plot( dsves , p4[0] , label='x = Back'  , color='black'  )
ax.plot( dsves , p4[1] , label='x = Front' , color='blue' )
ax.set_title("p4( x, dSves)")
ax.set_xlabel("dSves Level")
ax.set_ylabel("p4")
w=600
#ax.set_xlim(-w, w)
w=0.01
ax.set_ylim(p4b-p4a-w, p4b+p4a+w)
ax.legend(loc='center right')
showfig()
fig.savefig( "coupled_p4_func.pdf", transparent=True )
