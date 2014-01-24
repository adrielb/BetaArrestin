from BetaArrestin import *
from FigDisplay import *

'''
Noco inhibits
Rab11: recycling endosomes
active transport btwn front and back
gradient of ves sharper than gradient of ligand
  due to Rab11 / microtubles
Rab11 enhances ves transport to membrane
Rab11 localized to back
Rab11DN inhibits recycling to mem
E. Noco: Vesicle to mem inhib (p4 50%)
C. Drug: Mem to ves (p3 95%)
more Rab11 in back in WT
Rab11 enables ves transport
p4 sensitive to F/B, proportional to position (or
  1/scaffold)
Rab11 inhibition - makes gradient smaller (scale
  factor)
Noco  -  suppress assym of Rab11
Noco  -  inhibits Arrb2 polarization
         increases ERK-P
Rab11DN eliminates gradient of recycling (p4
  evenly distributed across cell)
'''

sim = pd.read_csv('rab11dn.csv')
sim = sim.set_index( ['name', 'Input'] )
ctrl = sim['MI']['ctrl']
rab11dn = sim['MI']['rab11dn']

#displayfig()

fig, ax = genfig(2)
fig.delaxes( ax )
ax = fig.add_subplot( 1,2,1 )

ax.plot( ctrl.index , ctrl    , label='Ctrl'    , color='blue' )
ax.plot( ctrl.index , rab11dn , label='Rab11DN' , color='pink' )
ax.set_xlabel("Input")
ax.set_ylabel("MI")
ax.legend(loc='center right')
ax = fig.add_subplot( 1,2,2 )
ax.set_title("Avg MI")
avgMI = pd.Series(
            [ ctrl.mean(), rab11dn.mean() ],
            index = ['Ctrl', 'Rab11DN']
            )
ax = avgMI.plot(kind='bar', color=['blue','pink'])
ax.set_xticklabels(['Ctrl','Rab11DN'],rotation='horizontal')
fig.savefig( "rab11dn.pdf", transparent=True )
showfig()

