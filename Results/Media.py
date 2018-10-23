import csv
import pandas as pd

nomeBase = 'ionosphere'
qtdFeatures = [0 for _ in range(201)]
qtdParticulas = [0 for _ in range(201)]
fitness = [0 for _ in range(201)]

for index in range(30):
    print(str(index+1)+'/30')
    URL_csv = '../buffer/'+nomeBase+'/'+nomeBase+'Exe'+str(index+1)+'.csv'

    data = pd.read_csv(URL_csv)

    geracoes = data.geracao
    qf = data.qtdFeatures
    qP = data.qtdParticulas
    fit = data.fitness

    for geracao in range(len(geracoes)):
        qtdFeatures[geracao] += qf[geracao]
        qtdParticulas[geracao] += qP[geracao]
        fitness[geracao] += fit[geracao]

with open('../buffer/'+nomeBase+'/'+nomeBase+'MEDIA_TOTAL.csv', 'w') as out_file:
    writer = csv.writer(out_file)
    writer.writerow(('geracao', 'qtdFeatures', 'qtdParticulas', 'fitness'))
    for geracao in range(len(geracoes)):
        qf = (qtdFeatures[geracao]/30)
        qp = (qtdParticulas[geracao]/30)
        fi = (fitness[geracao]/30)
        writer.writerow((geracao, qf, qp, fi))
