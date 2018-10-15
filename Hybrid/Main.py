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
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB

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
    avaliarController = AvaliadorController(X, y)
    dadosModel = DadosModel(X, y)
    pso = PsoLearning()
    cso = CsoLearning()

    # Inicializando Enxame
    enxame = EnxameModel()
    enxameController = EnxameController(dadosModel, avaliarController, buffer)
    enxameController.criarEnxame(enxame, qtdParticulas)

    return enxame, enxameController, avaliarController, pso, cso

def save_buffer(enxame, nome_base_dados, execucao, geracao, avaliarController, buffer):
        if geracao is 0:
            conteudo = []
        else:
            arquivo = open('../buffer/'+nome_base_dados+'/'+nome_base_dados+'Exe'+execucao+'.txt', 'r') 
            conteudo = arquivo.readlines()
        
        texto = str(geracao) + ' ' + repr(1-enxame._melhorFitness) + ' ' + str(avaliarController.qtdFeatures(enxame._melhorPosicaoGlobal)) + ' ' + str(buffer.bufferSave) + '\n'
        conteudo.append(texto)   
        
        arquivo = open('../buffer/'+nome_base_dados+'/'+nome_base_dados+'Exe'+execucao+'.txt', 'w')
        arquivo.writelines(conteudo)   

        arquivo.close
        buffer.bufferSave = 0

def aprendizagem(enxame, enxameController, geracoes, avaliarController, pso, cso, nome_base_dados, execucao, buffer):
    
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
    # print()
    # for particula in enxame._particulas:
    #     print(particula._posicao,' | ', particula._fitness)
    
    print("\nMelhor Particula")
    print(enxame._melhorPosicaoGlobal,' | ', enxame._melhorFitness)

    # print("\nParticula Média")
    # particula_media = enxameController.pc.particulaMedia(enxame)
    # print(particula_media)
        
def avaliar(enxame, enxameController, avaliarController):
    enxameController.atualizaMelhorPosicaoEnxame(enxame)
    # avaliarController.allClassifiers(enxame._melhorPosicaoGlobal, KNeighborsClassifier())
    avaliarController.allClassifiers(enxame._melhorPosicaoGlobal, GaussianNB())

if __name__ == "__main__":

    # Wine = [1 1 0 1 1 1 1 0 1 1 0 0 1]  |  0.9896554468051245
    # Wine = [1 0 1 0 1 1 1 1 0 1 1 1 1]  |  0.9948348133579673

    if len(sys.argv) != 4:
        print("Exemplo:")
        print("python Main.py qtdParticulas geracoes qtdExecucoes")
        exit()

    # nome = sys.argv[1]
    
    # nomes = ["cancer", "ionosphere", "isolet5", "madelon", "musk", "sonar", "wine"]
    # nomes = ["isolet5", "madelon", "musk"]
    nomes = ["wine", "sonar"]

    qtdParticulas = int(sys.argv[1])
    geracoes = int(sys.argv[2])
    qtdExecucoes = int(sys.argv[3])

    for index in range(qtdExecucoes):
        for nome in nomes:
            print("Base: ", nome)
            nomeBase = "../datasets/"+nome+"/"+nome+".csv"
            execucao = str(index+1)
            buffer = BufferController(nome, execucao)
            enxame, enxameController, avaliarController, pso, cso = inicializa(nomeBase, qtdParticulas, buffer)

            aprendizagem(enxame, enxameController, geracoes, avaliarController, pso, cso, nome, execucao, buffer)
            avaliar(enxame, enxameController, avaliarController)
