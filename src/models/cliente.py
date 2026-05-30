import random

class Cliente:
    def __init__(self, cid: int):
        self.id = cid
        self.tipo = random.choices(['regular', 'riesgo_alto', 'ocasional'], weights=[0.4, 0.35, 0.25])[0]
        self.preferencia_madres = random.random() > 0.45
        self.riesgo = 0.65 if self.tipo == 'riesgo_alto' else 0.22