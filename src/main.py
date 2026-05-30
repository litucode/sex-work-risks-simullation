import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from simulador import SimuladorEpidemiologico
from sensitivity import AnalisisSensibilidad
from validation import ValidacionModelo

if __name__ == "__main__":
    print("=== INICIANDO ANÁLISIS COMPLETO DEL MODELO ===\n")
    
    # 1. Análisis de sensibilidad
    analisis = AnalisisSensibilidad()
    analisis.tabla_parametros()
    analisis.analizar_sensibilidad()
    
    # 2. Validación y análisis cualitativo
    sim = SimuladorEpidemiologico(num_mujeres=150, dias_sim=365*8)
    validador = ValidacionModelo(sim)
    validador.validar_modelo()
    validador.analisis_cualitativo()
    validador.generar_reporte_final()
    
    print("\n🎉 ¡Proyecto completado exitosamente!")
    print("Revisa la carpeta 'outputs/' para todos los resultados.")