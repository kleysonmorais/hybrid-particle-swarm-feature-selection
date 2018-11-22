import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd
from matplotlib.legend_handler import HandlerLine2D

def fitness_generation(nomeBase, data_cso, data_pso, data_hibrido):

    cso_x = data_cso.geracao
    cso_y = data_cso.fitness

    pso_x = data_pso.geracao
    pso_y = data_pso.fitness

    hibrido_x = data_hibrido.geracao
    hibrido_y = data_hibrido.fitness

    plt.title(nomeBase) 
    plt.xlabel("gerações") 
    plt.ylabel("fitness") 

    cso, = plt.plot(cso_x, cso_y, label="CSO", linewidth=2)
    pso, = plt.plot(pso_x, pso_y, label="PSO", linewidth=2)
    hibrido, = plt.plot(hibrido_x, hibrido_y, label="Hibrido", linestyle='--')
    plt.legend(handler_map={cso: HandlerLine2D(numpoints=4)})
    plt.savefig('TCC/img/'+nomeBase+'_fitness_generation.png', format='png')

def particle_generation(nomeBase, data_cso, data_pso, data_hibrido):

    cso_x = data_cso.geracao
    cso_y = data_cso.qtdParticulas

    pso_x = data_pso.geracao
    pso_y = data_pso.qtdParticulas

    hibrido_x = data_hibrido.geracao
    hibrido_y = data_hibrido.qtdParticulas

    plt.title(nomeBase) 
    plt.xlabel("gerações") 
    plt.ylabel("número de novas soluções") 

    cso, = plt.plot(cso_x, cso_y, label="CSO", linewidth=2)
    pso, = plt.plot(pso_x, pso_y, label="PSO", linewidth=2)
    hibrido, = plt.plot(hibrido_x, hibrido_y, label="Hibrido", linestyle='--')
    plt.legend(handler_map={cso: HandlerLine2D(numpoints=4)})
    plt.savefig('TCC/img/'+nomeBase+'_particle_generation.png', format='png')

    # x = data.geracao
    # y = data.qtdParticulas

    # plt.title(nomeBase) 
    # plt.xlabel("generation") 
    # plt.ylabel("number of new solutions") 

    # plt.plot(x,y,'r')
    # plt.savefig('TCC/img/particle_generation.png', format='png')

def selection_generation(nomeBase, data_cso, data_pso, data_hibrido):

    cso_x = data_cso.geracao
    cso_y = data_cso.qtdFeatures

    pso_x = data_pso.geracao
    pso_y = data_pso.qtdFeatures

    hibrido_x = data_hibrido.geracao
    hibrido_y = data_hibrido.qtdFeatures

    plt.title(nomeBase) 
    plt.xlabel("gerações") 
    plt.ylabel("número de características selecionadas") 

    cso, = plt.plot(cso_x, cso_y, label="CSO", linewidth=2)
    pso, = plt.plot(pso_x, pso_y, label="PSO", linewidth=2)
    hibrido, = plt.plot(hibrido_x, hibrido_y, label="Hibrido", linestyle='--')
    plt.legend(handler_map={cso: HandlerLine2D(numpoints=4)})
    plt.savefig('TCC/img/'+nomeBase+'_selection_generation.png', format='png')

    # x = data.geracao
    # y = data.qtdFeatures

    # plt.title(nomeBase) 
    # plt.xlabel("generation") 
    # plt.ylabel("number of selected features") 

    # plt.plot(x,y,'r')
    # plt.savefig('TCC/img/selection_generation.png', format='png')

def main():
    nomeBase = 'wine'

    URL_cso = 'TCC/cso/'+nomeBase+'/valores/'+nomeBase+'MEDIA_TOTAL.csv'
    data_cso = pd.read_csv(URL_cso)

    URL_pso = 'TCC/pso/'+nomeBase+'/valores/'+nomeBase+'MEDIA_TOTAL.csv'
    data_pso = pd.read_csv(URL_pso)

    URL_hibrido = 'TCC/hibrido/'+nomeBase+'/valores/'+nomeBase+'MEDIA_TOTAL.csv'
    data_hibrido = pd.read_csv(URL_hibrido)

    # fitness_generation(nomeBase, data_cso, data_pso, data_hibrido)
    # particle_generation(nomeBase, data_cso, data_pso, data_hibrido)
    selection_generation(nomeBase, data_cso, data_pso, data_hibrido)

main()