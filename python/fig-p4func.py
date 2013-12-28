from BetaArrestin import *

x = np.array( [0,1] )
p4a = DEFAULT_PARAMS['p4a']
p4b = DEFAULT_PARAMS['p4b']
p4n = DEFAULT_PARAMS['p4n']
w=600
dsves = np.linspace( -w, w, 100 )

s = np.array( [0.1, 0.1] )
p4n = np.array( [ p4_func( x, p4a, p4b, s, ds ) for ds in dsves ] )
p4n = p4n.transpose()

s = np.array( [0.5, 0.5] )
p4o = np.array( [ p4_func( x, p4a, p4b, s, ds ) for ds in dsves ] )
p4o = p4o.transpose()

fig, ax = genfig()
ax.plot( dsves , p4n[0] , label='Native Back'         , color='black'  )
ax.plot( dsves , p4n[1] , label='Native Front'        , color='blue' )
ax.plot( dsves , p4o[0] , label='OE Back'  , color='black'    , linestyle='dashed' )
ax.plot( dsves , p4o[1] , label='OE Front' , color='blue'     , linestyle='dashed' )
ax.set_title("p4( x, Sves, dSves )")
ax.set_xlabel("dSves Level")
ax.set_ylabel("p4")
w=600
#ax.set_xlim(-w, w)
w=0.002
ax.set_ylim(p4b-p4a-w, p4b+p4a+w)
ax.legend(loc='center right')
showfig()
fig.savefig( "fig-p4func.pdf", transparent=True )


import sys
sys.exit(0)

sves = np.arange(0, 0.5, 0.01)

p4 = np.array( [[ p4_func( x, p4a, p4b, np.array([s,s]), ds )
                 for s in sves ] for ds in dsves ] )

sves, dsves = np.meshgrid( sves, dsves)

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

fig = plt.figure()
ax = fig.gca( projection='3d' )
ax.plot_surface( sves, dsves, p4[:,:,0], rstride=2, cstride=2, cmap=cm.coolwarm )
ax.set_xlabel( "Sves" )
ax.set_ylabel( "dSves" )
ax.set_zlabel( "p4" )
fig.show()
