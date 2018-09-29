# ------------------------------------------------------------------------------+
#
#   Morais, Kleyson.
#   08, 2018
#
# ------------------------------------------------------------------------------+

from Hybrid.Models import EnxameModel, DadosModel
from Hybrid.Controller import EnxameController
from EvaluationMetric.avaliador import AvaliadorController
from PSO.PsoLearning import PsoLearning
from CSO.CsoLearning import CsoLearning

import numpy as np
import pandas as pd
import sys

def inicializa(nome, qtdParticulas):
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
    enxameController = EnxameController(dadosModel, avaliarController)
    enxameController.criarEnxame(enxame, qtdParticulas)

    return enxame, enxameController, avaliarController, pso, cso

def aprendizagem(enxame, enxameController, geracoes, avaliarController, pso, cso):
    
    for geracao in range(geracoes):
        print(geracao, '/', geracoes)
        enxameController.atualizaMelhorPosicaoEnxame(enxame)
        sub_pso, sub_cso = enxameController.dividirEnxame(enxame)
        
        pso.aprendizagem(sub_pso)
        particula_media = enxameController.pc.particulaMedia(sub_pso)
        cso.aprendizagem(sub_pso, sub_cso, particula_media)

        for i, particula in enumerate(sub_pso._particulas):
            enxameController.pc.atualizaFitness(particula)
            enxame._particulas.append(particula)

            enxameController.pc.atualizaFitness(sub_cso._particulas[i])
            enxame._particulas.append(sub_cso._particulas[i])
        
    enxameController.atualizaMelhorPosicaoEnxame(enxame)
    print()
    for particula in enxame._particulas:
        print(particula._posicao,' | ', particula._fitness)
    
    print("\nMelhor Particula")
    print(enxame._melhorPosicaoGlobal,' | ', enxame._melhorFitness)

    print("\nParticula Média")
    particula_media = enxameController.pc.particulaMedia(enxame)
    print(particula_media)
        
def avaliar(enxame, enxameController, avaliarController):
    enxameController.verificarMelhorPosicaoEnxame(enxame)
    avaliarController.allClassifiers(enxame._melhorPosicaoGlobal)

if __name__ == "__main__":

    # Wine = [1 1 0 1 1 1 1 0 1 1 0 0 1]  |  0.9896554468051245
    # Wine = [1 0 1 0 1 1 1 1 0 1 1 1 1]  |  0.9948348133579673

    if len(sys.argv) != 4:
        print("Exemplo:")
        print("python Main.py base qtdParticulas geracoes")
        exit()

    nomeBase = "../datasets/"+sys.argv[1]
    
    qtdParticulas = int(sys.argv[2])
    geracoes = int(sys.argv[3])

    enxame, enxameController, avaliarController, pso, cso = inicializa(nomeBase, qtdParticulas)
    aprendizagem(enxame, enxameController, geracoes, avaliarController, pso, cso)
    # avaliar(enxame, enxameController, avaliarController)
