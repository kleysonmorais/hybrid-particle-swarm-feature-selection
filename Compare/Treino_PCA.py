from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split, cross_val_predict
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

nome = "sonar"
nomeBase = "../datasets/"+nome+"/"+nome+".csv"
data = pd.read_csv(nomeBase)
y = data.classe
list = ['classe']
x = data.drop(list, axis=1)

print('#########################################################################\n')
print(nome, ': ', x.shape)
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)


classificador = KNeighborsClassifier()
classificador = classificador.fit(x_train, y_train)
predict = classificador.predict(x_test)

CM = confusion_matrix(y_test, predict)
TN = CM[0][0]
FN = CM[1][0]
TP = CM[1][1]
FP = CM[0][1]  

# print('TN: ', TN)
# print('FN: ', FN)
# print('TP: ', TP)
# print('FP: ', FP)

precisao = (TP+TN)/(TP+FP+FN+TN)
recall = TP/(TP + FN)
acuracia = (TP+TN)/(TP+FP+FN+TN)
f1Score = 2 * (precisao * recall) / (precisao + recall)

print('Precisão: ', precisao)
print('F1 Score: ', f1Score)
print('Recall: ', recall)
print('Acurácia: ', acuracia)

print('#########################################################################\n')
scaler = StandardScaler()

scaler.fit(x_train)
x_train = scaler.transform(x_train)
x_test = scaler.transform(x_test)

pca = PCA(n_components=8)
pca = pca.fit(x_train)
x_train = pca.transform(x_train)
x_test = pca.transform(x_test)
print("PCA: ", x_train.shape)

# classificador = RandomForestClassifier(random_state=42)
classificador = KNeighborsClassifier()
predict = cross_val_predict(classificador, x_train, y_train, cv=10, n_jobs=-1)

# classificador = classificador.fit(x_train, y_train)
# predict = classificador.predict(x_test)

CM = confusion_matrix(y_train, predict)
TN = CM[0][0]
FN = CM[1][0]
TP = CM[1][1]
FP = CM[0][1]  

# print('TN: ', TN)
# print('FN: ', FN)
# print('TP: ', TP)
# print('FP: ', FP)

precisao = (TP+TN)/(TP+FP+FN+TN)
recall = TP/(TP + FN)
acuracia = (TP+TN)/(TP+FP+FN+TN)
f1Score = 2 * (precisao * recall) / (precisao + recall)

print('Precisão: ', precisao)
print('F1 Score: ', f1Score)
print('Recall: ', recall)
print('Acurácia: ', acuracia)