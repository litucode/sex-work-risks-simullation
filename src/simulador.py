import numpy as np
import matplotlib.pyplot as plt
import random
from typing import List

from models.mujer import Mujer
from models.parametros import ParametrosRiesgo
from models.economia import EntornoEconomico
from models.embarazo import EmbarazoManager
from models.red import RedPreferencias


class SimuladorEpidemiologico:
    def __init__(self, num_mujeres=250, dias_sim=365*15, params=None):
        self.num_mujeres = num_mujeres
        self.dias_sim = dias_sim
        self.params = params or ParametrosRiesgo()
        self.entorno = EntornoEconomico(ano_base=1910)
        
        self.mujeres: List[Mujer] = [Mujer(i) for i in range(num_mujeres)]
        self.red = RedPreferencias(self.mujeres)
        
        self.prevalencia = {p: [] for p in ['VIH', 'Clamidia', 'Gonorrea', 'Sífilis', 'Herpes']}
        self.muertes = []
        self.balance_promedio = []

    def ejecutar(self):
        print("🚀 Iniciando simulación completa con red, economía y embarazos...")
        for dia in range(self.dias_sim):
            self._simular_dia(dia)
            
            if dia % 2000 == 0 and dia > 0:
                print(f"   Día {dia} completado | Año aprox: {self.entorno.ano}")

        self.mostrar_resultados()

    def _simular_dia(self, dia: int):
        activas = [m for m in self.mujeres if m.viva]

        for mujer in activas:
            mujer.ciclo_dia = (mujer.ciclo_dia + 1) % 28
            
            # Lógica económica y vulnerabilidad
            vulnerabilidad = mujer.vulnerabilidad()
            self.params.ajustar_por_vulnerabilidad(vulnerabilidad)

            multiplicador_economico = 1.0
            if mujer.economia.deuda > 200:
                multiplicador_economico = 1.8
            elif mujer.hijos >= 4:
                multiplicador_economico = 1.45

            # Selección de clientes mediante red
            vecinos = list(self.red.G.neighbors(f"M{mujer.id}"))
            n_clientes = max(1, np.random.poisson(3.5 * multiplicador_economico * (1.7 if mujer.es_viuda else 1.0)))

            ingresos_hoy = 0.0

            for _ in range(n_clientes):
                if not vecinos:
                    continue
                cliente_id_str = random.choice(vecinos)
                cliente = next((c for c in self.red.clientes if f"C{c.id}" == cliente_id_str), None)
                if not cliente:
                    continue

                acepta_sin_condon = random.random() > self.params.rechazo_pago_extra_prob
                es_facial = random.random() < self.params.prob_eyaculacion_facial

                # Pago
                pago = 25.0
                if acepta_sin_condon:
                    pago *= 1.85
                ingresos_hoy += pago

                # Transmisión de patógenos
                for pat in list(mujer.infectado.keys()):
                    if mujer.infectado[pat]:
                        continue
                    p = self._prob_transmision(pat, mujer, acepta_sin_condon, es_facial)
                    if random.random() < p:
                        mujer.infectado[pat] = True
                        mujer.dias_infectado[pat] = 0

                # Embarazo no deseado
                if acepta_sin_condon:
                    balance_aprox = mujer.economia.balance_mensual(
                        ingresos_hoy * 30, self.entorno.get_inflacion(), mujer.hijos
                    )
                    if mujer.embarazo_manager.intentar_embarazo(mujer, acepta_sin_condon, es_facial, balance_aprox):
                        mujer.hijos += 1
                        mujer.embarazos_recientes += 1

            # Actualizar economía
            balance = mujer.economia.balance_mensual(
                ingresos_hoy * 30, self.entorno.get_inflacion(), mujer.hijos
            )
            if balance < 0:
                mujer.economia.deuda += abs(balance) * 0.75

        # Actualizar entorno y red
        self.entorno.actualizar(1)
        if dia % 90 == 0:
            self.red.actualizar(self.mujeres)

        # Salud y mortalidad
        self._actualizar_salud_y_mortalidad(activas)

        # Estadísticas
        self._actualizar_estadisticas()

    def _prob_transmision(self, pat: str, mujer: Mujer, sin_condon: bool, es_facial: bool) -> float:
        """Probabilidad calibrada según literatura"""
        probs_base = {
            'VIH': self.params.p_vih,
            'Clamidia': self.params.p_clamidia,
            'Gonorrea': self.params.p_gonorrea,
            'Sífilis': self.params.p_sifilis,
            'Herpes': self.params.p_herpes
        }
        p = probs_base[pat]

        # Factores biológicos
        if 1 <= mujer.ciclo_dia <= 5:                    # Menstruación
            p *= self.params.mult_menstruacion
        if sum(mujer.infectado.values()) > 0:           # Coinfección
            p *= self.params.mult_coinfeccion

        # PrEP (solo VIH)
        if pat == 'VIH' and mujer.en_prep and random.random() < self.params.adherencia_prep:
            p *= self.params.mult_prep

        # Práctica de alto riesgo
        if es_facial and pat in ['Clamidia', 'Gonorrea', 'Sífilis']:
            p *= self.params.multiplicador_riesgo_facial

        # Condón
        if not sin_condon:
            p *= (1 - self.params.eficacia_condon)

        return max(0.0, min(1.0, p))

    def _actualizar_salud_y_mortalidad(self, activas):
        for mujer in activas[:]:
            for pat in list(mujer.infectado.keys()):
                if mujer.infectado[pat]:
                    mujer.dias_infectado[pat] += 1
                    if random.random() < self.params.tasa_tratamiento_diaria * (1 + mujer.hijos * 0.08):
                        if random.random() < 0.92 and pat not in ['VIH', 'Herpes']:
                            mujer.infectado[pat] = False

            # Mortalidad
            if mujer.infectado['VIH']:
                riesgo = 0.12 / 365 * (1 + mujer.dias_infectado['VIH']/600)
                if random.random() < riesgo:
                    mujer.viva = False
                    continue

            if random.random() < 0.008 / 365:
                mujer.viva = False

            # Reducir embarazos recientes
            if mujer.embarazos_recientes > 0 and random.random() < 0.08:
                mujer.embarazos_recientes = max(0, mujer.embarazos_recientes - 1)

    def _actualizar_estadisticas(self):
        vivas = sum(1 for m in self.mujeres if m.viva)
        for pat in self.prevalencia:
            prev = sum(1 for m in self.mujeres if m.viva and m.infectado[pat]) / max(1, vivas)
            self.prevalencia[pat].append(prev)
        
        deuda_prom = np.mean([m.economia.deuda for m in self.mujeres])
        self.balance_promedio.append(deuda_prom)

    def mostrar_resultados(self):
        fig, axs = plt.subplots(2, 2, figsize=(14, 10))
        
        for pat, datos in self.prevalencia.items():
            axs[0, 0].plot(datos, label=pat)
        axs[0, 0].set_title('Prevalencia de ITS')
        axs[0, 0].legend()
        axs[0, 0].grid(True, alpha=0.3)

        axs[0, 1].plot(np.cumsum(self.muertes), color='darkred')
        axs[0, 1].set_title('Muertes Acumuladas')

        axs[1, 0].plot(self.balance_promedio, color='blue')
        axs[1, 0].set_title('Deuda Promedio')

        plt.tight_layout()
        plt.show()

        vivas = sum(m.viva for m in self.mujeres)
        print("\n=== RESULTADOS FINALES ===")
        print(f"Mujeres vivas: {vivas}/{self.num_mujeres} ({vivas/self.num_mujeres*100:.1f}%)")
        print(f"Muertes totales: {sum(self.muertes)}")
        for pat in self.prevalencia:
            print(f"{pat:12}: {self.prevalencia[pat][-1]*100:6.2f}%")
        print(f"Deuda promedio final: {self.balance_promedio[-1]:.1f}")