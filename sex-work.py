import numpy as np
import matplotlib.pyplot as plt
import random
import networkx as nx
from dataclasses import dataclass
from typing import List, Dict

# ====================== PARÁMETROS CONFIGURABLES ======================
@dataclass
class ParametrosRiesgo:
    """Todos los comportamientos variables aquí"""
    # Negociación y condón
    p_condon_base: float = 0.75
    rechazo_pago_extra_prob: float = 0.68      # Probabilidad de rechazar pago extra sin condón
    prima_sin_condon: float = 1.8              # +80% de pago
    
    # Prácticas de alto riesgo
    prob_eyaculacion_facial: float = 0.28
    multiplicador_riesgo_facial: float = 1.65   # Mayor riesgo para gonorrea, clamidia, sífilis
    
    # Factores biológicos
    mult_menstruacion: float = 2.2
    mult_coinfeccion: float = 2.5
    mult_prep: float = 0.01                    # Reducción con PrEP (99%)
    
    # Adherencia y tratamiento
    adherencia_prep: float = 0.65
    tasa_tratamiento_diaria: float = 0.08
    eficacia_tratamiento: float = 0.92

    def ajustar_por_vulnerabilidad(self, vulnerabilidad: float):
        """Mujeres más vulnerables (viudas, más hijos) aceptan más riesgos"""
        self.rechazo_pago_extra_prob = max(0.25, 0.68 * (1 - vulnerabilidad * 0.55))


# ====================== CLASES ======================
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

    def __post_init__(self):
        self.infectado = {p: False for p in ['VIH', 'Clamidia', 'Gonorrea', 'Sífilis', 'Herpes']}
        self.dias_infectado = {p: 0 for p in self.infectado.keys()}

    def vulnerabilidad(self) -> float:
        base = (self.hijos * 0.28) + (1 - self.atractivo) * 0.25
        if self.es_viuda:
            base += 0.48
        return min(1.0, base)

class Cliente:
    def __init__(self, cid: int):
        self.id = cid
        self.tipo = random.choices(['regular', 'riesgo_alto', 'ocasional'], [0.4, 0.35, 0.25])[0]
        self.preferencia_madres = random.random() > 0.5
        self.riesgo_base = 0.65 if self.tipo == 'riesgo_alto' else 0.22

class RedPreferencias:
    def __init__(self, mujeres: List[Mujer], clientes: List[Cliente]):
        self.G = self._crear_red(mujeres, clientes)

    def _crear_red(self, mujeres, clientes) -> nx.Graph:
        G = nx.Graph()
        for m in mujeres:
            G.add_node(f"M{m.id}")
        for c in clientes:
            G.add_node(f"C{c.id}")
            for m in mujeres:
                score = m.atractivo * 0.4
                if c.preferencia_madres and m.hijos >= 2:
                    score += 0.45
                if m.es_viuda:
                    score += 0.35
                if random.random() < min(0.38, score):
                    G.add_edge(f"C{c.id}", f"M{m.id}")
        return G

