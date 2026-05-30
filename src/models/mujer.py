from dataclasses import dataclass
import random
from typing import Dict
from .economia import EconomiaMujer
from .embarazo import EmbarazoManager

@dataclass
class Mujer:
    id: int
    tipo_trabajo: str = random.choice(["callejera", "vip"])   # Nuevo
    edad: int = random.randint(22, 48)
    hijos: int = random.randint(1, 5)
    es_viuda: bool = False
    causa_viudez: str = "ninguna"
    atractivo: float = random.uniform(0.4, 0.95)
    ciclo_dia: int = 0
    infectado: Dict[str, bool] = None
    dias_infectado: Dict[str, int] = None
    en_prep: bool = False
    viva: bool = True
    economia: EconomiaMujer = None
    embarazo_manager: EmbarazoManager = None
    embarazos_recientes: int = 0
    dias_sin_trabajar_por_violencia: int = 0   # Nuevo

    def __post_init__(self):
        patogenos = ['VIH', 'Clamidia', 'Gonorrea', 'Sífilis', 'Herpes']
        self.infectado = {p: False for p in patogenos}
        self.dias_infectado = {p: 0 for p in patogenos}
        self.economia = EconomiaMujer(tipo_trabajo=self.tipo_trabajo)
        self.embarazo_manager = EmbarazoManager()

    def vulnerabilidad(self) -> float:
        base = (self.hijos * 0.30) + (1 - self.atractivo) * 0.25
        if self.es_viuda:
            base += 0.45
        if self.economia.deuda > 400:
            base += 0.35
        if self.dias_sin_trabajar_por_violencia > 0:
            base += 0.25
        return min(1.0, base)