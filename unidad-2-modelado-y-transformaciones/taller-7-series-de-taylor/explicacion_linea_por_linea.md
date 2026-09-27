# Explicación Detallada Línea a Línea · Taller 7: Aproximación de Funciones con Series de Taylor

Este documento explica qué hace cada bloque del archivo ejecutable [`taller_7_otras_funciones.py`](./taller_7_otras_funciones.py) y por qué.

El código conserva el **estilo algorítmico visto en clase** ([`codigo_base_clase.py`](./codigo_base_clase.py)): factorial recursivo, serie con `while`, vectorización con `np.frompyfunc` y subgráficas que comparan **5, 10 y 50 puntos**. Sobre esa base cumple dos enunciados.

**Enunciado específico del Taller 7:**

1. Versiones propias de **exponencial, seno, coseno, tangente y logaritmo natural** mediante series de Taylor.
2. Todas las funciones graficadas **en un mismo subplot**, para compararlas visualmente (figura 1).
3. **Precisión evaluada frente a NumPy**: el error máximo se imprime en consola.

**Requisitos generales de la actividad (Moodle):**

1. Funciones reutilizables con un **número configurable de términos** (`numTerminos`).
2. Un **dominio justificado** para cada función.
3. La función real y **tres aproximaciones** ($N = 2, 4, 8$) en la misma gráfica (figuras 2 a 6).
4. El **error absoluto** graficado.
5. Una **conclusión técnica de 8 líneas** como comentario final.

## Tabla de contenido

