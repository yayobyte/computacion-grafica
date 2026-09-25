# Explicación Detallada Línea a Línea · Taller 7: Series de Taylor

Este documento complementa el desarrollo del **Taller 7 de la Unidad 2 (Computación Gráfica - UTP)**. Su objetivo es explicar de forma rigurosa y didáctica qué ocurre en cada línea de código, tanto en la **versión base vista en clase** (imágenes de referencia) como en la **versión final del taller** entregada en [`taller_7_series_taylor.py`](./taller_7_series_taylor.py).

---

## 1. Fundamento Matemático: Serie de Taylor para $\sin(x)$

La serie de Taylor centrada en $x_0 = 0$ (también llamada **Serie de Maclaurin**) para la función analítica $f(x) = \sin(x)$ está definida como:

$$\sin(x) = \sum_{n=0}^{\infty} \frac{(-1)^n}{(2n+1)!} x^{2n+1} = x - \frac{x^3}{3!} + \frac{x^5}{5!} - \frac{x^7}{7!} + \frac{x^9}{9!} - \dots$$

### Propiedades clave:
1. **Términos impares:** Solo contiene potencias impares de $x$ y factoriales impares, reflejando que el seno es una función impar: $\sin(-x) = -\sin(x)$.
2. **Signos alternantes:** El factor $(-1)^n$ genera la alternancia $+ - + - \dots$, lo que permite la oscilación acotada en $[-1, 1]$.
3. **Radio de convergencia ($R = \infty$):** Teóricamente converge para cualquier $x \in \mathbb{R}$, pero en computación finita la convergencia es **localmente rápida cerca de $x=0$** y requiere muchos más términos a medida que $|x|$ aumenta.

---

## 2. Explicación Línea a Línea del Código Base de Clase

A continuación se transcribe y explica cada línea del código presentado en las imágenes de clase:

```python
 1 import numpy as np
 2 import matplotlib.pyplot as plt
 3 import math
```
- **Línea 1:** Importa la biblioteca `numpy` con el alias convencional `np`. Se usa para el manejo de arreglos numéricos multidimensionales y funciones matemáticas vectorizadas.
- **Línea 2:** Importa el submódulo `pyplot` de `matplotlib` con el alias `plt`. Es la herramienta estándar para generar gráficos 2D.
- **Línea 3:** Importa el módulo estándar `math` de Python, utilizado para operaciones matemáticas sobre escalares (como `math.fabs`).

---

### Función Factorial Recursiva

```python
 5 def miFactorial(n):
 6     if (n==0 or n==1):
 7         fact= 1
 8     elif (n>1):
 9         fact=n*miFactorial(n-1)
10     else:
11         return "NaN"
12     return (fact)
```
- **Línea 5:** Declara la función `miFactorial`, que toma como argumento un número `n`.
- **Línea 6:** **Caso base de la recursión:** Si $n=0$ o $n=1$, por definición matemática $0! = 1$ y $1! = 1$.
- **Línea 7:** Asigna el valor `1` a la variable local `fact`.
- **Línea 8:** Evalúa si $n$ es un entero estrictamente mayor que 1.
- **Línea 9:** **Paso recursivo:** Aplica la identidad $n! = n \times (n-1)!$, llamando a la función a sí misma con `n - 1`. Cada llamada se apila en la pila de ejecución (*call stack*) hasta alcanzar el caso base.
- **Línea 10-11:** Control de casos no válidos: si $n < 0$, retorna el string `"NaN"` (*Not a Number*).
- **Línea 12:** Retorna el resultado calculado en `fact`.

---

### Función de Aproximación con Criterio de Tolerancia

```python
15 def miSin(x):
16     suma=0
17     termino=0
18     n=0
19     aporteMin=0.00001
20     while(True):
21         termino=((-1)**n) / (miFactorial(2*n+1)) * x**(2*n+1)
22         suma += termino
23         n += 1
24         if(math.fabs(termino)<aporteMin):
25             break
26     return (suma)
```
- **Línea 15:** Define la función `miSin(x)` para calcular el seno de un valor escalar `x` en radianes.
- **Línea 16:** Inicializa el acumulador `suma = 0`, donde se sumarán los términos sucesivos del polinomio.
- **Línea 17:** Inicializa la variable `termino = 0`, que almacena el valor del monomio evaluado en la iteración actual.
- **Línea 18:** Inicializa el índice `n = 0`, correspondiente al contador del término de la serie ($n = 0, 1, 2, \dots$).
- **Línea 19:** Define una tolerancia de parada `aporteMin = 0.00001` ($10^{-5}$). Si el valor absoluto del nuevo término a sumar es menor que este umbral, el algoritmo asume que la serie ha convergido suficientemente y detiene el cálculo.
- **Línea 20:** Inicia un bucle infinito `while(True)`, cuya salida está controlada internamente por la condición `break`.
- **Línea 21:** Calcula el término $n$-ésimo de la serie de Taylor:
  $$\text{termino} = \frac{(-1)^n}{(2n+1)!} \cdot x^{2n+1}$$
  - `(-1)**n`: determina el signo alternante.
  - `miFactorial(2*n+1)`: calcula el factorial del exponente impar.
  - `x**(2*n+1)`: eleva el valor $x$ a la potencia impar.
