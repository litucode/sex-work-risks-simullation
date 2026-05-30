from dataclasses import dataclass
import random
from typing import Dict
from .economia import EconomiaMujer
from .embarazo import EmbarazoManager

@dataclass
class Mujer:
    id: int
    edad: int = random.randint(20, 45)
    hijos: int = random.randint(1, 5)
    es_viuda: bool = False
    causa_viudez: str = "ninguna"
    atractivo: float = random.uniform(0.4, 0.9)
    ciclo_dia: int = 0
    infectado: Dict[str, bool] = None
    dias_infectado: Dict[str, int] = None
    en_prep: bool = False
    viva: bool = True
    
    # Capa económica
    economia: EconomiaMujer = None

    # Capa embarazos
    embarazo_manager: EmbarazoManager = None
    embarazos_recientes: int = 0   # Para impacto temporal en salud/trabajo

    def __post_init__(self):
        patogenos = ['VIH', 'Clamidia', 'Gonorrea', 'Sífilis', 'Herpes']
        self.infectado = {p: False for p in patogenos}
        self.dias_infectado = {p: 0 for p in patogenos}
        self.economia = EconomiaMujer()
        
        self.embarazo_manager = EmbarazoManager()
        self.embarazos_recientes = 0

    def vulnerabilidad(self) -> float:
        base = (self.hijos * 0.28) + (1 - self.atractivo) * 0.25
        if self.es_viuda:
            base += 0.48
        # Más presión económica = más vulnerable
        if self.economia.deuda > 300:
            base += 0.25
        return min(1.0, base)