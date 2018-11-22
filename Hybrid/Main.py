# ------------------------------------------------------------------------------+
#
#   Morais, Kleyson.
#   08, 2018
#
# ------------------------------------------------------------------------------+

from Hybrid.Models import EnxameModel, DadosModel
from Hybrid.Controller import EnxameController
from Hybrid.BufferController import BufferController
from EvaluationMetric.avaliador import AvaliadorController
from PSO.PsoLearning import PsoLearning
from CSO.CsoLearning import CsoLearning
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier

import numpy as np
import pandas as pd
import sys

def inicializa(nome, qtdParticulas, buffer):
    # Lendo a Base
    data = pd.read_csv(nome)
    y = data.classe
    list = ['classe']
    X = data.drop(list, axis=1)

    # Ajustando Parâmetros
    avaliarController = AvaliadorController(X, y, GaussianNB())
    # dadosModel = DadosModel(X, y)
    pso = PsoLearning()
    cso = CsoLearning()

    # Inicializando Enxame
    nLinhas, nAtributos = X.shape
    enxame = EnxameModel()
    enxameController = EnxameController(nAtributos, avaliarController, buffer)
    enxameController.criarEnxame(enxame, qtdParticulas)

    return enxame, enxameController, avaliarController, pso, cso

def save_buffer(enxame, nome_base_dados, execucao, geracao, avaliarController, buffer):
        if geracao is 0:
            conteudo = []
        else:
            arquivo = open('../buffer/'+nome_base_dados+'/'+nome_base_dados+'Exe'+execucao+'.txt', 'r') 
            conteudo = arquivo.readlines()

        texto = str(geracao) + ' ' + str(avaliarController.qtdFeatures(enxame._melhorPosicaoGlobal)) + ' ' + str(buffer.bufferSave) + ' ' + repr(1-enxame._melhorFitness) + ' ' + str(enxame._melhorPosicaoGlobal) + '\n'
        conteudo.append(texto)   
        
        arquivo = open('../buffer/'+nome_base_dados+'/'+nome_base_dados+'Exe'+execucao+'.txt', 'w')
        arquivo.writelines(conteudo)   

        arquivo.close
        buffer.bufferSave = 0

def aprendizagemHibrida(enxame, enxameController, geracoes, avaliarController, pso, cso, nome_base_dados, execucao, buffer):
    print('Realizando Aprendizagem Híbrida...')
    for geracao in range(geracoes):
        print(geracao, '/', geracoes)
        enxameController.atualizaMelhorPosicaoEnxame(enxame)
        save_buffer(enxame, nome_base_dados, execucao, geracao, avaliarController, buffer)
        sub_pso, sub_cso = enxameController.dividirEnxame(enxame)
        
        pso.aprendizagem(sub_pso)
        particula_media = enxameController.pc.particulaMedia(sub_pso)
        cso.aprendizagem(sub_pso, sub_cso, particula_media)

        for i, particula in enumerate(sub_pso._particulas):
            enxameController.pc.atualizaFitness(particula)
            enxame._particulas.append(particula)

            enxameController.pc.atualizaFitness(sub_cso._particulas[i])
            enxame._particulas.append(sub_cso._particulas[i])
        
    print(geracoes, '/', geracoes)
    enxameController.atualizaMelhorPosicaoEnxame(enxame)
    save_buffer(enxame, nome_base_dados, execucao, geracoes, avaliarController, buffer)
    
    print("\nMelhor Particula")
    print(enxame._melhorPosicaoGlobal,' | ', enxame._melhorFitness, '\n')

def aprendizagemPSO(enxame, enxameController, geracoes, avaliarController, pso, cso, nome_base_dados, execucao, buffer):
    print('Realizando Aprendizagem PSO...')
    for geracao in range(geracoes):
        print(geracao, '/', geracoes)
        enxameController.atualizaMelhorPosicaoEnxame(enxame)
        save_buffer(enxame, nome_base_dados, execucao, geracao, avaliarController, buffer)        
        pso.aprendizagem(enxame)

        for i, particula in enumerate(enxame._particulas):
            enxameController.pc.atualizaFitness(particula)
        
    print(geracoes, '/', geracoes)
    enxameController.atualizaMelhorPosicaoEnxame(enxame)
    save_buffer(enxame, nome_base_dados, execucao, geracoes, avaliarController, buffer)
    
    print("\nMelhor Particula")
    print(enxame._melhorPosicaoGlobal,' | ', enxame._melhorFitness, '\n')

def aprendizagemCSO(enxame, enxameController, geracoes, avaliarController, pso, cso, nome_base_dados, execucao, buffer):
    print('Realizando Aprendizagem CSO...')
    for geracao in range(geracoes):
        print(geracao, '/', geracoes)
        enxameController.atualizaMelhorPosicaoEnxame(enxame)
        save_buffer(enxame, nome_base_dados, execucao, geracao, avaliarController, buffer)
        sub_win, sub_loser = enxameController.dividirEnxame(enxame)
        
        particula_media = enxameController.pc.particulaMedia(sub_win)
        cso.aprendizagem(sub_win, sub_loser, particula_media)

        for i, particula in enumerate(sub_win._particulas):
            enxame._particulas.append(particula)

            enxameController.pc.atualizaFitness(sub_loser._particulas[i])
            enxame._particulas.append(sub_loser._particulas[i])
        
    print(geracoes, '/', geracoes)
    enxameController.atualizaMelhorPosicaoEnxame(enxame)
    save_buffer(enxame, nome_base_dados, execucao, geracoes, avaliarController, buffer)
    
    print("\nMelhor Particula")
    print(enxame._melhorPosicaoGlobal,' | ', enxame._melhorFitness, '\n')

def avaliar(enxame, enxameController, avaliarController):
    enxameController.atualizaMelhorPosicaoEnxame(enxame)
    avaliarController.allClassifiers(enxame._melhorPosicaoGlobal)

if __name__ == "__main__":

    # if len(sys.argv) != 4:
    #     print("Exemplo:")
    #     print("python Main.py qtdParticulas geracoes qtdExecucoes")
    #     exit()

    # nome = sys.argv[1]
    
    # nomes = ["cancer", "ionosphere", "isolet5", "madelon", "musk", "sonar", "wine"]
    # nomes = ["isolet5", "madelon", "musk"]
    # nomes = ["cancer", "ionosphere", "sonar", "wine"]
    # Cancer Pendente a partir do 12
    nomes = ["madelon"]
    qtdParticulas = 100
    geracoes = 150
    qtdExecucoes = 15
    # de = 1
    # ate = 2

    for nome in nomes:
        for index in range(qtdExecucoes):  
            print("Base: ", nome)
            print('Execução: ', index)
            nomeBase = "../datasets/"+nome+"/"+nome+".csv"
            execucao = str(index+1)
            buffer = BufferController(nome, execucao)
            enxame, enxameController, avaliarController, pso, cso = inicializa(nomeBase, qtdParticulas, buffer)

            # aprendizagemHibrida(enxame, enxameController, geracoes, avaliarController, pso, cso, nome, execucao, buffer)
            aprendizagemPSO(enxame, enxameController, geracoes, avaliarController, pso, cso, nome, execucao, buffer)
            # aprendizagemCSO(enxame, enxameController, geracoes, avaliarController, pso, cso, nome, execucao, buffer)
            avaliar(enxame, enxameController, avaliarController)
