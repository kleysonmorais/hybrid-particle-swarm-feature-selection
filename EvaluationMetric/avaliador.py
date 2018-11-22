import numpy as np
import matplotlib.pyplot as plt

from sklearn.naive_bayes import GaussianNB
# from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score, confusion_matrix, accuracy_score
from sklearn.model_selection import cross_val_predict
# from sklearn.metrics import roc_curve, roc_auc_score
from matplotlib import pyplot as plt
# from sklearn.preprocessing import label_binarize
# from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import precision_score

class AvaliadorController():

    dados                   = None
    atributoClassificador   = None
    classificador = None
    
    def __init__(self, dados, atributoClassificador, classificador):
        self.dados = dados
        self.atributoClassificador = atributoClassificador
        self.classificador = classificador

    def selectionFeatures(self, features, base):
        aux = np.asarray(base)
        if np.count_nonzero(features) == 0:
            X_subset = aux
        else:
            X_subset = aux[:,features==1]
        return X_subset


    def allClassifiers(self, features):
                
        f1score, acuracia, precision_score = self.allMetrics(self.dados, self.atributoClassificador)
        print('---------------------------------------------------------------------------------------')
        print('Erro: F1 Score na base original (', self.dados.shape[1] ,' atributos) é: ', f1score,'%')
        print('Erro: Acurácia na base original (', self.dados.shape[1] ,' atributos) é: ', acuracia,'%')
        print('---------------------------------------------------------------------------------------')
        
        X_subset = self.selectionFeatures(features, self.dados)
        f1score, acuracia, precision_score = self.allMetrics(X_subset, self.atributoClassificador)
        print('Erro: F1 Score após a Selection Feature Aplicada (', X_subset.shape[1] ,' atributos) é: ', f1score,'%')
        print('Erro: Acurácia após a Selection Feature Aplicada (', X_subset.shape[1] ,' atributos) é: ', acuracia,'%')
        print('---------------------------------------------------------------------------------------')

    def taxaGlobal(self):
        f1score, acuracia, precision_score = self.allMetrics(self.dados, self.atributoClassificador)
        print('---------------------------------------------------------------------------------------')
        print('Erro: F1 Score na base original (', self.dados.shape[1] ,' atributos) é: ', f1score,'%')
        print('Erro: Acurácia na base original (', self.dados.shape[1] ,' atributos) é: ', acuracia,'%')
        print('Erro: Precisão na base original (', self.dados.shape[1] ,' atributos) é: ', precision_score,'%')
        print('---------------------------------------------------------------------------------------')

    def GlobalClassifier(self, features):
        return self.metrics(features)

    def metrics(self, features):
        X_subset = self.selectionFeatures(features, self.dados)
        predicao = cross_val_predict(self.classificador, X_subset, self.atributoClassificador, cv=10, n_jobs=-1)
        CM = confusion_matrix(self.atributoClassificador, predicao)

        TN = CM[0][0]
        FN = CM[1][0]
        TP = CM[1][1]
        FP = CM[0][1]  
        precisao = (TP+TN)/(TP+FP+FN+TN)
        recall = TP/(TP + FN)
        # acuracia = (TP+TN)/(TP+FP+FN+TN)
        f1Score = 2 * (precisao * recall) / (precisao + recall)

        # f1Score = f1_score(self.atributoClassificador, predicao, average='micro')
        return f1Score


    def allMetrics(self, X_subset, y_subset):
        predicao = cross_val_predict(self.classificador, X_subset, y_subset, cv=10)
        CM = confusion_matrix(y_subset, predicao)
        
        TN = CM[0][0]
        FN = CM[1][0]
        TP = CM[1][1]
        FP = CM[0][1]  
        precisao = (TP+TN)/(TP+FP+FN+TN)
        recall = TP/(TP + FN)
        acuracia = (TP+TN)/(TP+FP+FN+TN)
        f1Score = 2 * (precisao * recall) / (precisao + recall)

        print('Precisão: ', precisao)
        print('F1 Score: ', f1Score)
        print('Recall: ', recall)
        print('Acurácia: ', acuracia)
        
        return f1Score, acuracia, precisao

    def qtdFeatures(self, features):
        X_subset = self.selectionFeatures(features, self.dados)
        return X_subset.shape[1]