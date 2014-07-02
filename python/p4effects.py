from BetaArrestin import *
from FigDisplay import *

sims = pd.read_csv('p4effects.csv')
sims = sims.set_index( ['lbl','slevel','Input'] )

#displayfig()

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

dSves = np.linspace( -400, 400, 100 )

for l in xrange(lbls.size):
    p = lbls[l]
    fig, ax = genfig(l+1)
    ax.set_title(plot_labels[p])
    ax.set_xlabel("Input")
    ax.set_ylabel("MI")
    ax.set_xlim(auto=True)
    ax.set_ylim(-10 , 14)
    ax.axhline( 0 , color='black' , lw=1 )
    ax.plot( index , sims['MI'].loc['model']['StotNative'] , label='Native; Model'           , color='#FF9999')
    ax.plot( index , sims['MI'].loc[p]['StotNative']       , label='Native; '+plot_labels[p] , color=color_native)
    ax.plot( index , sims['MI'].loc['model']['StotOE']     , label='OE; Model'               , color='#9999FF')
    ax.plot( index , sims['MI'].loc[p]['StotOE']           , label='OE; '    +plot_labels[p] , color=color_oe)
    ax.legend(loc='lower left')
    # p4 inset
    s = sims.loc[p].iloc[0]
    p4funcN0 = p4_func( 0, s['p4a'], s['p4b'], s['p4m'], s['p4n'], 0.1, dSves )
    p4funcN1 = p4_func( 1, s['p4a'], s['p4b'], s['p4m'], s['p4n'], 0.1, dSves )
    p4funcO0 = p4_func( 0, s['p4a'], s['p4b'], s['p4m'], s['p4n'], 0.5, dSves )
    p4funcO1 = p4_func( 1, s['p4a'], s['p4b'], s['p4m'], s['p4n'], 0.5, dSves )
    rect = [0.40, 0.66, 0.48, 0.2]
    ax = fig.add_axes(rect)
    ax.set_xlabel("dSves")
    ax.set_ylabel("p4")
    ax.set_ylim(6.495,6.505)
    ax.plot( dSves , p4funcN0 , color='lightgreen' )
    ax.plot( dSves , p4funcN1 , color='lightgreen' )
    ax.plot( dSves , p4funcO0 , color='green' )
    ax.plot( dSves , p4funcO1 , color='green' )
    ax.grid()
    fig.savefig( "p4effects_" + p + ".pdf", transparent=True )
    showfig(False)