- **Línea 22:** Acumula el término actual en la sumatoria total: `suma = suma + termino`.
- **Línea 23:** Incrementa el contador `n` en 1 para la siguiente potencia impar ($2n+1$).
- **Línea 24:** Evalúa el criterio de parada: calcula el valor absoluto del término con `math.fabs(termino)` y lo compara contra `aporteMin`.
- **Línea 25:** Si el aporte del término es inferior a $10^{-5}$, ejecuta `break` y finaliza el ciclo `while`.
- **Línea 26:** Retorna el valor acumulado en `suma`.

---

### Vectorización de la Función Escalar con NumPy

```python
29 miSin= np.frompyfunc(miSin, 1, 1)
```
- **Línea 29:** `np.frompyfunc(func, nin, nout)` transforma una función que opera sobre escalares (`miSin`) en una **función universal (*ufunc*) de NumPy**:
  - `1`: indica que la función recibe 1 argumento de entrada.
  - `1`: indica que la función produce 1 valor de salida.
  - **¿Por qué fue necesaria en el código del profesor?** Porque la función `miSin` original usa `while`, `math.fabs` y operadores escalares (`**`), por lo que no puede recibir directamente un arreglo `np.ndarray`. Al envolverla con `frompyfunc`, NumPy aplica automáticamente la función elemento a elemento sobre cada celda del arreglo.

---

### Generación de Datos y Graficación por Resolución de Puntos

```python
31 x=np.linspace(0,2*np.pi,5)
32 y1=np.sin(x)
33 y2=miSin(x)
34 
35 plt.figure(1)
36 plt.subplot(3,2,1)
37 plt.title("Función Seno original")
38 plt.plot(x,y1)
```
- **Línea 31:** Genera un arreglo `x` de **5 puntos** equiespaciados entre $0$ y $2\pi$ mediante `np.linspace(inicio, fin, num)`.
- **Línea 32:** Evalúa la función analítica estándar `np.sin(x)` en esos 5 puntos, guardando el resultado en `y1`.
- **Línea 33:** Evalúa la función de Taylor `miSin(x)` en esos mismos 5 puntos, guardando el resultado en `y2`.
- **Línea 35:** Crea o activa la ventana de visualización número 1 (`figure(1)`).
- **Línea 36:** Selecciona el primer panel de una cuadrícula de subgráficas: `plt.subplot(filas, columnas, índice)`. En este caso, cuadrícula de $3 \times 2$, posición 1 (fila 1, columna 1).
- **Línea 37:** Asigna el título `"Función Seno original"` a este panel.
- **Línea 38:** Dibuja la curva uniendo con segmentos rectos los 5 puntos calculados para la función original. Como solo hay 5 puntos, la curva se ve poligonal y poco suave.

```python
40 plt.subplot(3,2,2)
41 plt.title("Función Seno usando series de tylor")
42 plt.plot(x,y2)
```
- **Líneas 40-42:** Configura la posición 2 de la cuadrícula (fila 1, columna 2), titula el gráfico y grafica la aproximación de Taylor evaluada en los mismos 5 puntos.

```python
44 x=np.linspace(0,2*np.pi,10)
45 y1=np.sin(x)
46 y2=miSin(x)
47 
48 plt.subplot(3,2,3)
49 plt.title("Función Seno original")
50 plt.plot(x,y1)
51 
52 plt.subplot(3,2,4)
53 plt.title("Función Seno usando series de tylor")
54 plt.plot(x,y2)
```
- **Líneas 44-54:** Repite el experimento pero aumentando la densidad a **10 puntos** (`np.linspace(0, 2*np.pi, 10)`).
  - Posición 3 (fila 2, columna 1): Seno original con 10 puntos.
  - Posición 4 (fila 2, columna 2): Taylor con 10 puntos.
  - Se observa mayor suavidad visual, pero aún con discretización apreciable.

