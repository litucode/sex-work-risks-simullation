from dataclasses import dataclass

@dataclass
class EconomiaMujer:
    """Gestión económica individual según tipo de trabajo"""
    tipo_trabajo: str = "callejera"
    ingresos_acumulados: float = 0.0
    deuda: float = 0.0
    alquiler: float = 0.0
    comida: float = 0.0
    belleza: float = 0.0
    costo_hijos: float = 0.0

    def __post_init__(self):
        if self.tipo_trabajo == "callejera":
            self.alquiler = 85
            self.comida = 110
            self.belleza = 25
            self.costo_hijos = 32
        else:  # VIP
            self.alquiler = 220
            self.comida = 95
            self.belleza = 95
            self.costo_hijos = 45

    def gastos_mensuales(self, inflacion: float = 1.0, num_hijos: int = 0) -> float:
        return (self.alquiler + self.comida + self.belleza) * inflacion + (num_hijos * self.costo_hijos)

    def balance_mensual(self, ingresos_mes: float, inflacion: float = 1.0, num_hijos: int = 0) -> float:
        gastos = self.gastos_mensuales(inflacion, num_hijos)
        return ingresos_mes - gastos - (self.deuda * 0.025)


class EntornoEconomico:
    """Manejo de inflación y contexto histórico"""
    def __init__(self, ano_base: int = 1910):
        self.ano = ano_base
        self.indice_inflacion = 1.0

    def actualizar(self, dias: int):
        self.ano += dias // 365
        if 1914 <= self.ano <= 1925:      # Post WWI
            self.indice_inflacion *= 1.085
        elif 1939 <= self.ano <= 1950:    # Post WWII
            self.indice_inflacion *= 1.065
        else:
            self.indice_inflacion *= 1.018

    def get_inflacion(self) -> float:
        return self.indice_inflacion