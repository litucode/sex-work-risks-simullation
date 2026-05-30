**✅ Aquí tienes un README.md profesional, claro y bien estructurado** para tu proyecto:

---

```markdown
# Modelo Epidemiológico de ITS en Trabajo Sexual por Necesidad

**Simulación agent-based** de la dinámica de enfermedades de transmisión sexual (ITS) en mujeres que ejercen prostitución por necesidad económica, con enfoque en viudas y madres.

El modelo incorpora factores económicos, violencia de clientes, ciclos menstruales, embarazos no deseados, diferenciación entre **prostitución callejera** y **VIP**, y análisis de escenarios históricos (Francia 1900-2000 y contextos similares).

---

## 🎯 Objetivo del Proyecto

Estudiar de forma realista los mecanismos que aumentan la vulnerabilidad a ITS en mujeres que entran al trabajo sexual por necesidad (viudez por accidentes laborales o guerra, madres con hijos a cargo), evaluando el impacto de variables económicas, conductuales y estructurales.

---

## ✨ Características Principales

- Diferenciación clara entre **prostituta callejera** y **VIP**
- Violencia de clientes con impacto en salud y negociación
- Modelo económico detallado (alquiler, comida, belleza, costos de hijos)
- Feedback loops: deuda → mayor riesgo → más infecciones → más deuda
- Embarazos no deseados y su impacto económico
- Ciclos menstruales y multiplicadores biológicos
- Análisis de sensibilidad y escenarios históricos
- Generación automática de reportes en Word (.docx)

---

## 🛠 Tecnologías Utilizadas

- Python 3.9+
- NumPy, Matplotlib, NetworkX, Pandas
- python-docx (para reportes automáticos)

---

## 🚀 Instalación

1. Clona el repositorio:
   ```bash
   git clone <url-del-repositorio>
   cd ets-prostitucion
   ```

2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Ejecuta el modelo completo:
   ```bash
   python src/main.py
   ```

---

## 📁 Estructura del Proyecto

```
ets-prostitucion/
├── src/
│   ├── main.py
│   ├── simulador.py
│   ├── sensitivity.py
│   ├── validation.py
│   └── models/
│       ├── parametros.py
│       ├── mujer.py
│       ├── economia.py
│       ├── embarazo.py
│       ├── red.py
│       └── cliente.py
├── outputs/          ← Resultados, gráficos y reportes
├── requirements.txt
└── README.md
```

---

## ⚠️ Nota Ética e Importante

Este modelo es una herramienta **académica y de investigación**. Su objetivo es ayudar a comprender mejor los mecanismos de vulnerabilidad en el trabajo sexual por necesidad, **no estigmatizar** a las personas que lo ejercen.

Los resultados son simulaciones y deben interpretarse con cautela. No sustituyen estudios empíricos ni datos reales de campo.

---

## 🔗 Enlace al Hilo de Desarrollo

El desarrollo completo de este modelo se discutió paso a paso en el siguiente hilo:

→ **[Discusión y desarrollo detallado del modelo](https://grok.com/share/bGVnYWN5LWNvcHk_272ad376-4bbb-4152-89f8-077eefca34c2)**

*(Reemplaza este enlace con el link real del hilo cuando lo compartas)*

---

## Licencia

Este proyecto se distribuye bajo licencia **MIT**. Puedes usarlo para fines académicos y de investigación.

---
