from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

nome = "wine"
nomeBase = "../datasets/"+nome+"/"+nome+".csv"
data = pd.read_csv(nomeBase)
y = data.classe
list = ['classe']
X = data.drop(list, axis=1)

X = StandardScaler().fit_transform(X)
pca = PCA()

pca = pca.fit(X)
print(pca.explained_variance_ratio_)
principalComponents = pca.transform(X)

principalDf = pd.DataFrame(data = principalComponents
             , columns = ['principal component 1', 'principal component 2'])
finalDf = pd.concat([principalDf, data[['classe']]], axis = 1)

fig = plt.figure(figsize = (8,8))
ax = fig.add_subplot(1,1,1) 
ax.set_xlabel('Principal Component 1', fontsize = 15)
ax.set_ylabel('Principal Component 2', fontsize = 15)
ax.set_title('2 component PCA', fontsize = 20)
classes = [1, 2, 3]
colors = ['r', 'g', 'b']
for classe, color in zip(classes,colors):
    indicesToKeep = finalDf['classe'] == classe
    ax.scatter(finalDf.loc[indicesToKeep, 'principal component 1']
               , finalDf.loc[indicesToKeep, 'principal component 2']
               , c = color
               , s = 50)
ax.legend(classes)
ax.grid()

plt.show()
