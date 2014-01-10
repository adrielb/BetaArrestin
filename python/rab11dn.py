from BetaArrestin import *

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

ctrl = dose_response( { 'slevel' : 'StotNative'} )

p4b = DEFAULT_PARAMS['p4b'] * 0.2
noco = dose_response( { 'slevel' : 'StotNative', 'p4b': p4b } )

csv = pd.DataFrame( index = ctrl.index )
csv['MAPKpp-ctrl'] = ctrl['MAPKpp']
csv['MAPKpp-noco'] = noco['MAPKpp']
csv.index.name = 'Input'
csv.to_csv('noco.csv')

fig = plt.figure(1)
ctrl['MAPKpp-noco'] = noco['MAPKpp']
ax = ctrl['MAPKpp'].plot(color='blue', label='MAPKpp-ctrl')
ax = ctrl['MAPKpp-noco'].plot(color='red')
ax.set_title('Nocodazole treatment')
ax.set_ylabel('MAPKpp')
ax.set_xlabel('Input')
plt.legend(loc='lower right')
fig.savefig( "noco.pdf", transparent=True )

# Rab11DN
rab11dn = dose_response( { 'slevel' : 'StotNative', 'p4a':0 } )

csv = pd.DataFrame( index = ctrl.index )
csv['MI-ctrl'] = ctrl['MI']
csv['MI-rab11dn'] = rab11dn['MI']
csv.index.name = 'Input'
csv.to_csv('rab11dn.csv')

#displayfig()
fig, ax = genfig(2)
fig.delaxes( ax )
ax = fig.add_subplot( 1,2,1 )
ax.plot( ctrl.index, ctrl['MI'] , label='Ctrl', color='blue' )
ax.plot( ctrl.index, rab11dn['MI'] , label='Rab11DN', color='pink' )
ax.set_xlabel("Input")
ax.set_ylabel("MI")
ax.legend(loc='center right')
ax = fig.add_subplot( 1,2,2 )
ax.set_ylabel("Avg MI")
avgMI = pd.Series(
            [ ctrl['MI'].mean(), rab11dn['MI'].mean() ],
            index = ['Ctrl', 'Rab11DN']
            )
ax = avgMI.plot(kind='bar', color=['blue','pink'])
ax.set_xticklabels(['Ctrl','Rab11DN'],rotation='horizontal')
fig.savefig( "rab11dn.pdf", transparent=True )
showfig()

