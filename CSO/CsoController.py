#------------------------------------------------------------------------------+
#
#   Morais, Kleyson.
#   April, 2018
#
#------------------------------------------------------------------------------+

#--- IMPORT DEPENDENCIES ------------------------------------------------------+

from random import randint
import numpy as np
import random
import copy

class ParticulaController:

    def atualizaPosicao(self, p1, p2, media_enxame):
        '''
        Esta função é responsável pela movimentação das partículas no espaço, calculando suas respectivas velocidades
        para descobrir as novas posições.

        - A variáveis c é constante para o cálculo, convencionalmente utiliza-se 2.5
        - e1 e e2 são variáveis de atrito para o movimento da partícula
        - valorMaximo é um limite que não permite a ser ultrapassada, convencionalmente utiliza-se [-6, 6]
        '''
        
        if p1._fitness > p2._fitness:
            pWin = p1
            pLoser = p2
        else:
            pWin = p2
            pLoser = p1
        
        c = 2.5

        #Número aleatório entre 0 e 1
        r1 = np.random.rand() 
        r2 = np.random.rand() 
        r3 = np.random.rand() 
        valorMaximo = 6

        for i, velocidade in enumerate(pLoser._velocidade):
            #Calculando velocidade
            velocidade = (r1 * velocidade) + (r2 * (pWin._posicao[i] - pLoser._posicao[i])) + (c * r3 * (media_enxame[i] - pLoser._posicao[i]))
            #Verificar Limite
            if abs(velocidade) > valorMaximo and abs(velocidade) is velocidade:
                velocidade = valorMaximo
            elif abs(velocidade) > valorMaximo:
                velocidade = -valorMaximo
            velocidade = self.sigmoid(velocidade)
        
            #Condicional de definição 0 ou 1
            if velocidade > 0.5:
                pLoser._velocidade[i] = 1
            elif velocidade < 0.5:
                pLoser._velocidade[i] = 0
            else:
                # Igual a 0.5, recebe bit aleatório (0 ou 1)
                pLoser._velocidade[i] = randint(0, 1)
            
            aux = np.random.rand()
            if aux < velocidade:
                pLoser._posicao[i] = 1
            else:            
                pLoser._posicao[i] = 0
        
    def sigmoid(self, x):
        return 1.0/(1.0 + np.exp(-(x)))


class EnxameController:

    pc = None
  
    def __init__(self):
        self.pc = ParticulaController()

    def atualizaEnxame(self, sub_pso, sub_cso, particula_media):
        for i, p1 in enumerate(sub_pso._particulas):
            self.pc.atualizaPosicao(p1, sub_cso._particulas[i], particula_media)

