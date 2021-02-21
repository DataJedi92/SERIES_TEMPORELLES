# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 22:33:04 2020

@author: Marcel64
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



#LA SERIE TEMPORELLE
data=[1248.30,1392.10,1056.60,3159.10,890.80,1065.30,1117.60, \
      2934.20,1138.20,1456.00,1224.30,3090.20]


# affichage du graphique
X_label = [str('T'+str(n)) for n in range(1,len(data)+1)]

data_labeled=pd.Series(data,X_label)


graph=data_labeled.plot()
graph.set_ylabel('nombres de macarons vendus')
graph.set_xlabel('Trimestres')
plt.show()


#transformation de la liste en numpy array
data_n=np.array(data)
#reshape
data_w=data_n.reshape(3,4)

print(data_w.shape)
print(data_w)


# ANALYSE DE LA SAISONNALITE

# calcul des moyennes
#       moyenne générale
print(data_w.mean())

#       moyenne des trimestres
for i in range(data_w.shape[1]):
    print(data_w[:,i].mean())
    
# calcul des sommes des différences au carré
#       St = Somme Période/trimetre
St=0
for i in range(data_w.shape[1]):
    St= St + pow(data_w[:,i].mean() - data_w.mean(),2 )
St=St*data_w.shape[0]
print(St)
 

#       Sr = Somme Residuelle
Sr=0
for i in range(data_w.shape[0]):
    for j in range(data_w.shape[1]):
        Sr = Sr + pow(data_w[i,j] - data_w[i,:].mean() - data_w[:,j].mean() + data_w.mean(),2)


# calcul des variances

#   Vt = Variance Trimestrielle
Vt = St / (data_w.shape[1]-1)

#   Vr = Variance Residu
Vr = Sr / ((data_w.shape[1]-1) * (data_w.shape[0]-1))


# calcul du Fishcer de la table
import scipy.stats as stat
print(stat.f.ppf(0.95,dfn=3,dfd=6))
FischerTable = stat.f.ppf(0.95,dfn=3,dfd=6)

# calcul du Fischer empirique :
FisherEmp = Vt / Vr

# test de détermination de la saisonnalité
if (FisherEmp > FischerTable ):
    print("série saisonnière")
else:
    print("série non saisonnière")
    
    


    

# ANALYSE DE LA TENDANCE
    
    
# calcul des moyennes
#       moyenne générale
print(data_w.mean())

#       moyenne des années
print(data_w[0,:].mean())
print(data_w[1,:].mean())
print(data_w[2,:].mean())


# calcul des sommes des différences au carré
#   Sa = Somme Année
Sa=0
for i in range(data_w.shape[0]):
    Sa = Sa + pow(data_w[i,:].mean() - data_w.mean(),2 )
Sa = Sa * data_w.shape[1]

#   Sr = Somme Residuelle
Sr=0
for i in range(data_w.shape[0]):
    for j in range(data_w.shape[1]):
        Sr = Sr + pow(data_w[i,j] - data_w[i,:].mean() - data_w[:,j].mean() + data_w.mean(),2)

#   St = Somme Totale = Sp + Sa + Sr
STot=0
STot = St + Sa + Sr


# calcul des variances

#   Va = Variance Année
Va = Sa / (data_w.shape[0] -1)

#   Vr = Variance Residu
Vr = Sr / ((data_w.shape[1]-1) * (data_w.shape[0]-1))

#   Vtot = Variance Totale
VTot = STot / (data_w.shape[0] * data_w.shape[1] - 1)
    
# test de détermination de la tendance
Fischer_Tendance_Empirique = Va / Vr

Fischer_Tendance_Theorique = stat.f.ppf(0.95,dfn=2,dfd=6)

# test de détermination de la tendance
if (Fischer_Tendance_Theorique > Fischer_Tendance_Empirique ):
    print("série sans tendance")
else:
    print("série avec tendance")
    
    
# AUTOCORRELOGRAMME
from statsmodels.graphics.tsaplots import plot_acf
plot_acf(data, lags=10)




# PROCHAINE ETAPE ON CROIT QUE LA SERIE A UNE TENDANCE
# DONC ELIMINATION DE TENDANCE SOIT PAR REGRESSION DU TEMPS
# SOIT PAS PASSAGE DES DIFFERENCES