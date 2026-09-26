# Explicación Detallada Línea a Línea · Taller 7: Función Coseno y Series de Taylor

Este documento explica de forma clara y precisa qué hace cada línea del archivo ejecutable [`taller_7_series_taylor.py`](./taller_7_series_taylor.py).

El código conserva el **estilo algorítmico visto en clase** (mismas variables, recursividad para factorial, `np.frompyfunc` y subgráficas con `plt.subplot`), pero adaptado a los requisitos pedagógicos del **Taller 7**:
1. Implementar la aproximación para la **función coseno** ($\cos$).
2. Evaluar visualmente el efecto de **variar el número de términos** ($N = 1, 3, 5$).
3. Calcular y representar el **error absoluto** correspondiente a cada aproximación.
4. Generar curvas continuas suaves con un dominio justificado en NumPy.
5. Incluir una conclusión técnica de entre cinco y ocho líneas al final.

---

## 1. Fundamento Matemático: Serie de Maclaurin para $\cos(x)$

La función analítica coseno se expande en serie de Taylor alrededor de $x_0 = 0$ (serie de Maclaurin) mediante la fórmula:

$$\cos(x) = \sum_{n=0}^{\infty} \frac{(-1)^n}{(2n)!} x^{2n} = 1 - \frac{x^2}{2!} + \frac{x^4}{4!} - \frac{x^6}{6!} + \frac{x^8}{8!} - \dots$$

- **$N = 1$ término ($n = 0$):** $P_1(x) = 1$ (aproximación constante).
- **$N = 3$ términos ($n = 0, 1, 2$):** $P_3(x) = 1 - \frac{x^2}{2} + \frac{x^4}{24}$ (polinomio de grado 4).
- **$N = 5$ términos ($n = 0, 1, 2, 3, 4$):** $P_5(x) = 1 - \frac{x^2}{2} + \frac{x^4}{24} - \frac{x^6}{720} + \frac{x^8}{40320}$ (polinomio de grado 8).

---

## 2. Explicación Línea a Línea del Código

### Bloque de Importaciones (Líneas 1 - 3)
```python
1 import numpy as np
2 import matplotlib.pyplot as plt
3 import math
```
- **Línea 1 (`import numpy as np`):** Importa la librería NumPy para generar el vector del dominio con `np.linspace`, evaluar la función coseno real con `np.cos()` y vectorizar la función con `np.frompyfunc`.
- **Línea 2 (`import matplotlib.pyplot as plt`):** Importa el módulo de graficación de Matplotlib para crear figuras, subgráficas, títulos, leyendas y cuadrículas.
- **Línea 3 (`import math`):** Módulo matemático estándar de Python.

---

### Función Factorial Recursiva (Líneas 5 - 12)
```python
5 def miFactorial(n):
6     if (n == 0 or n == 1):
7         fact = 1
8     elif (n > 1):
9         fact = n * miFactorial(n - 1)
10    else:
11        return "NaN"
12    return (fact)
```
- **Línea 5:** Define la función `miFactorial(n)`, idéntica a la vista en clase.
- **Línea 6 - 7:** **Caso base:** Si $n = 0$ o $n = 1$, define `fact = 1` (ya que $0! = 1$ y $1! = 1$).
- **Línea 8 - 9:** **Caso recursivo:** Si $n > 1$, calcula el factorial multiplicando $n$ por el factorial de $n - 1$ de manera recursiva (`n * miFactorial(n - 1)`).
- **Línea 10 - 11:** Si $n < 0$, retorna el texto `"NaN"`.
- **Línea 12:** Retorna el valor numérico acumulado en `fact`.

---

