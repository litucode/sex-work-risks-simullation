**Modelo epidemiológico ampliado para ITS en prostitución femenina**

Incluyo los elementos solicitados: **dinámica de clientes**, **ciclos menstruales**, **uso variable de condón**, **coinfecciones** y **tratamiento**. Propongo una estructura de modelo **híbrido** (compartimental + agent-based o simulación individual) implementable en Python (con NumPy/SciPy o librerías como `stochastic`/`epimodels`), R (`EpiModel`) o software especializado como NetLogo/GEM.

### 1. Estructura general del modelo

Usa un enfoque **SEIR modificado** por patógeno, con extensiones:

- **Estados por individuo** (para simulación agent-based recomendada):
  - Susceptible (S)
  - Expuesto (E, si aplica latencia)
  - Infectado sintomático/asintomático (I)
  - Recuperado/Tratado (R, con posible reinfección para curables)
  - Para VIH: agudo → crónico → suprimido (TARGA)

- **Múltiples patógenos** simulados en paralelo para **coinfecciones**.

**Parámetros clave (estimaciones basadas en literatura; calibrar con datos locales)**:

- **Dinámica de clientes**:
  - Número promedio de clientes/día: 2-6 (variable según contexto: calle, privado, etc.). Distribución Poisson o log-normal.
  - Prevalencia de ITS en clientes: usar datos locales (ej. VIH ~1-5% en clientes de alto riesgo en Argentina; sífilis/clamidia más alta).
  - Mezcla: clientes "fijos" vs. ocasionales (afecta reinfección y coinfecciones).

- **Ciclos menstruales**:
  - Ciclo de 28 días. Días de menstruación: 1-5/6.
  - Multiplicador de riesgo: **1.5-3x** durante menstruación (mayor inflamación, sangre facilita transmisión VIH/bacterianas).
  - Modelar fase folicular, ovulatoria y lútea con leves variaciones de susceptibilidad.

- **Uso variable de condón**:
  - Probabilidad por acto: p_condon = 0.6-0.9 (variable según negociación, cansancio, pago extra sin condón).
  - Eficacia: reduce riesgo 80-95% para fluidos (VIH, gonorrea, clamidia); menor (~50-70%) para piel-piel (herpes, VPH, sífilis).

- **Probabilidades de transmisión por acto vaginal (sin condón, mujer receptiva)**:
  - VIH: ~0.08-0.19% (aumenta con carga viral alta o coinfecciones).
  - Gonorrea/Clamidia: 20-50%.
  - Sífilis: alta si chancro.
  - Herpes (VHS-2): 10-30% si lesiones.
  - Ajustar por menstruación y coinfecciones.

**Riesgo diario aproximado**:
$$
P_{infección\ diaria} = 1 - \prod_{i=1}^{n} (1 - p_{trans} \times (1 - e_{condón}) \times m_{menstruación})
$$
donde n = clientes/día, m_menstruación = multiplicador.

### 2. Coinfecciones

Las coinfecciones aumentan transmisión:
- Úlceras (sífilis, herpes) → multiplican riesgo VIH por 2-5x.
- VIH → mayor susceptibilidad y transmisibilidad de otras ITS.
- Modelar con **matriz de interacción**: factor multiplicativo en probabilidad de adquisición/transmisión cuando ya infectada por otro patógeno.

Ejemplo: Prob_VIH | sífilis = Prob_VIH_base × 3.

### 3. Tratamiento y recuperación

- **Curables** (clamidia, gonorrea, sífilis, tricomoniasis):
  - Tasa de tratamiento: depende de acceso (chequeos mensuales → alta; estigma → baja).
  - Tiempo a tratamiento: 7-30 días.
  - Tasa de curación: >90% con antibióticos.
  - Reinfección posible inmediatamente.

- **Virales**:
  - VIH: TARGA → supresión viral (riesgo transmisión ≈0). Adherencia variable (50-80% en poblaciones vulnerables).
  - Herpes/VPH: manejo sintomático, no cura.
  - PrEP (profilaxis pre-exposición) como intervención.

Incluye **tasa de abandono** de tratamiento por presión económica o estigma.

### 4. Ecuaciones conceptuales (KaTeX)

Para modelo compartimental simplificado (por patógeno):

$$
\frac{dI}{dt} = \beta \cdot S \cdot C \cdot (1 - c) \cdot m \cdot (1 + \alpha \cdot Coinf) - (\gamma + \mu) I
$$

Donde:
- β = tasa transmisión base
- C = tasa contactos (clientes/día × prevalencia clientes)
- c = fracción condón efectiva
- m = multiplicador menstrual (promedio sobre ciclo)
- α = factor coinfección
- γ = tasa recuperación/tratamiento
- μ = mortalidad o salida

Para simulación individual: trackear estado menstrual, uso condón estocástico, etc.

### 5. Datos contextuales Argentina (aprox.)

Prevalencia en trabajadoras sexuales: VIH 2-6% (históricamente más alta en algunos grupos), sífilis y clamidia elevadas. En contextos de necesidad (viudas, madres), mayor vulnerabilidad por menor negociación de condón y más clientes.

### Recomendaciones para implementar

- **Simulación**: Agent-based para capturar heterogeneidad (edad, #hijos, ingresos, ciclo individual).
- **Escenarios**: Varía uso condón (intervención: +20% → impacto grande), frecuencia chequeos, apoyo económico (reduce #clientes).
- **Sensibilidad**: Analiza incertidumbre en parámetros.
- **Ética**: El modelo debe usarse para promover salud, prevención y alternativas económicas, no estigmatizar.