```python
56 x=np.linspace(0,2*np.pi,50)
57 y1=np.sin(x)
58 y2=miSin(x)
59 
60 plt.subplot(3,2,5)
61 plt.title("Función Seno original")
62 plt.plot(x,y1)
63 
64 plt.subplot(3,2,6)
65 plt.title("Función Seno usando series de tylor")
66 plt.plot(x,y2)
```
- **Líneas 56-66:** Repite el experimento con **50 puntos** en las posiciones 5 y 6 (fila 3). Con 50 muestras, ambas curvas se ven completamente continuas y suaves al ojo humano.

---

## 3. Comparativa: ¿Qué hizo el código de clase vs. Qué exige el Taller 7?

| Aspecto | Código Visto en Clase | Requisito Exigido en Taller 7 |
| :--- | :--- | :--- |
| **Control de Términos** | Fijo mediante tolerancia interna (`aporteMin=0.00001`). No permitía elegir $N$ términos. | **Configurable por parámetro:** función que recibe explícitamente $N$ términos acumulados. |
| **Comparación de Polinomios** | Comparaba la misma aproximación convergida variando únicamente el número de puntos de la cuadrícula (5, 10, 50). | **Comparar al menos 3 polinomios de distinto orden** (ej. $N=1, 2, 3, 5, 7$) contra la función real en la misma gráfica. |
| **Cálculo del Error** | No calculaba ni graficaba el error numérico. | **Calcular y graficar el error absoluto** $|f(x) - P_N(x)|$ a lo largo de todo el dominio. |
| **Dominio** | Solo $[0, 2\pi]$ sin justificación de simetría. | **Dominio justificado** (ej. $[-2\pi, 2\pi]$) para evidenciar la divergencia simétrica respecto a $x_0 = 0$. |
| **Rótulos y Conclusión** | Subplots básicos sin etiquetas en ejes ($x, y$) ni leyendas. | Gráficas rotuladas profesionalmente y **conclusión técnica obligatoria de 5 a 8 líneas**. |

---

## 4. Explicación del Código Final del Taller (`taller_7_series_taylor.py`)

El archivo [`taller_7_series_taylor.py`](./taller_7_series_taylor.py) fue diseñado para satisfacer rigurosamente todos los criterios de evaluación.

### 4.1. Factorial Robusto y Recursivo
```python
def mi_factorial(n: int) -> int:
    if not isinstance(n, (int, np.integer)):
        raise TypeError("El factorial solo está definido para números enteros.")
    if n < 0:
        raise ValueError("El factorial no está definido para números negativos.")
    if n == 0 or n == 1:
        return 1
    return n * mi_factorial(n - 1)
```
- Conserva el espíritu didáctico de la **recursividad** visto en clase.
- Añade validaciones de tipo y valor para evitar llamadas infinitas o errores silenciosos si se ingresan valores negativos o flotantes.

### 4.2. Aproximación con Número Configurable de Términos
```python
def aproximacion_taylor_seno(x: np.ndarray, num_terminos: int) -> np.ndarray:
    if num_terminos < 1:
        raise ValueError("El número de términos debe ser al menos 1.")
    
    x_arr = np.asarray(x, dtype=np.float64)
    suma = np.zeros_like(x_arr)
    
    for k in range(num_terminos):
        potencia = 2 * k + 1
        coeficiente = ((-1) ** k) / mi_factorial(potencia)
        termino = coeficiente * (x_arr ** potencia)
        suma += termino
        
    return suma
```
- **Parámetro `num_terminos` ($N$):** Permite controlar exactamente cuántos términos de la sumatoria se suman:
  - $N=1$: Polinomio $P_1(x) = x$ (grado 1).
  - $N=2$: Polinomio $P_2(x) = x - \frac{x^3}{6}$ (grado 3).
  - $N=3$: Polinomio $P_3(x) = x - \frac{x^3}{6} + \frac{x^5}{120}$ (grado 5).
  - $N=5$: Polinomio de grado 9.
  - $N=7$: Polinomio de grado 13.
- **Vectorización Nativa:** `x_arr ** potencia` aprovecha las instrucciones SIMD vectorizadas de NumPy, eliminando la sobrecarga lenta de `np.frompyfunc` y calculando el polinomio para cientos de puntos de forma instantánea.

### 4.3. Cálculo del Error Absoluto
```python
def calcular_error_absoluto(y_real: np.ndarray, y_aprox: np.ndarray) -> np.ndarray:
    return np.abs(y_real - y_aprox)
```
Calcula la métrica canónica del error en análisis numérico:

$$E_{\text{abs}}(x) = |\sin(x) - P_N(x)|$$