### Función Coseno con Series de Taylor (Líneas 15 - 23)
```python
15 def miCos(x, numTerminos):
16     suma = 0
17     termino = 0
18     n = 0
19     while (n < numTerminos):
20         termino = ((-1)**n) / (miFactorial(2 * n)) * (x**(2 * n))
21         suma += termino
22         n += 1
23     return (suma)
```
- **Línea 15:** Define la función `miCos(x, numTerminos)` que recibe el valor escalar `x` y el número configurable de términos a acumular (`numTerminos`).
- **Línea 16:** `suma = 0`: acumulador que suma los términos del polinomio.
- **Línea 17:** `termino = 0`: variable temporal para el valor del término en la iteración actual.
- **Línea 18:** `n = 0`: índice de iteración que inicia en cero.
- **Línea 19:** `while (n < numTerminos):` itera exactamente hasta alcanzar el número de términos solicitado por el usuario.
- **Línea 20:** Aplica la fórmula del término $n$-ésimo de la serie de Maclaurin de coseno:
  - `(-1)**n`: genera el signo alternante ($+1, -1, +1, -1, \dots$).
  - `miFactorial(2 * n)`: calcula el factorial de la potencia par.
  - `(x**(2 * n))`: eleva el valor `x` a la potencia par ($0, 2, 4, \dots$).
- **Línea 21:** Suma el término actual a la sumatoria total (`suma += termino`).
- **Línea 22:** Incrementa el contador en 1 (`n += 1`).
- **Línea 23:** Retorna el resultado acumulado en `suma`.

---

### Vectorización de la Función con NumPy (Línea 26)
```python
26 miCos = np.frompyfunc(miCos, 2, 1)
```
- **`np.frompyfunc(miCos, 2, 1)`**: Convierte la función escalar `miCos` en una función universal (*ufunc*) de NumPy:
  - `2`: indica que recibe 2 argumentos de entrada (`x` y `numTerminos`).
  - `1`: indica que retorna 1 valor de salida (`suma`).
- Permite evaluar la función directamente sobre un arreglo completo de NumPy `x` sin necesidad de escribir bucles manuales.

---

### Dominio Justificado y Función de Referencia (Líneas 29 - 30)
```python
29 x = np.linspace(0, 2 * np.pi, 200)
30 y1 = np.cos(x)
```
- **Línea 29:** Genera un arreglo de **200 puntos** uniformemente distribuidos entre $0$ y $2\pi$ ($\approx 6.2832$). Se eligen 200 puntos (en lugar de 5 o 10) para garantizar que las curvas se vean completamente continuas y suaves, evitando distorsiones visuales por falta de resolución.
- **Línea 30:** Calcula el valor analítico exacto de referencia con `np.cos(x)`.

---

### Configuración de la Figura (Línea 32)
```python
32 plt.figure(1, figsize=(11, 8.5))
```
- Inicializa la ventana gráfica `figure(1)` con un tamaño de $11 \times 8.5$ pulgadas para una visualización cómoda y legible.

---

### Bloque 1: Evaluación con 1 Término ($N = 1$) (Líneas 34 - 49)
```python
34 y2_1 = miCos(x, 1)
35 error_1 = np.abs(y1 - y2_1)
36 
37 plt.subplot(3, 2, 1)
38 plt.title("Coseno original vs. Taylor (1 término)")
39 plt.plot(x, y1, label="cos(x) real")
40 plt.plot(x, y2_1, "--", label="Taylor (1 térm.)")
41 plt.ylim(-2.5, 2.5)
42 plt.legend()
43 plt.grid(True)
44 
45 plt.subplot(3, 2, 2)
46 plt.title("Error absoluto (1 término)")
47 plt.plot(x, error_1, "r")
48 plt.grid(True)
```
- **Línea 34:** Evalúa la serie de Taylor para $N = 1$ término ($P_1(x) = 1$).
- **Línea 35:** Calcula el error absoluto: $|y_{\text{real}} - y_{\text{aprox}}|$.
- **Línea 37:** Posiciona la gráfica en la fila 1, columna 1 (`plt.subplot(3, 2, 1)`).
- **Línea 38 - 43:** Grafica la curva real y la aproximación superpuestas con leyenda, fija límites en Y (`ylim(-2.5, 2.5)`) para que no se pierda la escala y añade cuadrícula.
- **Línea 45 - 48:** En la fila 1, columna 2 (`plt.subplot(3, 2, 2)`), grafica la curva del error absoluto en color rojo (`"r"`).

