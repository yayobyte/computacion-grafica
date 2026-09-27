# Taller 7 — Aproximación de Funciones con Series de Taylor en Python

Ruta sugerida: [← Unidad 2](../) | [Inicio](../../)

## Objetivo

Desarrollar versiones propias de las funciones **exponencial, seno, coseno, tangente y logaritmo natural** mediante series de Taylor. Luego se grafican todas en un mismo subplot, se comparan con NumPy y se evalúa cómo cambia el error al aumentar el número de términos.

- **Alineación:** RAA1 (modelación numérica), RAA5 (análisis técnico), RAA6 (exploración autónoma).
- **Valor:** 0,0 a 5,0 · trabajo individual · ~4 horas.
- **Evaluación del enunciado:** precisión frente a NumPy, correcta visualización de las gráficas y participación en el análisis de resultados.

## Conceptos clave

- **Serie de Taylor:** $f(x) = \sum \frac{f^{(n)}(x_0)}{n!}(x - x_0)^n$. Cuando $x_0 = 0$ se llama **serie de Maclaurin**. Al truncarla en $N$ términos se obtiene un polinomio $P_N(x)$.
- **Error absoluto:** $E_N(x) = |f(x) - P_N(x)|$.
- **Radio de convergencia:** $e^x$, $\sin$ y $\cos$ convergen en todo $\mathbb{R}$. $\tan$ solo converge en $|x| < \pi/2$, y $\ln$ (centrada en $x_0 = 1$) solo en $(0, 2]$.
- **Términos vs. puntos:** el número de términos $N$ define la **precisión**. El número de puntos de muestreo solo define la **resolución** de la gráfica.
- **Números de Bernoulli:** son los coeficientes que necesita la serie de $\tan(x)$.

## Estado

- [x] Código base de clase transcrito
- [x] Series de exp, sin, cos, tan y ln con número configurable de términos
- [x] Las cinco funciones en un mismo subplot (figura 1)
- [x] Detalle por función: real vs. 3 aproximaciones + error absoluto (figuras 2 a 6)
- [x] Precisión frente a NumPy impresa en consola
- [x] Conclusión técnica (8 líneas) al final del `.py`
- [x] Explicación línea a línea
- [ ] Revisado y entregado en Moodle

## Archivos de esta carpeta

| Archivo | Descripción |
| --- | --- |
| [`taller_7_otras_funciones.py`](./taller_7_otras_funciones.py) | **Entregable.** Series de $e^x$, $\sin$, $\cos$, $\tan$ y $\ln$. Grafica las cinco en un mismo subplot, más una figura por función con $N = 2, 4, 8$ términos, 5, 10 y 50 puntos, y el error absoluto en escala log. |
| [`codigo_base_clase.py`](./codigo_base_clase.py) | Transcripción del código visto en clase: sin(x) por tolerancia y comparación de 5, 10 y 50 puntos. |
| [`explicacion_linea_por_linea.md`](./explicacion_linea_por_linea.md) | Explicación pedagógica del entregable, resultados y preguntas de sustentación. |

## Cómo ejecutar

Desde la raíz del repositorio, con el entorno virtual activo (ver [README principal](../../README.md#️-requisitos-técnicos-y-ejecución)):

```bash
python3 unidad-2-modelado-y-transformaciones/taller-7-series-de-taylor/taller_7_otras_funciones.py
```

Se abren **6 figuras**:

1. Las cinco funciones reales vs. Taylor en un mismo subplot.
2. A 6. El detalle de exp, sin, cos, tan y ln.

La consola imprime el error máximo frente a NumPy para cada función y número de términos.

## Antes de entregar

- [ ] Ejecutar el archivo desde cero y comprobar que no hay errores.
- [ ] Poder explicar y modificar cualquier línea (ver [preguntas de sustentación](./explicacion_linea_por_linea.md#4-preguntas-que-te-pueden-hacer-en-la-sustentación)).
- [ ] Revisar en Moodle la fecha y las condiciones de entrega.
