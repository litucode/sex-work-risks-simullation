**✅ Modelo actualizado con las tres solicitudes**

### 1. ¿Qué es el Análisis de Sensibilidad?

El **Análisis de Sensibilidad** (Sensitivity Analysis) es una técnica que evalúa **cómo cambian los resultados del modelo** cuando se modifican los valores de los parámetros de entrada.  

Sirve para:
- Identificar qué variables son más influyentes (ej. ¿el uso de condón es más importante que el número de clientes?).
- Medir incertidumbre y robustez del modelo.
- Ayudar en la toma de decisiones (políticas de salud pública).

Existen dos tipos principales:
- **Univariate** (una variable a la vez)
- **Multivariate** (varias variables combinadas)

---

### 2. Cómo se ajusta al caso (prostitución femenina por necesidad)

En este contexto específico (mujeres viudas o madres que ejercen prostitución para alimentar a sus hijos), el análisis de sensibilidad es **muy útil** porque:

- Hay alta incertidumbre en parámetros reales (número real de clientes, adherencia a PrEP, negociación de condón bajo presión económica, acceso a tratamiento).
- Permite evaluar intervenciones: ¿qué impacto tiene aumentar el acceso a PrEP vs. mejorar el uso de condón vs. reducir número de clientes mediante apoyo económico?
- Ayuda a priorizar recursos en poblaciones vulnerables.

**Parámetros clave para analizar en este caso**:
- `CLIENTES_PROMEDIO`
- `P_CONDON_BASE`
- `P_ADHERENCIA_PREP` y `TASA_INICIO_PREP`
- `MULT_MENSTRUACION`
- Prevalencia en clientes

---

### 3. Código mejorado (incluye Análisis de Sensibilidad + Redes de Clientes)

