import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict
from simulador import SimuladorEpidemiologico
from models.parametros import ParametrosRiesgo

class AnalisisSensibilidad:
    """Análisis de sensibilidad y tabla de parámetros con fuentes"""
    
    def __init__(self):
        self.resultados = []

    def tabla_parametros(self):
        """Tabla profesional de parámetros calibrados"""
        data = {
            "Parámetro": [
                "p_vih", "p_clamidia", "p_gonorrea", "eficacia_condon",
                "mult_menstruacion", "mult_coinfeccion",
                "rechazo_pago_extra_prob", "prob_eyaculacion_facial",
                "tasa_tratamiento_diaria", "prob_embarazo_base"
            ],
            "Valor": [0.0008, 0.30, 0.28, 0.87, 2.0, 2.4, 0.68, 0.26, 0.085, 0.085],
            "Rango Sensible": ["0.0005-0.0012", "0.20-0.45", "0.20-0.40", "0.80-0.95", "1.5-3.0", "1.8-3.0", "0.25-0.85", "0.15-0.40", "0.04-0.15", "0.05-0.12"],
            "Fuente": [
                "CDC & Patel et al. 2014",
                "Meta-análisis ITS",
                "Meta-análisis ITS",
                "WHO & Cochrane",
                "Estudios ciclo menstrual",
                "Boily et al. coinfecciones",
                "Estudios negociación condón",
                "Estudios prácticas sexuales",
                "Acceso salud en poblaciones vulnerables",
                "Wilcox et al. fertilidad"
            ]
        }
        df = pd.DataFrame(data)
        df.to_csv("outputs/tabla_parametros.csv", index=False)
        print("\n=== TABLA DE PARÁMETROS CALIBRADOS ===")
        print(df)
        return df

    def analizar_sensibilidad(self, num_simulaciones=6):
        """Análisis univariado de las variables más críticas"""
        print("Ejecutando Análisis de Sensibilidad...\n")
        
        variables = {
            "Base": {},
            "Alta Vulnerabilidad": {"rechazo_pago_extra_prob": 0.38},
            "Baja Vulnerabilidad": {"rechazo_pago_extra_prob": 0.82},
            "Mejor Acceso Tratamiento": {"tasa_tratamiento_diaria": 0.15},
            "Alta Inflación/Economía": {"rechazo_pago_extra_prob": 0.45},
            "Mejor Uso Condón": {"rechazo_pago_extra_prob": 0.78}
        }
        
        resultados = {}
        
        for nombre, mods in variables.items():
            params = ParametrosRiesgo()
            for key, value in mods.items():
                if hasattr(params, key):
                    setattr(params, key, value)
            
            sim = SimuladorEpidemiologico(num_mujeres=180, dias_sim=365*10, params=params)
            sim.ejecutar()  # Ejecuta la simulación
            
            resultados[nombre] = {
                "VIH_Final": sim.prevalencia['VIH'][-1] * 100,
                "Sífilis_Final": sim.prevalencia['Sífilis'][-1] * 100,
                "Muertes_Totales": sum(sim.muertes),
                "Deuda_Promedio": sim.balance_promedio[-1]
            }
        
        df = pd.DataFrame.from_dict(resultados, orient='index')
        df.to_csv("outputs/sensibilidad_resultados.csv")
        
        # Gráfico comparativo
        fig, axs = plt.subplots(2, 2, figsize=(14, 10))
        df[['VIH_Final', 'Sífilis_Final']].plot(kind='bar', ax=axs[0,0])
        axs[0,0].set_title('Prevalencia Final ITS (%)')
        axs[0,0].set_ylabel('%')
        
        df['Muertes_Totales'].plot(kind='bar', ax=axs[0,1], color='darkred')
        axs[0,1].set_title('Muertes Totales')
        
        df['Deuda_Promedio'].plot(kind='bar', ax=axs[1,0], color='blue')
        axs[1,0].set_title('Deuda Promedio Final')
        
        plt.tight_layout()
        plt.savefig("outputs/grafico_sensibilidad.png")
        plt.show()
        
        print("\n=== RESULTADOS ANÁLISIS DE SENSIBILIDAD ===")
        print(df.round(3))
        return df