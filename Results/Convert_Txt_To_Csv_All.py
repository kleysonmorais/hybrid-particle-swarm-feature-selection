import csv

nomeBase = 'cancer'
algoritmos = ['cso', 'pso', 'hibrido']

for algoritmo in algoritmos:
    print('\n', algoritmo)
    for index in range(15):
        print(str(index+1)+'/15')
        URL = 'TCC/'+algoritmo+'/'+nomeBase+'/valores/'+nomeBase+'Exe'+str(index+1)
        URL_txt = URL+'.txt'
        URL_csv = URL+'.csv'

        with open(URL_txt, 'r') as in_file:
            stripped = (line.strip() for line in in_file)
            with open(URL_csv, 'w') as out_file:
                writer = csv.writer(out_file)
                writer.writerow(('geracao', 'qtdFeatures', 'qtdParticulas', 'fitness'))
                g = 0
                for line in stripped:
                    colunas = line.split(" ")
                    geracao = colunas[0]
                    qtdFeatures = colunas[1]
                    qtdParticulas = colunas[2]
                    fitness = colunas[3]
                    # print(int(geracao) + int(qtdFeatures) + int(qtdParticulas) + float(fitness))
                    if (int(geracao) == g) and ((int(geracao) + int(qtdFeatures) + int(qtdParticulas) + float(fitness)) > 4):
                        writer.writerow((geracao, qtdFeatures, qtdParticulas, fitness))
                        g += 1
