import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from simulador import SimuladorEpidemiologico
from analysis import AnalisisEscenarios

if __name__ == "__main__":
    # Opción 1: Simulación individual
    # sim = SimuladorEpidemiologico(num_mujeres=180, dias_sim=365*12)
    # sim.ejecutar()

    # Opción 2: Análisis de escenarios (Recomendado ahora)
    analisis = AnalisisEscenarios(SimuladorEpidemiologico)
    analisis.comparar_escenarios()

    print("\nResultados guardados en carpeta 'outputs/'")