### 4.4. Justificación Técnica del Dominio
```python
x_inicio = -2 * np.pi
x_fin = 2 * np.pi
num_puntos = 600

x = np.linspace(x_inicio, x_fin, num_puntos)
```
- **Intervalo $[-2\pi, 2\pi]$:** Comprende dos períodos completos ($\approx [-6.28, 6.28]$). Permite ver la simetría impar y constatar que cerca del punto de expansión $x=0$, todos los polinomios ajustan con gran exactitud; pero al alejarse hacia los extremos, los polinomios de bajo orden se disparan hacia $\pm \infty$.
- **600 puntos:** Brinda una resolución gráfica continua de alta fidelidad, evitando quiebres en las curvas.

### 4.5. Gráficas Comparables y Escala Logarítmica para el Error
- **Subplot 1 (Aproximación vs. Real):** Presenta la curva real $\sin(x)$ junto a 5 aproximaciones ($N=1, 2, 3, 5, 7$). Se utiliza `ylim(-2.5, 2.5)` para delimitar la ventana de interés visual y evitar que los extremos divergentes de los polinomios reduzcan a una línea plana la zona central de convergencia.
- **Subplot 2 (Error Absoluto):** Se aplica **escala logarítmica** en el eje Y (`ax2.set_yscale('log')`). Esto es indispensable en computación gráfica y análisis numérico, ya que el error varía en más de 16 órdenes de magnitud: desde $10^{-15}$ (precisión de doble precisión flotante IEEE 754) en el centro, hasta más de $10^2$ en los extremos.

---

## 5. Análisis de Resultados Numéricos

Al ejecutar el script, se obtiene el siguiente resumen de errores en el dominio $[-2\pi, 2\pi]$:

| Términos ($N$) | Grado del Polinomio | Error Máximo | Error Promedio | Comportamiento Visual |
| :---: | :---: | :---: | :---: | :--- |
| **1** | 1 (lineal) | $6.2832 \times 10^{0}$ | $3.1468 \times 10^{0}$ | Solo es válida para ángulos pequeños ($|x| < 0.5$). |
| **2** | 3 (cúbico) | $3.5059 \times 10^{1}$ | $7.2404 \times 10^{0}$ | Ajusta bien hasta el primer pico ($x \approx \pm \pi/2$). |
| **3** | 5 (quíntico) | $4.6547 \times 10^{1}$ | $6.4742 \times 10^{0}$ | Ajusta hasta aproximadamente $x \approx \pm \pi$. |
| **5** | 9 | $1.1900 \times 10^{1}$ | $1.0429 \times 10^{0}$ | Cubre casi un período completo con alta precisión. |
| **7** | 13 | $6.2488 \times 10^{-1}$ | $4.0630 \times 10^{-2}$ | Ajusta prácticamente los dos periodos completos $[-2\pi, 2\pi]$. |

---

## 6. Conclusión Técnica (Incluida en el Script)

> *"La serie de Taylor centrada en el origen exhibe convergencia uniforme y asintótica hacia sen(x). Al incrementar el número de términos N, el polinomio extiende progresivamente el intervalo de validez donde el error absoluto se aproxima a la precisión de máquina (~10^-16), reduciendo drásticamente la discrepancia en el centro. Sin embargo, para cualquier N finito, al alejarse de x = 0 el término dominante de mayor grado provoca una divergencia polinómica exponencial, lo que hace crecer el error en los extremos del dominio [-2π, 2π]. Por consiguiente, la precisión en computación gráfica no solo depende de la cantidad de términos evaluados, sino críticamente de la cercanía al punto de expansión y del costo computacional de evaluar factoriales de alto orden."*

---

## 7. Preguntas Frecuentes para Sustentación

1. **¿Por qué se llama serie de Maclaurin en lugar de Taylor?**  
   Porque la serie de Maclaurin es simplemente el caso particular de la serie de Taylor cuando el punto de expansión es $x_0 = 0$.
2. **¿Por qué el error explota en los bordes?**  
   Porque un polinomio de grado $k$ tiende a $\pm \infty$ cuando $x \to \pm \infty$, mientras que la función seno es acotada entre $[-1, 1]$.
3. **¿Por qué no usamos simplemente $N = 100$?**  
   Porque el factorial $(2n+1)!$ crece extremadamente rápido ($15! \approx 1.3 \times 10^{12}$, $21! \approx 5.1 \times 10^{19}$), lo que puede ocasionar problemas de desbordamiento (*overflow*) o pérdida de dígitos significativos por cancelación catastrófica en aritmética de punto flotante.
