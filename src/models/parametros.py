from dataclasses import dataclass

@dataclass
class ParametrosRiesgo:
    """Parámetros calibrados según literatura científica (CDC, WHO, meta-análisis)"""
    
    # ==================== TRANSMISIÓN ====================
    # Probabilidades base por acto vaginal (mujer receptiva, sin condón)
    p_vih: float = 0.0008          # 0.08% - CDC & Patel et al. (2014)
    p_clamidia: float = 0.30       # 20-50% según pareja infectada
    p_gonorrea: float = 0.28
    p_sifilis: float = 0.25
    p_herpes: float = 0.16

    # ==================== MULTIPLICADORES ====================
    mult_menstruacion: float = 2.0         # Evidencia moderada (1.5-3x)
    mult_coinfeccion: float = 2.4          # Úlceras facilitan transmisión
    mult_prep: float = 0.01                # 99% eficacia con buena adherencia
    eficacia_condon: float = 0.87          # Más realista (80-95%)

    # ==================== COMPORTAMIENTO ====================
    rechazo_pago_extra_prob: float = 0.68
    prob_eyaculacion_facial: float = 0.26
    multiplicador_riesgo_facial: float = 1.6

    # ==================== SALUD Y TRATAMIENTO ====================
    adherencia_prep: float = 0.65
    tasa_tratamiento_diaria: float = 0.085
    eficacia_tratamiento: float = 0.92

    # ==================== VIOLENCIA ====================
    prob_violencia_callejera: float = 0.08      # por cliente
    prob_violencia_vip: float = 0.018
    impacto_violencia: float = 0.35             # reduce rechazo y aumenta deuda

    # ==================== Comportamiento ====================
    rechazo_pago_extra_prob: float = 0.68
    prob_eyaculacion_facial: float = 0.26

    def ajustar_por_vulnerabilidad(self, vulnerabilidad: float):
        """Ajuste gradual según presión económica"""
        factor = max(0.28, 1 - (vulnerabilidad * 0.48))
        self.rechazo_pago_extra_prob = max(0.25, self.rechazo_pago_extra_prob * factor)