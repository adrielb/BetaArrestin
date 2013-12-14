import statsmodels.api as sm
import numpy as np
import SPSA_rprop as spsa
from BetaArrestin import *
reload(spsa)


pre = '/tmp/'

Qnames = (
    'maxdose'    ,
    'StotNative' ,
    'StotOE'     ,
    'p2'         ,
    'p5'         ,
    'p3a'        ,
    'p3b'        ,
    'p3c'        ,
    'p3d'        ,
    'p3e'        ,
    'p4a'        ,
    'p4b'        ,
    'p4n'    )

    'grad'       : 1.0 ,
    'maxdose'    : 0.0085 ,
    'l'          : 1.0 ,
    'dx'         : 0.0001,
    'slevel'     : 'StotNone' ,
    'stot'       : 0.0 ,
    'stotnone'   : 0.0 ,
    'stotnative' : 1.5,
    'stotopt'    : 3.3 ,
    'stotoe'     : 42.0 ,
    'p2'         : 0.89 ,
    'p5'         : 7.7 ,
    'p3a'        : 0.00088 ,
    'p3b'        : 0.48 ,
    'p3c'        : 2.1 ,
    'p3d'        : 0.02 ,
    'p3e'        : 1.5 ,
    'p4a'        : 0.001 ,
    'p4b'        : 6.5 ,
    'p4n'        : 50 ,
    'di'         : 0.0001,
    'tp'         : 5e-1

def loss( Q ):
    sim = dose_response({ 'slevel' : 'StotNative' })
    return Q * Q

def run_opt():
    spsa.constraints = constraints
    spsa.loss = loss
    spsa.max_iter = 1
    Q0 = np.array( [100] )
    spsa.run_log( Q0 )

    df = spsa.readlog()
    print df.head()

def constraints( Q ):
    return np.clip( Q, 0, 1e10 )

def unpack_Q( Q ):
    return

def viz_opt():
    df = pd.read_csv( pre+'sim.csv' )

reload( BetaArrestin )
sim = dose_response({ 'slevel' : 'StotOE' }, num=1)

sim = dose_response({ 'slevel' : 'StotOE' })
sim.to_csv( pre+'sim.csv', index=False )

ols = sm.OLS( exog=sm.add_constant(sim.index), endog=sim['MI'] ).fit()
ols.summary()


x=np.arange( 5000 )
y=x+0
y[0] = 1
ols = sm.OLS( exog=sm.add_constant(x), endog=y ).fit()
ols.mse_resid
ols.summary()

l = np.array([0,1])
est = ols.params['const'] + ols.params['x1'] * l
sim['MI'].plot()
ax = plt.gca()
ax.plot( l, est )
plt.show()

