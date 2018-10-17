import numpy as np
import matplotlib.pyplot as plt

# from sklearn import svm
from sklearn import tree
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score, confusion_matrix, accuracy_score
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import roc_curve, roc_auc_score
from matplotlib import pyplot as plt
from sklearn.preprocessing import label_binarize
from sklearn.neighbors import KNeighborsClassifier

class AvaliadorController():

    dados                   = None
    atributoClassificador   = None
    # X_train                 = None 
    # X_test                  = None
    # y_train                 = None
    # y_test                  = None

    def __init__(self, dados, atributoClassificador):
        self.dados = dados
        self.atributoClassificador = atributoClassificador
        # self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.dados, self.atributoClassificador, test_size=0.33, random_state=43)

    def selectionFeatures(self, features, base):
        aux = np.asarray(base)
        if np.count_nonzero(features) == 0:
            X_subset = aux
        else:
            X_subset = aux[:,features==1]
        return X_subset

    # def geracao(self, features):
    #     X_subset = self.selectionFeatures(features)
    #     print("Quantidade de Features: ", X_subset.shape[1])
    #     f1score, acuracia = self.allMetrics(RandomForestClassifier(random_state=43), X_subset)
    #     f1score, acuracia = self.allMetrics(GaussianNB(), X_subset)
    #     print('F1 Score: ', f1score,'%')
    #     print('Acurácia: ', acuracia,'%')


    def allClassifiers(self, features, classificador):
        
        # print("\nRandom Forest Classifier")        
        
        # f1score, acuracia = self.allMetrics(RandomForestClassifier(random_state=43), self.dados)
        # print('---------------------------------------------------------------------------------------')
        # print('F1 Score na base original (', self.dados.shape[1] ,' atributos) é: ', f1score*100,'%')
        # print('Acurácia na base original (', self.dados.shape[1] ,' atributos) é: ', acuracia*100,'%')
        # print('---------------------------------------------------------------------------------------')
        
        # X_subset = self.selectionFeatures(features)
        # f1score, acuracia = self.allMetrics(RandomForestClassifier(random_state=43), X_subset)
        # print('F1 Score após a Selection Feature Aplicada (', X_subset.shape[1] ,' atributos) é: ', f1score*100,'%')
        # print('Acurácia após a Selection Feature Aplicada (', X_subset.shape[1] ,' atributos) é: ', acuracia*100,'%\n')
        # print('---------------------------------------------------------------------------------------')

        # print("//////////////////////////////////////////////////////////////////////////////////////////")
        # print("\nNaive Bayes")        
        
        # f1score, acuracia = self.allMetrics(GaussianNB(), self.dados)
        # print('---------------------------------------------------------------------------------------')
        # print('Erro: F1 Score na base original (', self.dados.shape[1] ,' atributos) é: ', 1-f1score,'%')
        # print('Erro: Acurácia na base original (', self.dados.shape[1] ,' atributos) é: ', 1-acuracia,'%')
        # print('---------------------------------------------------------------------------------------')
        
        # X_subset = self.selectionFeatures(features)
        # f1score, acuracia = self.allMetrics(GaussianNB(), X_subset)
        # print('Erro: F1 Score após a Selection Feature Aplicada (', X_subset.shape[1] ,' atributos) é: ', 1-f1score,'%')
        # print('Erro: Acurácia após a Selection Feature Aplicada (', X_subset.shape[1] ,' atributos) é: ', 1-acuracia,'%')
        # print('---------------------------------------------------------------------------------------')

        # print("\nKNN")        
        
        f1score, acuracia = self.allMetrics(classificador, self.dados, self.atributoClassificador)
        print('---------------------------------------------------------------------------------------')
        print('Erro: F1 Score na base original (', self.dados.shape[1] ,' atributos) é: ', 1-f1score,'%')
        print('Erro: Acurácia na base original (', self.dados.shape[1] ,' atributos) é: ', 1-acuracia,'%')
        print('---------------------------------------------------------------------------------------')
        
        X_subset = self.selectionFeatures(features, self.dados)
        f1score, acuracia = self.allMetrics(classificador, X_subset, self.atributoClassificador)
        print('Erro: F1 Score após a Selection Feature Aplicada (', X_subset.shape[1] ,' atributos) é: ', 1-f1score,'%')
        print('Erro: Acurácia após a Selection Feature Aplicada (', X_subset.shape[1] ,' atributos) é: ', 1-acuracia,'%')
        print('---------------------------------------------------------------------------------------')


    def KNeighborsClassifier(self, features):
        return self.metrics(KNeighborsClassifier(), features)

    def RandomForest(self, features):
        # print("\nRandom Forest Classifier")        
        return self.metrics(RandomForestClassifier(random_state=43), features)

    def NaiveBayes(self, features):
        # print("\nNaive Bayes Classifier")
        return self.metrics(GaussianNB(), features)

    def metrics(self, classificador, features):
        X_subset = self.selectionFeatures(features, self.dados)
        predicao = cross_val_predict(classificador, X_subset, self.atributoClassificador, cv=10)
        f1Score = f1_score(self.atributoClassificador, predicao, average='micro')
        return f1Score

    def allMetrics(self, classificador, X_subset, y_subset):
        predicao = cross_val_predict(classificador, X_subset, y_subset, cv=10)
        f1Score = f1_score(y_subset, predicao, average='micro')
        acuracia = accuracy_score(y_subset, predicao)
        return f1Score, acuracia

    def qtdFeatures(self, features):
        X_subset = self.selectionFeatures(features, self.dados)
        return X_subset.shape[1]