from dataclasses import dataclass

@dataclass
class EconomiaMujer:
    """Gestión económica individual de cada mujer"""
    ingresos_acumulados: float = 0.0
    deuda: float = 0.0
    pension_mensual: float = 45.0      # Francos históricos
    costo_vida_base: float = 120.0     # Costo mensual base
    costo_por_hijo: float = 28.0

    def calcular_gastos_mensuales(self, inflacion: float = 1.0, num_hijos: int = 0) -> float:
        """Gastos totales ajustados por inflación"""
        return (self.costo_vida_base * inflacion) + (num_hijos * self.costo_por_hijo)

    def balance_mensual(self, ingresos_mes: float, inflacion: float = 1.0, num_hijos: int = 0) -> float:
        """Calcula balance mensual"""
        gastos = self.calcular_gastos_mensuales(inflacion, num_hijos)
        interes_deuda = self.deuda * 0.02
        return ingresos_mes - gastos - interes_deuda


class EntornoEconomico:
    """Maneja inflación y contexto histórico"""
    def __init__(self, ano_base: int = 1910):
        self.ano = ano_base
        self.indice_inflacion = 1.0

    def actualizar(self, dias: int):
        """Simula inflación histórica Francia"""
        self.ano += dias // 365
        if 1914 <= self.ano <= 1925:      # Post Primera Guerra
            self.indice_inflacion *= 1.085
        elif 1939 <= self.ano <= 1950:    # Post Segunda Guerra
            self.indice_inflacion *= 1.065
        else:
            self.indice_inflacion *= 1.018   # Inflación moderada

    def get_inflacion(self) -> float:
        return self.indice_inflacion