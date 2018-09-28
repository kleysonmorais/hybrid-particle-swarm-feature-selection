# ------------------------------------------------------------------------------+
#
#   Morais, Kleyson.
#   08, 2018
#
# ------------------------------------------------------------------------------+

# from Controller import *
from PSO.PsoController import EnxameController

import numpy as np
import pandas as pd
import sys

class PsoLearning:

    ec = None

    def __init__(self):
        self.ec = EnxameController()

    def aprendizagem(self, enxame):
        print("Aprendizagem PSO")

        print("Antes")
        for particula in enxame._particulas:
            print(particula._posicao)

        self.ec.atualizaMelhorPosicaoEnxame(enxame)
        self.ec.atualizaEnxame(enxame)

        print("Depois")
        for particula in enxame._particulas:
            print(particula._posicao)
