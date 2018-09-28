#------------------------------------------------------------------------------+
#
#   Morais, Kleyson.
#   April, 2018
#
#------------------------------------------------------------------------------+

#--- IMPORT DEPENDENCIES ------------------------------------------------------+

from Hybrid.Models import *
from EvaluationMetric.avaliador import AvaliadorController
from random import randint
import numpy as np
import random
import copy

class ParticulaController:

    dadosModel = None
    ac = None

    def __init__(self, avaliador):
        self.ac = avaliador

    def criarParticular(self, particula, dados):
        '''
        Esta função cria uma partícula para o enxame, personalizando a mesma para que tenha as características 
        do banco de dados informado.

        - São gerados aleatoriamente: Posição e Velociade
        - Cada partícula possui também a melhor posição pela qual ela já passou e seu respectivo fitness
        '''
        self.dadosModel = dados
        nLinhas, nAtributos = self.dadosModel._dados.shape
        #Criar array com posição (binário)
        particula._posicao = np.random.randint(2, size = nAtributos)
        #Criar array com velocidade (binário)
        particula._velocidade = np.random.randint(2, size = nAtributos)
        #Melhor posição já passada iniciar com a primeira posição
        # particula._melhorPosicaoLocal = particula._posicao

        #Salvar o fitness da respectiva posição
        self.atualizaFitness(particula)
        print("Partícula Criada:")
        print(particula._posicao,' | ', particula._fitness)

    def atualizaFitness(self, particula):
        '''
        Função para calcular o fitness da partícula, onde 1 significa atributo utilizado e 0 não utilizado
        '''        
        merito = self.ac.RandomForest(particula._posicao)
        # merito = self.ac.NaiveBayes(particula._posicao)
        if particula._fitness is None or merito > particula._fitness:
            particula._melhorPosicaoLocal = np.copy(particula._posicao)
            particula._fitness = merito

    def competir(self, p1, p2):
        if p1._fitness > p2._fitness:
            pWin = p1
            pLoser = p2
        else:
            pWin = p2
            pLoser = p1
        return pWin, pLoser


class EnxameController:

    pc              = None
    dadosModel      = None
  
    def __init__(self, DadosModel, avaliador):
        self.pc = ParticulaController(avaliador)
        self.dadosModel = DadosModel

    def criarEnxame(self, enxame, nParticulas):
        print("Criando Enxame de Partículas")
        for i in range(nParticulas):
            #Criando instância de uma nova partícula e adicionando ao enxame
            novaParticula = ParticulaModel()
            self.pc.criarParticular(novaParticula, self.dadosModel)
            enxame._particulas.append(novaParticula)
        print("Enxame Criado Com Sucesso")


    def dividirEnxame(self, enxame):
        
        sub_pso = EnxameModel()
        sub_cso = EnxameModel()
        
        while len(enxame._particulas) > 1:
            if len(enxame._particulas) >= 2:
                while True:
                    p1 = random.choice(enxame._particulas)
                    p2 = random.choice(enxame._particulas)
                    if p1 != p2:    
                        break
                
                pWin, pLoser = self.pc.competir(p1, p2)
                sub_pso._particulas.append(pWin)
                sub_cso._particulas.append(pLoser)
                
                enxame._particulas.remove(p1)
                enxame._particulas.remove(p2)
            # else:
            #     resto = enxame._particulas.pop()
            #     sub_cso._particulas.append(resto)

        print("Enxame Dividido: ", len(enxame._particulas))
        return sub_pso, sub_cso