from dataclasses import dataclass

@dataclass
class ParametrosRiesgo:
    """Parámetros variables - Fácil de modificar"""
    p_condon_base: float = 0.75
    rechazo_pago_extra_prob: float = 0.68
    prob_eyaculacion_facial: float = 0.28
    mult_menstruacion: float = 2.2
    mult_coinfeccion: float = 2.5
    mult_prep: float = 0.01
    adherencia_prep: float = 0.65
    tasa_tratamiento_diaria: float = 0.08

    def ajustar_por_vulnerabilidad(self, vulnerabilidad: float):
        """Ajusta el rechazo a riesgos según vulnerabilidad económica"""
        # Más vulnerable → menos rechazo a pago extra sin condón
        factor = 1 - (vulnerabilidad * 0.55)
        self.rechazo_pago_extra_prob = max(0.25, self.rechazo_pago_extra_prob * factor)