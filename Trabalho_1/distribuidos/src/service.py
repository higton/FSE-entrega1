from read_config import json_config_parse

class Service:
    def __init__(self):
        self.nome = ""
        self.arcondicionado = False
        self.aspersor = False
        self.alarme = False
        self.corredor = False
        self.gpio_map = {}
        self.fumaca = False
        self.janelas = []
        self.lampadas = []
        self.quantidade_de_pessoas = 0
        self.temperatura = 0
        self.porta = False
        self.umidade = 0
        self.ip_servidor_distribuido = ''
        self.porta_servidor_distribuido = ''

    def setup(self, path: str):
        path = ''

        json_config = json_config_parse(path)

        self.nome = json_config["nome"]
        self.ip_servidor_distribuido = json_config["ip_servidor_distribuido"]
        self.porta_servidor_distribuido = json_config["porta_servidor_distribuido"]
        outputs = json_config["outputs"]

        for output in outputs:
            tag = output["tag"]
            self.gpio_map[tag] = output["gpio"]

    def switch_lampada(self, i: int):
        self.lampadas[i] = not self.lampadas[i]

    def switch_arcondicionado(self):
        self.arcondicionado = not self.arcondicionado

    def switch_corredor(self):
        self.corredor = not self.corredor

    def switch_aspersor(self):
        self.aspersor = not self.aspersor