- [1. Fundamento matemático](#1-fundamento-matemático)
- [2. Explicación línea a línea](#2-explicación-línea-a-línea)
- [3. Resultados obtenidos](#3-resultados-obtenidos)
- [4. Preguntas que te pueden hacer en la sustentación](#4-preguntas-que-te-pueden-hacer-en-la-sustentación)

---

## 1. Fundamento matemático

La **serie de Taylor** de $f$ alrededor de un punto $x_0$ es:

$$f(x) = \sum_{n=0}^{\infty} \frac{f^{(n)}(x_0)}{n!} (x - x_0)^n$$

Cada término multiplica una derivada evaluada en $x_0$ por una potencia de $(x - x_0)$ y lo divide entre el factorial. Cuando $x_0 = 0$, se llama **serie de Maclaurin**.

Si se trunca en $N$ términos, se obtiene un **polinomio** $P_N(x)$. Es muy preciso cerca de $x_0$ y pierde precisión al alejarse. El **error absoluto** mide esa diferencia:

$$E_N(x) = |f(x) - P_N(x)|$$

| Función | Serie | Centro | Converge en |
| --- | --- | :---: | :---: |
| $e^x$ | $\displaystyle\sum_{n=0}^{\infty} \frac{x^n}{n!} = 1 + x + \frac{x^2}{2!} + \frac{x^3}{3!} + \dots$ | $0$ | todo $\mathbb{R}$ |
| $\sin x$ | $\displaystyle\sum_{n=0}^{\infty} \frac{(-1)^n x^{2n+1}}{(2n+1)!} = x - \frac{x^3}{3!} + \frac{x^5}{5!} - \dots$ | $0$ | todo $\mathbb{R}$ |
| $\cos x$ | $\displaystyle\sum_{n=0}^{\infty} \frac{(-1)^n x^{2n}}{(2n)!} = 1 - \frac{x^2}{2!} + \frac{x^4}{4!} - \dots$ | $0$ | todo $\mathbb{R}$ |
| $\tan x$ | $\displaystyle\sum_{n=1}^{\infty} \frac{(-1)^{n-1} 2^{2n}(2^{2n}-1) B_{2n}}{(2n)!} x^{2n-1} = x + \frac{x^3}{3} + \frac{2x^5}{15} + \dots$ | $0$ | $\lvert x\rvert < \pi/2$ |
| $\ln x$ | $\displaystyle\sum_{n=1}^{\infty} \frac{(-1)^{n+1} (x-1)^n}{n} = (x-1) - \frac{(x-1)^2}{2} + \frac{(x-1)^3}{3} - \dots$ | $1$ | $0 < x \le 2$ |

**Tres observaciones:**

- **Tangente:** sus coeficientes no siguen un patrón simple. Usan los **números de Bernoulli** $B_{2n}$: $B_2 = \tfrac{1}{6}$, $B_4 = -\tfrac{1}{30}$, $B_6 = \tfrac{1}{42}, \dots$ Su radio de convergencia es $\pi/2$ porque ahí está la primera asíntota, y ningún polinomio puede "atravesar" una asíntota.
- **Logaritmo:** **no tiene serie de Maclaurin**, porque $\ln(0)$ no existe y tampoco sus derivadas en $0$. Por eso se centra en $x_0 = 1$, donde $\ln(1) = 0$. Su radio es $1$, pues la singularidad más cercana está en $x = 0$, a distancia $1$ del centro.
- **Fuera del radio de convergencia**, la serie **diverge**: agregar términos empeora el resultado en lugar de mejorarlo.

---

## 2. Explicación línea a línea

### Docstring inicial (líneas 1 – 21)

Describe el propósito del archivo, las cinco series con su rango de convergencia y la organización de las figuras. También deja constancia de las herramientas y de la asistencia de IA utilizada, como exige la **integridad académica**.

---

### Importaciones (líneas 23 – 26)

```python
import math

import numpy as np
import matplotlib.pyplot as plt
```

- **`math`**: se usa por `math.comb(n, k)`, el coeficiente binomial $\binom{n}{k}$ que necesita la recurrencia de Bernoulli.
- **`numpy`**: genera el dominio (`np.linspace`), da las funciones de referencia (`np.exp`, `np.sin`, `np.cos`, `np.tan`, `np.log`), calcula el error (`np.abs`) y vectoriza (`np.frompyfunc`).
- **`matplotlib.pyplot`**: figuras, subgráficas, títulos, leyendas y cuadrículas.

---

### Factorial recursivo (líneas 29 – 36)

```python
def miFactorial(n):
    if (n == 0 or n == 1):
        fact = 1
    elif (n > 1):
        fact = n * miFactorial(n - 1)
    else:
        return "NaN"
    return fact
```

Es idéntico al de clase.

- **Caso base:** $0! = 1! = 1$.
- **Caso recursivo:** $n! = n \cdot (n-1)!$.
- **$n < 0$:** retorna `"NaN"`, porque el factorial no está definido para negativos.

---

### Números de Bernoulli (líneas 39 – 47)

```python
def miBernoulli(m):
    B = [1.0]  # B_0 = 1
    for j in range(1, m + 1):
        suma = 0
        for k in range(j):
            suma += math.comb(j + 1, k) * B[k]
        B.append(-suma / (j + 1))
    return B[m]
```

Implementa la recurrencia clásica:

$$B_0 = 1, \qquad B_j = -\frac{1}{j+1} \sum_{k=0}^{j-1} \binom{j+1}{k} B_k$$

- **Línea 41:** empieza la lista con $B_0 = 1$.
- **Líneas 42 – 46:** calcula cada $B_j$ usando todos los anteriores. Por eso se guardan en la lista `B`.
- **Línea 47:** retorna solo el que se pidió, $B_m$.

**Verificación:** `miBernoulli(2) = 0.1667` ($\tfrac{1}{6}$), `miBernoulli(4) = -0.0333` ($-\tfrac{1}{30}$) y `miBernoulli(6) = 0.0238` ($\tfrac{1}{42}$).

---

### Las cinco series (líneas 50 – 103)

Todas siguen **el mismo patrón** del código de clase:

```python
def miFuncion(x, numTerminos):
    suma = 0          # acumulador del polinomio
    n = 0             # índice del término (1 en tan y ln)
    while n < numTerminos:
        termino = ...  # fórmula del n-ésimo término
        suma += termino
        n += 1
    return suma
```

A diferencia del código de clase, que se detenía por tolerancia (`aporteMin`), aquí se suman **exactamente** `numTerminos` términos. Así se puede comparar $N = 2, 4, 8$, que es lo que pide el taller.

Lo único que cambia en cada una es la línea del `termino`:

| Función | Líneas | `termino = ...` | Qué hay que notar |
| --- | :---: | --- | --- |
| `miExp` | 50 – 58 | `x**n / miFactorial(n)` | Todas las potencias y sin signo alternante. |
| `miSin` | 61 – 69 | `((-1)**n) / miFactorial(2*n + 1) * x**(2*n + 1)` | Potencias **impares** con signo alternante, igual que `miSin` de clase. |
| `miCos` | 72 – 80 | `((-1)**n) / miFactorial(2*n) * x**(2*n)` | Potencias **pares** con signo alternante. |
| `miTan` | 83 – 92 | `coeficiente / miFactorial(2*n) * x**(2*n - 1)` | Empieza en `n = 1` y usa `n <= numTerminos`. |
| `miLn` | 95 – 103 | `((-1)**(n + 1)) * (x - 1)**n / n` | Empieza en `n = 1`, usa $(x - 1)$ porque el centro es $1$, y **no usa factorial**. |

**Sobre `miTan`:** la línea 88 calcula el coeficiente $(-1)^{n-1}\, 2^{2n}\,(2^{2n}-1)\, B_{2n}$ por separado, para que la línea sea legible.

- Comprobación manual con $n = 1$: el coeficiente es $1 \cdot 4 \cdot 3 \cdot \tfrac{1}{6} = 2$, y $2 / 2! = 1$, lo que da el término $x$ ✓.
- Con $n = 2$: el coeficiente es $-1 \cdot 16 \cdot 15 \cdot (-\tfrac{1}{30}) = 8$, y $8 / 4! = \tfrac{1}{3}$, lo que da el término $\tfrac{x^3}{3}$ ✓.

**Sobre `miLn`:** el factorial se cancela. La derivada $n$-ésima de $\ln x$ en $1$ es $(-1)^{n+1}(n-1)!$, y $\frac{(n-1)!}{n!} = \frac{1}{n}$.

---

### Vectorización (líneas 106 – 112)

```python
miExp = np.frompyfunc(miExp, 2, 1)
...
miLn = np.frompyfunc(miLn, 2, 1)
```

`np.frompyfunc(func, 2, 1)` convierte una función que trabaja con **un número** en una que trabaja con **arreglos completos**:

- `2` significa dos entradas: `x` y `numTerminos`.
- `1` significa una salida: `suma`.

Esa salida es un arreglo de tipo `object`. Por eso, más adelante se convierte con `.astype(float)` antes de restar o graficar.

---

### Parámetros del experimento (líneas 114 – 115)

```python
RESOLUCIONES = [5, 10, 50]   # número de puntos de muestreo
TERMINOS = [2, 4, 8]         # número de términos de cada aproximación
```

Estas son las dos variables del experimento, separadas a propósito:

- **`RESOLUCIONES`:** cuántos puntos se evalúan. Esto afecta **cómo se ve** la curva, igual que en el código de clase.
- **`TERMINOS`:** cuántos términos tiene cada polinomio. Esto afecta **qué tan precisa** es la aproximación.

---

### Tabla de funciones y justificación del dominio (líneas 117 – 131)

```python
FUNCIONES = [
    # (nombre,  fReal,   fTaylor, xMin, xMax,      limiteY, unidad X)
    ("e^x",    np.exp, miExp,   -2,   3,         None,    ""),
    ("sin(x)", np.sin, miSin,   0,    2 * np.pi, 3,       "rad"),
    ...
]
```

Cada fila reúne todo lo que se necesita para graficar una función. Así, agregar una sexta función es añadir **una línea**.

| Función | Dominio | Justificación |
| --- | --- | --- |
| $e^x$ | $[-2, 3]$ | Converge en todo $\mathbb{R}$. El intervalo muestra cómo crece el error con $\lvert x\rvert$ sin que los valores se disparen. |
| $\sin, \cos$ | $[0, 2\pi]$ rad | Un periodo completo, el mismo intervalo de clase. |
| $\tan$ | $[0, 2\pi]$ rad | Se grafica **completo a propósito** para evidenciar que la serie solo sirve antes de $\pi/2$. |
| $\ln$ | $[0.1, 3]$ | Converge en $(0, 2]$. Empieza en $0.1$ porque en $0$ $\ln \to -\infty$, y llega hasta $3$ para mostrar la divergencia. |

- **`limiteY`:** recorta el eje Y cuando la función o sus aproximaciones se disparan. Sin él, la escala aplastaría el resto de la gráfica.
- **Unidad X:** `"rad"` para las trigonométricas. $e^x$ y $\ln x$ no tienen unidad.

---

### Figura 1: todas las funciones en un mismo subplot (líneas 134 – 153)

```python
def graficarTodasJuntas(numFigura, numTerminos, numPuntos):
```

Responde directamente al enunciado: *"graficar todas estas funciones en un mismo subplot, facilitando así una comparativa visual directa"*.

- **Línea 140:** recorre la tabla `FUNCIONES`. Los `_` ignoran `limiteY` y la unidad, que aquí no se usan.
- **Línea 142:** grafica la función real con línea continua. `linea, = plt.plot(...)` guarda el objeto de la línea para poder leer su color.
- **Líneas 143 – 144:** grafica la aproximación con línea discontinua (`"--"`) y **el mismo color** (`linea.get_color()`). Así cada par real/Taylor se identifica a simple vista.
- **Líneas 146 – 147:** `plt.axvline` dibuja rectas verticales en $x = \pi/2$ y $x = 2$, los **límites de convergencia** de tan y ln. Más allá de ellas, las curvas discontinuas se separan de las reales.
- **Línea 148:** `plt.ylim(-4, 6)` fija una escala común para las cinco.
- **Línea 193:** se llama con `TERMINOS[-1]` ($N = 8$) y `RESOLUCIONES[-1]` (50 puntos), la mejor aproximación y la curva más suave.

---

### Figuras 2 a 6: detalle por función (líneas 156 – 189)

```python
def graficarComparacion(numFigura, nombre, fReal, fTaylor, xMin, xMax, limiteY=None, unidadX=""):
```

El código de clase repetía tres bloques casi iguales. Aquí se agrupan en **una sola función reutilizable** que la línea 196 llama una vez por cada fila de `FUNCIONES`.

- **Línea 159:** arma la etiqueta del eje X con su unidad, por ejemplo `x (rad)`.
- **Línea 161:** `enumerate(RESOLUCIONES)` recorre $5, 10, 50$ y da el número de fila $0, 1, 2$.
- **Líneas 162 – 163:** genera `numPuntos` valores con `np.linspace` y evalúa la función de referencia de NumPy.
- **Líneas 165 – 175, columna izquierda:**
  - `plt.subplot(3, 2, 2 * fila + 1)` elige las posiciones impares (1, 3, 5).
  - Dibuja la función real en negro grueso y encima las tres aproximaciones en línea discontinua.
- **Líneas 177 – 187, columna derecha:**
  - `plt.subplot(3, 2, 2 * fila + 2)` elige las posiciones pares (2, 4, 6).
  - **Línea 180:** calcula el error absoluto $|f(x) - P_N(x)|$ **frente a NumPy**.
  - **Línea 181:** `plt.semilogy` grafica en **escala logarítmica**, porque los errores van de $10^{-18}$ a $10^{9}$. En escala lineal solo se vería la curva más grande.
  - **Líneas 182 – 183:** imprime en consola el error máximo, solo para la mayor resolución. El máximo está en el extremo del intervalo, que `linspace` siempre incluye, así que es igual con 5, 10 o 50 puntos. Imprimirlo tres veces sería redundante.
- **Línea 189:** `plt.tight_layout()` evita que títulos y etiquetas se encimen.

---

### Ejecución y conclusión (líneas 192 – 212)

- **Línea 193:** crea la figura comparativa.
- **Líneas 196 – 197:** crea una figura de detalle por función. Son las figuras 2 a 6, porque el índice empieza en `i + 2`.
- **Líneas 199 – 200:** `plt.show()` abre las seis ventanas. El `if __name__ == "__main__"` evita que se abran si el archivo se **importa** desde otro script.
- **Líneas 205 – 212:** la **conclusión técnica de 8 líneas**. Se basa en los resultados de la sección siguiente.

---

## 3. Resultados obtenidos

Estos son los errores máximos frente a NumPy en el dominio de cada función, tal como los imprime el script:

| Función | Dominio | $N = 2$ | $N = 4$ | $N = 8$ |
| --- | --- | :---: | :---: | :---: |
| $e^x$ | $[-2, 3]$ | 16.1 | 7.09 | 0.24 |
| $\sin x$ | $[0, 2\pi]$ | 35.1 | 30.2 | 0.09 |
| $\cos x$ | $[0, 2\pi]$ | 19.7 | 40.3 | 0.25 |
| $\tan x$ | $[0, 2\pi]$ | 89 | 2.2·10⁴ | **1.5·10⁹** |
| $\ln x$ | $[0.1, 3]$ | 1.10 | 2.43 | **20.4** |

Si se evalúa **solo dentro de la zona de convergencia y lejos del borde**, con $N = 8$ los errores son pequeños:

| Función | Intervalo | Error máx. ($N = 8$) |
| --- | --- | :---: |
| $\sin x$ | $[0, \pi]$ | $7.7 \cdot 10^{-7}$ |
| $\tan x$ | $[0, 1]$ | $9.9 \cdot 10^{-4}$ |
| $\ln x$ | $[0.5, 1.5]$ | $4.0 \cdot 10^{-4}$ |
| $e^x$ | $[-2, 1]$ | $5.2 \cdot 10^{-3}$ |

**Lectura de los resultados:**

1. **Cerca del centro todas las series son excelentes.** El error crece a medida que $x$ se aleja de $x_0$.
2. **$e^x$, sin y cos** convergen en todo $\mathbb{R}$, así que con suficientes términos el error baja en todo el intervalo. Pero **no siempre de forma monótona**: en cos, $N = 4$ es peor que $N = 2$ cerca de $2\pi$. El término $x^6/720$ domina ahí, y los términos siguientes todavía no alcanzan a cancelarlo.
3. **tan y ln** tienen radio finito. Dentro de él, más términos reducen el error. Fuera ocurre **al revés**: con $N = 8$, tan llega a $\sim 10^9$ y ln a $\sim 20$. Así se ve en la práctica que la serie **diverge fuera de su radio de convergencia**.
4. **Puntos de muestreo:** el error máximo es igual con 5, 10 y 50 puntos, así que la precisión la decide $N$, no la resolución. Con 5 puntos, además, `linspace(0, 2π, 5)` cae **exactamente** en $\pi/2$ y $3\pi/2$, las asíntotas de tan. Por eso esa fila muestra líneas verticales y errores de $\sim 10^{16}$: el muestreo también debe justificarse.

---

## 4. Preguntas que te pueden hacer en la sustentación

<details>
<summary><strong>¿Por qué ln(x) no está centrada en 0 como las demás?</strong></summary>

La serie de Maclaurin exige evaluar $f$ y sus derivadas en $x = 0$, y $\ln(0)$ no existe: tiende a $-\infty$. Se elige $x_0 = 1$ porque $\ln(1) = 0$ y sus derivadas son sencillas. Una alternativa equivalente es la serie de $\ln(1 + u)$ con $u = x - 1$.
</details>

<details>
<summary><strong>¿Por qué usaste <code>numTerminos</code> en lugar de la tolerancia <code>aporteMin</code> de clase?</strong></summary>

El taller pide comparar aproximaciones con un número **configurable** de términos. Con tolerancia, la función decide sola cuándo parar, y no se podrían comparar $N = 2, 4, 8$. Además, fuera del radio de convergencia los términos nunca se hacen pequeños y un `while` por tolerancia **no terminaría nunca**.
</details>

<details>
<summary><strong>¿Por qué aparece <code>.astype(float)</code>?</strong></summary>

`np.frompyfunc` retorna arreglos de tipo `object`. Para operar con `np.abs` y graficar de forma confiable se convierten a `float`.
</details>

<details>
<summary><strong>¿Por qué el eje del error está en escala logarítmica?</strong></summary>

Los errores abarcan más de 25 órdenes de magnitud. En escala lineal, la curva de mayor error aplastaría a las demás contra el cero.
</details>

<details>
<summary><strong>¿Por qué la serie de tan no funciona después de π/2, si tan(x) existe en (π/2, 3π/2)?</strong></summary>

Una serie de Taylor solo converge dentro de un intervalo centrado en $x_0$ cuyo radio es la distancia a la singularidad más cercana. Para tan, esa singularidad es la asíntota en $\pi/2$. Para aproximar tan en $(\pi/2, 3\pi/2)$ habría que usar una serie de Taylor centrada en otro punto, por ejemplo en $x_0 = \pi$.
</details>

<details>
<summary><strong>¿Cómo agregarías una sexta función, por ejemplo sinh(x)?</strong></summary>

Primero se escribe `miSinh` con el mismo patrón, con el término `x**(2*n + 1) / miFactorial(2*n + 1)`. Luego se vectoriza con `np.frompyfunc(miSinh, 2, 1)` y se agrega una línea a `FUNCIONES`: `("sinh(x)", np.sinh, miSinh, 0, 2 * np.pi, None, "rad")`. Las gráficas se generan solas.
</details>

<details>
<summary><strong>¿Cómo cambiarías el experimento para usar 3, 6 y 10 términos?</strong></summary>

Solo hay que editar `TERMINOS = [3, 6, 10]` en la línea 115. Todo lo demás se adapta solo.
</details>
