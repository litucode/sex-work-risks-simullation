from dataclasses import dataclass
import random

@dataclass
class EmbarazoManager:
    """Manejo de embarazos no deseados y fertilidad"""
    prob_embarazo_base: float = 0.085          # Por acto de alto riesgo (sin condón)
    probabilidad_aborto_espontaneo: float = 0.15
    decision_continuar_embarazo: float = 0.68   # Influida por situación económica

    def intentar_embarazo(self, mujer, sin_condon: bool, es_facial: bool, balance_economico: float) -> bool:
        if not sin_condon:
            return False

        # Mayor probabilidad en fase ovulatoria aproximada
        prob = self.prob_embarazo_base
        if 12 <= mujer.ciclo_dia <= 16:   # Ventana fértil aproximada
            prob *= 2.2

        if es_facial:
            prob *= 1.2

        if random.random() < prob:
            # Presión económica influye en continuar el embarazo
            factor_pobreza = max(0.45, 1.0 - (balance_economico / -800))  # Más deuda = más probable continuar
            if random.random() < self.decision_continuar_embarazo * factor_pobreza:
                return True
        return False