# ====================== SIMULADOR CON LÓGICA COMPLETA ======================
class SimuladorEpidemiologico:
    def __init__(self, num_mujeres=300, dias_sim=365*30, params: ParametrosRiesgo = None):
        self.num_mujeres = num_mujeres
        self.dias_sim = dias_sim
        self.params = params or ParametrosRiesgo()
        
        self.mujeres = [Mujer(i) for i in range(num_mujeres)]
        self.clientes = [Cliente(i) for i in range(800)]
        self.red = RedPreferencias(self.mujeres, self.clientes)
        
        self.prevalencia = {p: [] for p in ['VIH', 'Clamidia', 'Gonorrea', 'Sífilis', 'Herpes']}
        self.muertes = []

    def _calcular_prob_transmision(self, mujer: Mujer, cliente: Cliente, sin_condon: bool, es_facial: bool) -> Dict[str, float]:
        probs = {}
        es_menstruacion = 1 <= mujer.ciclo_dia <= 5
        num_infecciones = sum(mujer.infectado.values())

        for pat in ['VIH', 'Clamidia', 'Gonorrea', 'Sífilis', 'Herpes']:
            p = {
                'VIH': 0.001,
                'Clamidia': 0.35,
                'Gonorrea': 0.30,
                'Sífilis': 0.27,
                'Herpes': 0.16
            }[pat]

            # Multiplicadores biológicos
            if es_menstruacion:
                p *= self.params.mult_menstruacion
            if num_infecciones > 0:
                p *= self.params.mult_coinfeccion

            # PrEP (solo VIH)
            if pat == 'VIH' and mujer.en_prep:
                if random.random() < self.params.adherencia_prep:
                    p *= self.params.mult_prep

            # Práctica de riesgo (facial/oral)
            if es_facial and pat in ['Clamidia', 'Gonorrea', 'Sífilis']:
                p *= self.params.multiplicador_riesgo_facial

            # Condón
            if not sin_condon:
                p *= (1 - 0.90)

            # Riesgo del cliente
            p *= (1 + cliente.riesgo_base)

            probs[pat] = max(0.0, min(1.0, p))
        
        return probs

    def simular_dia(self, dia: int):
        activas = [m for m in self.mujeres if m.viva]

        for mujer in activas:
            mujer.ciclo_dia = (mujer.ciclo_dia + 1) % 28
            self.params.ajustar_por_vulnerabilidad(mujer.vulnerabilidad())

            n_clientes = max(1, np.random.poisson(3.5 * (1.7 if mujer.es_viuda else 1.0)))

            for _ in range(n_clientes):
                # Seleccionar cliente de la red
                vecinos = list(self.red.G.neighbors(f"M{mujer.id}"))
                if not vecinos:
                    continue
                cliente_id = random.choice(vecinos).replace("C", "")
                cliente = next((c for c in self.clientes if c.id == int(cliente_id)), None)
                if not cliente:
                    continue

                # Decisión crítica: ¿acepta pago extra sin condón?
                acepta_sin_condon = random.random() > self.params.rechazo_pago_extra_prob
                es_facial = random.random() < self.params.prob_eyaculacion_facial

                probs = self._calcular_prob_transmision(mujer, cliente, acepta_sin_condon, es_facial)

                for pat, p_trans in probs.items():
                    if mujer.infectado[pat]:
                        continue
                    if random.random() < p_trans:
                        mujer.infectado[pat] = True
                        mujer.dias_infectado[pat] = 0

        # Evolución: tratamiento y mortalidad
        muertes_hoy = 0
        for mujer in activas[:]:
            for pat in list(mujer.infectado.keys()):
                if mujer.infectado[pat]:
                    mujer.dias_infectado[pat] += 1
                    
                    # Tratamiento
                    if random.random() < self.params.tasa_tratamiento_diaria * (1 + mujer.hijos * 0.1):
                        if random.random() < self.params.eficacia_tratamiento:
                            if pat not in ['VIH', 'Herpes']:
                                mujer.infectado[pat] = False

            # Mortalidad
            if mujer.infectado['VIH']:
                riesgo_muerte = 0.12 / 365 * (1 + mujer.dias_infectado['VIH']/500)
                if random.random() < riesgo_muerte:
                    mujer.viva = False
                    muertes_hoy += 1
                    continue

            if random.random() < 0.008 / 365:
                mujer.viva = False
                muertes_hoy += 1

        # Registrar prevalencia
        vivas = sum(1 for m in self.mujeres if m.viva)
        for pat in self.prevalencia.keys():
            prev = sum(1 for m in self.mujeres if m.viva and m.infectado[pat]) / max(1, vivas)
            self.prevalencia[pat].append(prev)
        
        self.muertes.append(muertes_hoy)

    def ejecutar(self):
        print("Iniciando simulación...")
        for dia in range(self.dias_sim):
            self.simular_dia(dia)
            if dia % 1000 == 0:
                print(f"Día {dia} completado...")

        self.mostrar_resultados()

    def mostrar_resultados(self):
        plt.figure(figsize=(14, 8))
        for pat, datos in self.prevalencia.items():
            plt.plot(datos, label=pat)
        
        plt.title('Evolución de Prevalencia de ITS - Modelo con Viudas y Madres')
        plt.xlabel('Días simulados')
        plt.ylabel('Prevalencia')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.show()

        vivas_final = sum(1 for m in self.mujeres if m.viva)
        print(f"\n=== RESULTADOS FINALES ===")
        print(f"Mujeres vivas: {vivas_final}/{self.num_mujeres} ({vivas_final/self.num_mujeres*100:.1f}%)")
        print(f"Muertes totales: {sum(self.muertes)}")
        for pat in self.prevalencia:
            print(f"{pat:12}: Prevalencia final = {self.prevalencia[pat][-1]*100:6.2f}%")

# ====================== EJECUCIÓN ======================
if __name__ == "__main__":
    params = ParametrosRiesgo(
        rechazo_pago_extra_prob=0.65,   # Más bajo = más riesgo (viudas)
        prob_eyaculacion_facial=0.30
    )
    
    sim = SimuladorEpidemiologico(num_mujeres=250, dias_sim=365*15, params=params)
    sim.ejecutar()