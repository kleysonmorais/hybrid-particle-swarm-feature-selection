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
        self.clearBuffer()

    def clearBuffer(self):
        arquivo = open(self.URL, 'w')
        arquivo.writelines("")   
        arquivo.close()

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
