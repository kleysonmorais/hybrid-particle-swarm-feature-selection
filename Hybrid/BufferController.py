import csv

class BufferController:

    nomeBase = None
    bufferSave = None
    execucao = None
    URL = None

    def __init__(self, nome, execucao):
        self.nomeBase = nome
        self.bufferSave = 0
        self.execucao = execucao
        self.URL = '../buffer/'+self.nomeBase+'/'+self.nomeBase+'BufferExe'+self.execucao+'.txt'
        self.URL_GLOBAL = '../buffer/'+self.nomeBase+'/'+self.nomeBase+'BufferGlobal.txt'
        self.clearBuffer()

    def clearBuffer(self):
        arquivo = open(self.URL, 'w')
        arquivo.writelines("")   
        arquivo.close()

        # arquivo = open(self.URL_GLOBAL, 'w')
        # arquivo.writelines("")   
        # arquivo.close()
                
    def search_buffer(self, particulaPosicao):
        arquivo = open(self.URL, 'r')
        m_string = "[" + " ".join(str(x) for x in particulaPosicao) + "]" + '\n'
        for linha in arquivo:
            if m_string == linha:
                return False
        arquivo.close()
        return True

    def save_buffer(self, particulaPosicao):
        arquivo = open(self.URL, 'r') 
        conteudo = arquivo.readlines()
        
        texto = '[' + ' '.join(str(x) for x in particulaPosicao) + ']' + '\n'
        conteudo.append(texto)   
        
        arquivo = open(self.URL, 'w')
        arquivo.writelines(conteudo)   
        arquivo.close()
        self.bufferSave += 1

    def search_buffer_global(self, particulaPosicao):
        arquivo = open(self.URL_GLOBAL, 'r')
        m_string = "[" + " ".join(str(x) for x in particulaPosicao) + "]"
        for linha in arquivo:
            aux = linha[0:(len(m_string))]
            # print("Aux: ", aux)
            if m_string == aux:
                aux2 = linha[len(m_string)+1:-1]
                # print('Merito Encontrado')
                return float(aux2)
        arquivo.close()
        # print('Merito não encontrado')
        return None

    def save_buffer_global(self, particulaPosicao, merito):

        arquivo = open(self.URL_GLOBAL, 'r') 
        conteudo = arquivo.readlines()
        
        texto = '[' + ' '.join(str(x) for x in particulaPosicao) + ']' + ' ' + str(merito) + '\n'
        conteudo.append(texto)   
        
        arquivo = open(self.URL_GLOBAL, 'w')
        arquivo.writelines(conteudo)   
        arquivo.close()
    