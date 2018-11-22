import csv
import pandas as pd

nomeBase = 'cancer'
algoritmos = ['cso', 'pso', 'hibrido']

for algoritmo in algoritmos:
    print('\n', algoritmo)
    tamanho = 15
    quantidadeExecucoes = 151
    qtdFeatures = [0 for _ in range(quantidadeExecucoes)]
    qtdParticulas = [0 for _ in range(quantidadeExecucoes)]
    fitness = [0 for _ in range(quantidadeExecucoes)]

    for index in range(tamanho):
        print(str(index+1),'/',tamanho)
        URL_csv = 'TCC/'+algoritmo+'/'+nomeBase+'/valores/'+nomeBase+'Exe'+str(index+1)+'.csv'

        data = pd.read_csv(URL_csv)

        geracoes = data.geracao
        qf = data.qtdFeatures
        qP = data.qtdParticulas
        fit = data.fitness

        for geracao in range(len(geracoes)):
            qtdFeatures[geracao] += qf[geracao]
            qtdParticulas[geracao] += qP[geracao]
            fitness[geracao] += fit[geracao]

    with open('TCC/'+algoritmo+'/'+nomeBase+'/valores/'+nomeBase+'MEDIA_TOTAL.csv', 'w') as out_file:
        writer = csv.writer(out_file)
        writer.writerow(('geracao', 'qtdFeatures', 'qtdParticulas', 'fitness'))
        for geracao in range(len(geracoes)):
            qf = (qtdFeatures[geracao]/tamanho)
            qp = (qtdParticulas[geracao]/tamanho)
            fi = (fitness[geracao]/tamanho)
            writer.writerow((geracao, qf, qp, fi))
