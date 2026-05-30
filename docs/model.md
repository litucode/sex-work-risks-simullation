**Taxonomía principal de las Enfermedades de Transmisión Sexual (ETS/ITS)**

Las ITS se clasifican principalmente por el agente causal: bacterias, virus y parásitos. Según la OMS, hay más de 30 patógenos, pero ocho causan la mayor incidencia.

### Bacterianas (curables con antibióticos):
- **Clamidia** (*Chlamydia trachomatis*): Muy común, a menudo asintomática.
- **Gonorrea** (*Neisseria gonorrhoeae*): Puede causar secreciones y complicaciones.
- **Sífilis** (*Treponema pallidum*): Etapas primaria (chancro), secundaria y terciaria.

### Virales (generalmente incurables, controlables):
- **VIH**: Causa SIDA si no se trata.
- **Herpes genital** (VHS-2 principalmente): Úlceras recurrentes.
- **VPH** (Virus del Papiloma Humano): Verrugas y riesgo de cáncer cervical.
- **Hepatitis B**: Afecta el hígado.

### Parasitarias:
- **Tricomoniasis** (*Trichomonas vaginalis*): Secreción y picazón.

Otras: ladillas, sarna, etc. Muchas son asintomáticas, especialmente en mujeres, lo que facilita la transmisión inadvertida.

**Probabilidades de transmisión por acto sexual vaginal (estimaciones aproximadas, sin condón)**

Las probabilidades **per act** (por encuentro) varían mucho según:
- Carga viral/bacteriana del infectado.
- Presencia de otras ITS (úlceras facilitan entrada).
- Uso de condón (reduce drásticamente el riesgo).
- Tipo de acto (vaginal es menor riesgo que anal).

**Estimaciones aproximadas (mujer receptiva, sin condón, pareja infectada)**:
- **VIH**: ~0.08% por acto vaginal receptivo (bajo, pero se acumula con múltiples exposiciones).
- **Gonorrea y Clamidia**: Más altas, alrededor del 20-50% por acto con pareja infectada (depende de factores).
- **Sífilis**: Alta si hay chancro (úlceras).
- **Herpes**: 10-30% por acto si hay lesiones activas (transmisión piel a piel).
- **VPH y Tricomoniasis**: Altamente transmisibles por contacto.

Con condón correcto y consistente: reducción del 80-95% para la mayoría (no 100%, especialmente herpes/VPH). El sexo oral tiene riesgos menores para VIH pero altos para gonorrea/clamidia/sífilis/herpes.

**Efecto de la menstruación**

La menstruación **aumenta el riesgo de transmisión** en ambos sentidos:
- Sangre menstrual puede transportar virus (VIH, Hepatitis B) o facilitar bacterias.
- Cambios hormonales reducen inmunidad local en la vagina/cérvix.
- Mayor inflamación y exposición de tejidos.
- Estudios asocian sexo durante la regla con mayor riesgo de VIH y otras ITS.

En un modelo, los días de menstruación (generalmente 4-6 por ciclo) deberían tener un multiplicador de riesgo (ej. 1.5-3x según literatura), especialmente para VIH y bacterianas.

**Modelado epidemiológico simple para prostitución femenina**

Para un modelo básico (tipo compartimental SIR o individual-based), considera:

1. **Tasa de contactos**: Promedio de clientes/día en trabajadoras sexuales varía (1-10+ según contexto, ubicación, tipo de trabajo). En algunos estudios, 3-5 por día es común; en contextos de alta demanda, más.

2. **Probabilidad diaria de infección**:
   - Asume prevalencia en clientes (ej. VIH 1-5% en poblaciones generales de alto riesgo; mayor en grupos específicos).
   - Probabilidad por cliente = prevalencia × prob. transmisión per act.
   - Diaria = 1 - (1 - p_por_cliente)^n (n = clientes/día).
   - Separa menstruación: multiplica p en esos días.

**Ejemplo simplificado (VIH, sin condón, prevalencia clientes 2%)**:
- p_per_act ≈ 0.0008 (0.08%).
- 4 clientes/día normal: riesgo diario bajo (~0.0064), pero acumulado mensual/anual significativo.
- Días de menstruación: riesgo ×2 → más alto.

Con condón consistente: riesgo cae drásticamente. Factores protectores: PrEP (para VIH), chequeos regulares, tratamiento inmediato (para curables).

**Contexto del objetivo: mujeres en prostitución por necesidad (viudas, madres)**

Este grupo enfrenta riesgos elevados por:
- Presión económica → menos negociación de condón, más clientes.
- Menor acceso a salud, estigma, violencia.
- Mayor vulnerabilidad social (bajos ingresos, hijos a cargo).

Estudios en trabajadoras sexuales muestran prevalencias variables de ITS (bajas para VIH en algunos países latinoamericanos con programas, pero altas para clamidia/VPH). Modelos destacan que intervenciones estructurales (educación, condones gratuitos, empoderamiento económico, chequeos accesibles) reducen incidencia más que solo biomédicas.

**Recomendaciones para tu modelo**:
- Usa software como R, Python (con paquetes epi) o NetLogo para simulaciones.
- Incorpora: dinámica de clientes, ciclos menstruales, uso condón variable, coinfecciones, tratamiento.
- Datos locales (Argentina/Buenos Aires): consulta ministerio de salud para prevalencias.
- Enfoque ético: prioriza derechos humanos, salida de la prostitución vía apoyo social/económico, no estigmatización.
