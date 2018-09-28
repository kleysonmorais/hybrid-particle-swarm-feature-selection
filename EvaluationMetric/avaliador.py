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


class AvaliadorController():

    dados                   = None
    atributoClassificador   = None

    def __init__(self, dados, atributoClassificador):
        self.dados                  = dados
        self.atributoClassificador  = atributoClassificador

    def selectionFeatures(self, features):
        aux = np.asarray(self.dados)
        if np.count_nonzero(features) == 0:
            X_subset = aux
        else:
            X_subset = aux[:,features==1]
        return X_subset

    def geracao(self, features):
        X_subset = self.selectionFeatures(features)
        print("Quantidade de Features: ", X_subset.shape[1])
        # f1score, acuracia = self.allMetrics(RandomForestClassifier(random_state=43), X_subset)
        f1score, acuracia = self.allMetrics(GaussianNB(), X_subset)
        print('F1 Score: ', f1score,'%')
        print('Acurácia: ', acuracia,'%')


    def allClassifiers(self, features):
        
        print("\nRandom Forest Classifier")        
        
        f1score, acuracia = self.allMetrics(RandomForestClassifier(random_state=43), self.dados)
        print('---------------------------------------------------------------------------------------')
        print('F1 Score na base original (', self.dados.shape[1] ,' atributos) é: ', f1score*100,'%')
        print('Acurácia na base original (', self.dados.shape[1] ,' atributos) é: ', acuracia*100,'%')
        print('---------------------------------------------------------------------------------------')
        
        X_subset = self.selectionFeatures(features)
        f1score, acuracia = self.allMetrics(RandomForestClassifier(random_state=43), X_subset)
        print('F1 Score após a Selection Feature Aplicada (', X_subset.shape[1] ,' atributos) é: ', f1score*100,'%')
        print('Acurácia após a Selection Feature Aplicada (', X_subset.shape[1] ,' atributos) é: ', acuracia*100,'%\n')
        # print('---------------------------------------------------------------------------------------')

        print("//////////////////////////////////////////////////////////////////////////////////////////")
        print("\nNaive Bayes")        
        
        f1score, acuracia = self.allMetrics(GaussianNB(), self.dados)
        print('---------------------------------------------------------------------------------------')
        print('F1 Score na base original (', self.dados.shape[1] ,' atributos) é: ', f1score*100,'%')
        print('Acurácia na base original (', self.dados.shape[1] ,' atributos) é: ', acuracia*100,'%')
        print('---------------------------------------------------------------------------------------')
        
        X_subset = self.selectionFeatures(features)
        f1score, acuracia = self.allMetrics(GaussianNB(), X_subset)
        print('F1 Score após a Selection Feature Aplicada (', X_subset.shape[1] ,' atributos) é: ', f1score*100,'%')
        print('Acurácia após a Selection Feature Aplicada (', X_subset.shape[1] ,' atributos) é: ', acuracia*100,'%')
        print('---------------------------------------------------------------------------------------')

        # print("\nNaive Bayes Classifier")
        # ac2 = self.NaiveBayes(features)
        # print('Acurácia após a Selection Feature Aplicada (', X_subset.shape[1] ,' atributos) é: ', ac2*100,'%')

        # print("\nDecision Tree Classifier")
        # ac3 = self.DecisionTree(features)
        # print('Acurácia após a Selection Feature Aplicada (', X_subset.shape[1] ,' atributos) é: ', ac3*100,'%')

        # print("\nSupport Vector Machines Classifier")
        # ac4 = self.SupportVectorMachines(features)
        # print('Acurácia após a Selection Feature Aplicada (', X_subset.shape[1] ,' atributos) é: ', ac4*100,'%')

    def RandomForest(self, features):
        # print("\nRandom Forest Classifier")        
        return self.metrics(RandomForestClassifier(random_state=43), features)

    def NaiveBayes(self, features):
        # print("\nNaive Bayes Classifier")
        return self.metrics(GaussianNB(), features)

    def metrics(self, classificador, features):
        X_subset = self.selectionFeatures(features)
        predicao = cross_val_predict(classificador, X_subset, self.atributoClassificador, cv=10)
        f1Score = f1_score(self.atributoClassificador, predicao, average='macro')
        return f1Score

    def allMetrics(self, classificador, X_subset):
        predicao = cross_val_predict(classificador, X_subset, self.atributoClassificador, cv=10)
        f1Score = f1_score(self.atributoClassificador, predicao, average='macro')
        acuracia = accuracy_score(self.atributoClassificador, predicao)
        return f1Score, acuracia

    