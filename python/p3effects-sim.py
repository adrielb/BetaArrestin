from BetaArrestin import *
import pickle

with open( 'p3effects-params.pickle', 'r' ) as f:
    p3s = pickle.load(f)

sims = pd.DataFrame()
for p in p3s:
    for s in ['StotNative', 'StotOE']:
        p['slevel'] = s
        print p
        sim = dose_response( p, num=50 )
        sims = sims.append(sim[['MAPKpp','MI','slevel','name']])

sims.index.name = 'Input'

sims.to_csv('p3effects.csv')