```python
import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import List, Dict
import random
import networkx as nx   # Nueva dependencia para redes

# ====================== PARÁMETROS ======================
NUM_MUJERES = 200
DIAS_SIMULACION = 365 * 1.5

PATOGENOS = ['VIH', 'Clamidia', 'Gonorrea', 'Sífilis', 'Herpes']

TRANS_BASE = {'VIH': 0.001, 'Clamidia': 0.35, 'Gonorrea': 0.30, 'Sífilis': 0.25, 'Herpes': 0.15}
MULT_MENSTRUACION = 2.2
MULT_COINFECCION = 2.5
MULT_PREP = 0.01

P_CONDON_BASE = 0.75
EFICACIA_CONDON = 0.90
CLIENTES_PROMEDIO = 3.5

TASA_TRATAMIENTO_DIARIA = 0.08
P_ADHERENCIA_PREP = 0.65
TASA_INICIO_PREP = 0.03

MORTALIDAD_VIH_NO_TRATADO_ANUAL = 0.12
MORTALIDAD_GENERAL_ANUAL = 0.008

# ====================== CLASE MUJER ======================
@dataclass
class Mujer:
    id: int
    ciclo_dia: int = 0
    infectado: Dict[str, bool] = None
    dias_infectado: Dict[str, int] = None
    en_prep: bool = False
    hijos_a_cargo: int = random.randint(1, 4)
    uso_condon_hoy: float = P_CONDON_BASE
    viva: bool = True

    def __post_init__(self):
        self.infectado = {p: False for p in PATOGENOS}
        self.dias_infectado = {p: 0 for p in PATOGENOS}

# ====================== RED DE CLIENTES ======================
def crear_red_clientes(num_clientes=500, prob_conexion=0.08):
    """Crea una red de clientes con heterogeneidad (scale-free)"""
    G = nx.barabasi_albert_graph(num_clientes, 5)
    # Asignar prevalencia de ITS según grado (clientes más activos = mayor riesgo)
    prevalencia = {}
    for node in G.nodes():
        grado = G.degree(node)
        prevalencia[node] = {p: min(0.35, 0.08 + grado*0.015) if p == 'VIH' else min(0.45, 0.15 + grado*0.02) 
                           for p in PATOGENOS}
    return G, prevalencia

# ====================== SIMULACIÓN BASE ======================
def simular_escenario(parametros: dict = None):
    if parametros is None:
        parametros = {}
    
    # Aplicar parámetros variables
    clientes_prom = parametros.get('clientes', CLIENTES_PROMEDIO)
    p_condon = parametros.get('p_condon', P_CONDON_BASE)
    p_adherencia_prep = parametros.get('adherencia_prep', P_ADHERENCIA_PREP)
    
    mujeres = [Mujer(i) for i in range(NUM_MUJERES)]
    G_clientes, prev_clientes = crear_red_clientes()
    
    for dia in range(DIAS_SIMULACION):
        activas = [m for m in mujeres if m.viva]
        
        for mujer in activas:
            mujer.ciclo_dia = (mujer.ciclo_dia + 1) % 28
            es_menstruacion = 1 <= mujer.ciclo_dia <= 5
            
            if not mujer.en_prep and random.random() < TASA_INICIO_PREP:
                mujer.en_prep = True
                
            n_clientes = max(1, np.random.poisson(clientes_prom))
            
            mujer.uso_condon_hoy = max(0.3, min(0.95, p_condon + np.random.normal(0, 0.12)))
            
            for _ in range(n_clientes):
                cliente_id = random.choice(list(G_clientes.nodes()))
                for pat in PATOGENOS:
                    if mujer.infectado[pat]:
                        continue
                    if random.random() > prev_clientes[cliente_id][pat]:
                        continue
                        
                    p_trans = TRANS_BASE[pat]
                    if es_menstruacion: p_trans *= MULT_MENSTRUACION
                    if sum(mujer.infectado.values()) > 0: p_trans *= MULT_COINFECCION
                    if pat == 'VIH' and mujer.en_prep and random.random() < p_adherencia_prep:
                        p_trans *= MULT_PREP
                    if random.random() < mujer.uso_condon_hoy:
                        p_trans *= (1 - EFICACIA_CONDON)
                        
                    if random.random() < p_trans:
                        mujer.infectado[pat] = True
                        mujer.dias_infectado[pat] = 0
    
    # Resultado final (prevalencia VIH como ejemplo)
    mujeres_vivas = sum(1 for m in mujeres if m.viva)
    prev_vih = sum(1 for m in mujeres if m.viva and m.infectado['VIH']) / max(1, mujeres_vivas)
    return prev_vih

# ====================== ANÁLISIS DE SENSIBILIDAD ======================
def analisis_sensibilidad():
    print("Ejecutando Análisis de Sensibilidad...\n")
    
    escenarios = [
        {"nombre": "Base", "clientes": 3.5, "p_condon": 0.75, "adherencia_prep": 0.65},
        {"nombre": "Alta demanda", "clientes": 5.5, "p_condon": 0.75, "adherencia_prep": 0.65},
        {"nombre": "Mejor condón", "clientes": 3.5, "p_condon": 0.92, "adherencia_prep": 0.65},
        {"nombre": "Alta adherencia PrEP", "clientes": 3.5, "p_condon": 0.75, "adherencia_prep": 0.90},
        {"nombre": "Intervención combinada", "clientes": 2.8, "p_condon": 0.88, "adherencia_prep": 0.85},
    ]
    
    resultados = {}
    for esc in escenarios:
        prev = simular_escenario(esc)
        resultados[esc["nombre"]] = prev * 100
        print(f"{esc['nombre']:25}: Prevalencia VIH final ≈ {prev*100:5.2f}%")
    
    return resultados

# ====================== EJECUCIÓN ======================
if __name__ == "__main__":
    resultados = analisis_sensibilidad()
    
    # Gráfico de sensibilidad
    plt.figure(figsize=(10, 6))
    nombres = list(resultados.keys())
    valores = list(resultados.values())
    plt.bar(nombres, valores, color=['gray', 'red', 'green', 'blue', 'purple'])
    plt.title('Análisis de Sensibilidad - Prevalencia Final de VIH')
    plt.ylabel('Prevalencia VIH (%)')
    plt.xticks(rotation=15)
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.show()
```

### Cómo ejecutar

```bash
pip install numpy matplotlib networkx
python nombre_del_archivo.py
```

### Próximos pasos posibles

- Análisis de sensibilidad multivariado (Sobol, Morris)
- Exportar resultados a CSV
- Incluir costo económico de intervenciones
- Calibración con datos reales de Argentina
