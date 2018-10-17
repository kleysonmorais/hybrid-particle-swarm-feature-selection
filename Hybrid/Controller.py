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

    ac = None
    buffer = None

    def __init__(self, avaliador, BufferController):
        self.ac = avaliador
        self.buffer = BufferController

    def criarParticular(self, particula, nAtributos):
        '''
        Esta função cria uma partícula para o enxame, personalizando a mesma para que tenha as características 
        do banco de dados informado.

        - São gerados aleatoriamente: Posição e Velociade
        - Cada partícula possui também a melhor posição pela qual ela já passou e seu respectivo fitness
        '''
        #Criar array com posição (binário)
        particula._posicao = np.random.randint(2, size = nAtributos)
        #Criar array com velocidade (binário)
        particula._velocidade = np.random.randint(2, size = nAtributos)
        #Melhor posição já passada iniciar com a primeira posição
        # particula._melhorPosicaoLocal = particula._posicao

        #Salvar o fitness da respectiva posição
        self.atualizaFitness(particula)
        # print("Partícula Criada:")
        # print(particula._posicao,' | ', particula._fitness)

    def atualizaFitness(self, particula):
        '''
        Função para calcular o fitness da partícula, onde 1 significa atributo utilizado e 0 não utilizado
        '''        

        if self.buffer.search_buffer(particula._posicao):
            self.buffer.save_buffer(particula._posicao)

        merito = self.buffer.search_buffer_global(particula._posicao)
        if merito is None:
            # merito = self.ac.RandomForest(particula._posicao)
            merito = self.ac.NaiveBayes(particula._posicao)
            # merito = self.ac.KNeighborsClassifier(particula._posicao)
            self.buffer.save_buffer_global(particula._posicao, merito)
    
        # print(self.buffer.search_buffer_global(particula._posicao))
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

    def particulaMedia(self, enxame):
        tamanho = len(enxame._particulas)
        particula_media = []
        for index in range(len(enxame._particulas[0]._posicao)):
            somatorio = 0
            for particula in enxame._particulas:
                somatorio += particula._posicao[index]
            media_enxame = float(somatorio)/float(tamanho)
            if media_enxame > 0.5:
                particula_media.append(1)
            elif media_enxame < 0.5:
                particula_media.append(0)
            else:
                # Igual a 0.5
                # Recebe um número aleatório (0 ou 1)
                particula_media.append(randint(0, 1))
        return particula_media


class EnxameController:

    pc              = None
    nAtributos      = None
    buffer = None
  
    def __init__(self, nAtributos, avaliador, BufferController):
        self.pc = ParticulaController(avaliador, BufferController)
        self.nAtributos = nAtributos
        self.buffer = BufferController

    def criarEnxame(self, enxame, nParticulas):
        print("Criando Enxame de Partículas")
        for i in range(nParticulas):
            #Criando instância de uma nova partícula e adicionando ao enxame
            novaParticula = ParticulaModel()
            self.pc.criarParticular(novaParticula, self.nAtributos)
            enxame._particulas.append(novaParticula)
        print("Enxame Criado Com Sucesso")

    def atualizaMelhorPosicaoEnxame(self, enxame):
        # print("Atualizando Melhor Posição do Enxame")

        for particula in enxame._particulas:
            if (enxame._melhorFitness is None) or (particula._fitness > enxame._melhorFitness):
                enxame._melhorPosicaoGlobal = np.copy(particula._melhorPosicaoLocal)
                enxame._melhorFitness = particula._fitness

        for particula in enxame._particulas:
            particula._melhorPosicaoGlobal = np.copy(enxame._melhorPosicaoGlobal)
            
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

        # print("Enxame Dividido: ", len(enxame._particulas))
        return sub_pso, sub_cso