import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict, List
import json

class AnalisisEscenarios:
    """Análisis de sensibilidad y comparación de escenarios históricos"""
    
    def __init__(self, simulador_class):
        self.simulador_class = simulador_class

    def ejecutar_escenario(self, nombre: str, params_modificados: dict, num_mujeres=200, dias=365*12):
        """Ejecuta un escenario específico"""
        from models.parametros import ParametrosRiesgo
        
        params = ParametrosRiesgo()
        for key, value in params_modificados.items():
            if hasattr(params, key):
                setattr(params, key, value)
        
        sim = self.simulador_class(num_mujeres=num_mujeres, dias_sim=dias, params=params)
        print(f"Ejecutando escenario: {nombre}")
        sim.ejecutar()
        
        # Guardar resultados
        resultados = {
            "escenario": nombre,
            "prevalencia_final": {pat: sim.prevalencia[pat][-1] for pat in sim.prevalencia},
            "muertes_totales": sum(sim.muertes),
            "deuda_promedio_final": sim.balance_promedio[-1] if sim.balance_promedio else 0
        }
        
        with open(f"outputs/resultados_{nombre}.json", "w", encoding="utf-8") as f:
            json.dump(resultados, f, indent=2, ensure_ascii=False)
        
        return sim

    def comparar_escenarios(self):
        """Compara varios escenarios históricos"""
        escenarios = {
            "Pre_Guerra_1910": {"rechazo_pago_extra_prob": 0.78, "tasa_tratamiento_diaria": 0.05},
            "Post_WWI_1920": {"rechazo_pago_extra_prob": 0.45, "tasa_tratamiento_diaria": 0.04},   # Alta vulnerabilidad
            "Post_WWII_1950": {"rechazo_pago_extra_prob": 0.58, "tasa_tratamiento_diaria": 0.07},
            "Moderno_2000": {"rechazo_pago_extra_prob": 0.82, "tasa_tratamiento_diaria": 0.12}
        }
        
        resultados = {}
        for nombre, mods in escenarios.items():
            sim = self.ejecutar_escenario(nombre, mods)
            resultados[nombre] = {
                "VIH": sim.prevalencia['VIH'][-1],
                "Sífilis": sim.prevalencia['Sífilis'][-1],
                "Muertes": sum(sim.muertes),
                "Deuda_Final": sim.balance_promedio[-1]
            }
        
        # Crear tabla comparativa
        df = pd.DataFrame.from_dict(resultados, orient='index')
        df.to_csv("outputs/comparacion_escenarios.csv")
        print("\n=== TABLA COMPARATIVA ===")
        print(df)
        
        return df