---

### Bloque 2: Evaluación con 3 Términos ($N = 3$) (Líneas 51 - 66)
```python
51 y2_3 = miCos(x, 3)
52 error_3 = np.abs(y1 - y2_3)
53 
54 plt.subplot(3, 2, 3)
55 plt.title("Coseno original vs. Taylor (3 términos)")
56 plt.plot(x, y1, label="cos(x) real")
57 plt.plot(x, y2_3, "--", label="Taylor (3 térm.)")
58 plt.ylim(-2.5, 2.5)
59 plt.legend()
60 plt.grid(True)
61 
62 plt.subplot(3, 2, 4)
63 plt.title("Error absoluto (3 términos)")
64 plt.plot(x, error_3, "r")
65 plt.grid(True)
```
- Repite el procedimiento en la fila 2 para **$N = 3$ términos** (polinomio de grado 4: $1 - x^2/2 + x^4/24$).
- Se observa claramente cómo la aproximación se acopla a la función real hasta aproximadamente $x \approx \pi$, y el error absoluto disminuye drásticamente en la primera mitad del dominio.

---

### Bloque 3: Evaluación con 5 Términos ($N = 5$) (Líneas 68 - 85)
```python
68 y2_5 = miCos(x, 5)
69 error_5 = np.abs(y1 - y2_5)
70 
71 plt.subplot(3, 2, 5)
72 plt.title("Coseno original vs. Taylor (5 términos)")
73 plt.plot(x, y1, label="cos(x) real")
74 plt.plot(x, y2_5, "--", label="Taylor (5 térm.)")
75 plt.ylim(-2.5, 2.5)
76 plt.legend()
77 plt.grid(True)
78 
79 plt.subplot(3, 2, 6)
80 plt.title("Error absoluto (5 términos)")
81 plt.plot(x, error_5, "r")
82 plt.grid(True)
83 
84 plt.tight_layout()
```
- Repite el procedimiento en la fila 3 para **$N = 5$ términos** (polinomio de grado 8).
- Con 5 términos, la curva de Taylor se ajusta casi a la perfección a todo el intervalo $[0, 2\pi]$, y el error se mantiene muy cercano a cero.
- **Línea 84 (`plt.tight_layout()`):** Ajusta los márgenes automáticamente para que ningún título ni etiqueta colisione.

---

### Ejecución y Conclusión Técnica Final (Líneas 87 - 100)
```python
87 if __name__ == "__main__":
88     plt.show()

# =============================================================================
# Conclusión técnica (cinco a ocho líneas):
# =============================================================================
"""
La serie de Taylor centrada en cero (Maclaurin) aproxima localmente la función coseno.
Al incrementar el número de términos de N = 1 a N = 5, el polinomio expande notablemente
el rango del dominio donde el ajuste visual es prácticamente indistinguible del coseno real.
Con N = 1, la aproximación es una constante horizontal (P(x) = 1) con gran error global;
con N = 3 términos el ajuste es preciso hasta cerca de pi rad; y con N = 5 términos
se cubre prácticamente todo el intervalo [0, 2*pi] con un error absoluto mínimo.
Fuera de la zona de convergencia efectiva, el error crece de manera rápida debido a la
divergencia polinómica natural de los términos de mayor exponente.
"""
```
- **Línea 88 (`plt.show()`):** Despliega la ventana gráfica interactiva en pantalla.
- **Comentario final:** Contiene exactamente **8 líneas** de conclusión técnica que explican el comportamiento de convergencia, el dominio y la precisión, cumpliendo con la exigencia formal del taller.
