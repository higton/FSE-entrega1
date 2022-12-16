class DistServer:
    def __init__(self):
        self.nome = ""
        self.arcondicionado = 0
        self.aspersor = 0
        self.alarme = 0
        self.lampada_corredor = 0
        self.fumaca = 0
        self.janelas = [0, 0]
        self.lampadas = [0, 0]
        self.quantidade_de_pessoas = 0
        self.temperatura = 0
        self.porta = 0
        self.umidade = 0
        self.projector = 0
        self.presence = 0

    def switch_lampada(self, i: int):
        self.lampadas[i] = not self.lampadas[i]

    def switch_arcondicionado(self):
        self.arcondicionado = not self.arcondicionado

    def switch_corredor(self):
        self.lampada_corredor = not self.lampada_corredor

    def switch_aspersor(self):
        self.aspersor = not self.aspersor