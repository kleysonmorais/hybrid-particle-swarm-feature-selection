import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd

def fitness_generation(nomeBase, data):

    x = data.geracao
    y = data.fitness

    plt.title(nomeBase) 
    plt.xlabel("generation") 
    plt.ylabel("fitness") 

    plt.plot(x,y,'r')
    plt.savefig('fitness_generation.png', format='png')

def particle_generation(nomeBase, data):

    x2 = data.geracao
    y2 = data.qtdParticulas

    plt.title(nomeBase) 
    plt.xlabel("generation") 
    plt.ylabel("number of new solutions") 

    plt.plot(x2,y2,'r')
    plt.savefig('particle_generation.png', format='png')

def selection_generation(nomeBase, data):

    x3 = data.geracao
    y3 = data.qtdFeatures

    plt.title(nomeBase) 
    plt.xlabel("generation") 
    plt.ylabel("number of selected features") 

    plt.plot(x3,y3,'r')
    plt.savefig('selection_generation.png', format='png')

def main():
    nomeBase = 'madelon'

    URL_csv = '../buffer/'+nomeBase+'/'+nomeBase+'MEDIA_TOTAL.csv'
    data = pd.read_csv(URL_csv)

    # fitness_generation(nomeBase, data)
    # particle_generation(nomeBase, data)
    selection_generation(nomeBase, data)

main()