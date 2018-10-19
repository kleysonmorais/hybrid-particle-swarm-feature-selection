import csv

nomeBase = 'wine'

for index in range(30):
    print(str(index+1)+'/30')
    URL = '../buffer/'+nomeBase+'/'+nomeBase+'Exe'+str(index+1)
    URL_txt = URL+'.txt'
    URL_csv = URL+'.csv'

    with open(URL_txt, 'r') as in_file:
        stripped = (line.strip() for line in in_file)
        with open(URL_csv, 'w') as out_file:
            writer = csv.writer(out_file)
            writer.writerow(('geracao', 'qtdFeatures', 'qtdParticulas', 'fitness'))
            for line in stripped:
                colunas = line.split(" ")
                geracao = colunas[0]
                qtdFeatures = colunas[1]
                qtdParticulas = colunas[2]
                fitness = colunas[3]
                writer.writerow((geracao, qtdFeatures, qtdParticulas, fitness))
