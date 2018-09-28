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

    # Inicializando Enxame
    enxame = EnxameModel()
    enxameController = EnxameController(dadosModel, avaliarController)
    enxameController.criarEnxame(enxame, qtdParticulas)

    return enxame, enxameController, avaliarController, pso

def aprendizagem(enxame, enxameController, geracoes, avaliarController, pso):
    sub_pso, sub_cso = enxameController.dividirEnxame(enxame)
    
    pso.aprendizagem(sub_pso)
    
    # Chamar aprendizagem em pso
    
    # print("Sub Pso: ", len(sub_pso._particulas))
    # for particula in sub_pso._particulas:
    #     print(particula._fitness)

    # print("\nSub Cso: ", len(sub_cso._particulas))
    # for particula in sub_cso._particulas:
    #     print(particula._fitness)
        
def avaliar(enxame, enxameController, avaliarController):
    enxameController.verificarMelhorPosicaoEnxame(enxame)
    avaliarController.allClassifiers(enxame._melhorPosicaoGlobal)

if __name__ == "__main__":

    if len(sys.argv) != 4:
        print("Exemplo:")
        print("python Main.py base qtdParticulas geracoes")
        exit()

    nomeBase = "../datasets/"+sys.argv[1]
    
    qtdParticulas = int(sys.argv[2])
    geracoes = int(sys.argv[3])

    enxame, enxameController, avaliarController, pso = inicializa(nomeBase, qtdParticulas)
    aprendizagem(enxame, enxameController, geracoes, avaliarController, pso)
    # avaliar(enxame, enxameController, avaliarController)
