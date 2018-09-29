# ------------------------------------------------------------------------------+
#
#   Morais, Kleyson.
#   08, 2018
#
# ------------------------------------------------------------------------------+

from CSO.CsoController import EnxameController

class CsoLearning:

    ec = None

    def __init__(self):
        self.ec = EnxameController()

    def aprendizagem(self, sub_pso, sub_cso, particula_media):
        # print("Aprendizagem CSO")
        self.ec.atualizaEnxame(sub_pso, sub_cso, particula_media)