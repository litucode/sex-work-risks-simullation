from dataclasses import dataclass
import random

@dataclass
class EmbarazoManager:
    """Manejo de embarazos no deseados y fertilidad"""
    prob_embarazo_base: float = 0.085          # Por acto de alto riesgo (sin condón)
    probabilidad_aborto_espontaneo: float = 0.15
    decision_continuar_embarazo: float = 0.68   # Influida por situación económica

    def intentar_embarazo(self, mujer, sin_condon: bool, es_facial: bool, balance_economico: float) -> bool:
        """Intenta embarazo y devuelve si se produjo uno que continuó"""
        if not sin_condon:
            return False  # Con condón el riesgo es muy bajo

        # Mayor riesgo si eyaculación facial o acto de alto riesgo
        prob = self.prob_embarazo_base
        if es_facial:
            prob *= 1.25

        if random.random() < prob:
            # Decisión de continuar el embarazo (presión económica)
            factor_economico = max(0.4, 1.0 - (balance_economico / 1000))  # Más deuda = más probable continuar
            if random.random() < self.decision_continuar_embarazo * factor_economico:
                return True  # Embarazo que continúa
        return False