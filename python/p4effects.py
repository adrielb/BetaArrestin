from BetaArrestin import *
from FigDisplay import *

sims = pd.read_csv('p4effects.csv')
sims = sims.set_index( ['lbl','slevel','Input'] )

displayfig()


index = sims.loc['model'].loc['StotNative'].index

fig, ax = genfig()
ax.set_title("")
ax.set_xlabel("Input")
ax.set_ylabel("MI")
ax.set_xlim(auto=True)
ax.set_ylim(-4,4)
ax.plot( index , sims['MI'].loc['model']['StotNative']   , label='Model; Native'        , color=color_native)
ax.plot( index , sims['MI'].loc['model']['StotOE']       , label='Model; OE'            , color=color_oe)
ax.plot( index , sims['MI'].loc['flat']['StotNative']    , label='Flat; Native'         , color=color_native)
ax.plot( index , sims['MI'].loc['flat']['StotOE']        , label='Flat; OE'             , color=color_oe)
ax.plot( index , sims['MI'].loc['highsig']['StotNative'] , label='High Sigmoid; Native' , color=color_native)
ax.plot( index , sims['MI'].loc['highsig']['StotOE']     , label='High Sigmoid; OE'     , color=color_oe)
ax.plot( index , sims['MI'].loc['lowsig']['StotNative']  , label='Low Sigmoid; Native'  , color=color_native)
ax.plot( index , sims['MI'].loc['lowsig']['StotOE']      , label='Low Sigmoid; OE'      , color=color_oe)
ax.legend(loc='upper left')
showfig(False)

lbls = sims.index.levels[0]
plot_labels = {
    'model'   : 'Model',
    'flat'    : 'Flat',
    'highsig' : 'High Sigmoid',
    'lowsig'  : 'Low Sigmoid'
    }

Sves = np.arange(0, 0.5, 0.001)
Sves = 0.1
dSves = np.linspace( -600, 600, 100 )

for l in xrange(lbls.size):
    p = lbls[l]
    s = sims.loc['model'].iloc[0]
    p4func = p4_func( 0, s['p4a'], s['p4b'], s['p4m'], s['p4n'], Sves, dSves )
    fig, ax = genfig(l+1)
    ax.set_title(plot_labels[p])
    ax.set_xlabel("Input")
    ax.set_ylabel("MI")
    ax.set_xlim(auto=True)
    ax.set_ylim(-4 , 9)
    ax.axhline( 0   , color='black'           , lw=1 )
    ax.plot( index , sims['MI'].loc['model']['StotNative'] , label='Model; Native'           , color='#FF9999')
    ax.plot( index , sims['MI'].loc['model']['StotOE']     , label='Model; OE'               , color='#9999FF')
    ax.plot( index , sims['MI'].loc[p]['StotNative']       , label=plot_labels[p]+'; Native' , color=color_native)
    ax.plot( index , sims['MI'].loc[p]['StotOE']           , label=plot_labels[p]+'; OE'     , color=color_oe)
    ax.legend(loc='lower left')
    # p4 inset
    rect = [0.61, 0.54, 0.25, 0.2]
    ax = fig.add_axes(rect)
    ax.set_xlabel("dSves")
    ax.set_ylabel("p4")
    ax.plot( dSves, p4func, color='lightgreen' )
    #ax.plot( Smem, p3funcs[name] , color='green' )
    ax.grid()
    #fig.savefig( "p4effects_" + name + ".pdf", transparent=True )
    showfig(False)

