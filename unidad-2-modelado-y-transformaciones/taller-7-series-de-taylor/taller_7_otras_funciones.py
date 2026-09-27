"""
Taller 7 - Aproximación de funciones con Series de Taylor en Python.

Mismo esquema del código de clase (miFactorial + serie + np.frompyfunc + subplots),
aplicado a las cinco funciones que pide el enunciado:
    e^x    = sum_{n>=0} x^n / n!                                  (converge para todo x)
    sin(x) = sum_{n>=0} (-1)^n * x^(2n+1) / (2n+1)!               (converge para todo x)
    cos(x) = sum_{n>=0} (-1)^n * x^(2n) / (2n)!                   (converge para todo x)
    tan(x) = sum_{n>=1} (-1)^(n-1) * 2^(2n) * (2^(2n)-1) * B_2n * x^(2n-1) / (2n)!
             (B_2n = números de Bernoulli; converge solo en |x| < pi/2)
    ln(x)  = sum_{n>=1} (-1)^(n+1) * (x-1)^n / n                  (Taylor en x0 = 1;
             converge solo en 0 < x <= 2. No hay serie de Maclaurin porque ln(0) no existe)

Figura 1: las cinco funciones reales vs. sus aproximaciones en un mismo subplot.
Figuras 2 a 6: una por función, con 3 filas = resolución de muestreo (5, 10 y 50 puntos).
    Columna izquierda: función real + 3 aproximaciones (distinto número de términos).
    Columna derecha:   error absoluto |f(x) - P_N(x)| de cada aproximación.
En consola se imprime el error máximo frente a NumPy de cada función y número de términos.

Herramientas: Python 3, NumPy, Matplotlib. Asistencia de IA: Claude OPUS 5.5 (Anthropic).
"""

import math

import numpy as np
import matplotlib.pyplot as plt


def miFactorial(n):
    if (n == 0 or n == 1):
        fact = 1
    elif (n > 1):
        fact = n * miFactorial(n - 1)
    else:
        return "NaN"
    return fact


def miBernoulli(m):
    """Número de Bernoulli B_m por la recurrencia B_m = -1/(m+1) * sum C(m+1, k) * B_k."""
    B = [1.0]  # B_0 = 1
    for j in range(1, m + 1):
        suma = 0
        for k in range(j):
            suma += math.comb(j + 1, k) * B[k]
        B.append(-suma / (j + 1))
    return B[m]


def miExp(x, numTerminos):
    """Aproxima e^x con los primeros numTerminos de su serie de Maclaurin."""
    suma = 0
    n = 0
    while n < numTerminos:
        termino = x**n / miFactorial(n)
        suma += termino
        n += 1
    return suma


def miSin(x, numTerminos):
    """Aproxima sin(x) con los primeros numTerminos de su serie de Maclaurin."""
    suma = 0
    n = 0
    while n < numTerminos:
        termino = ((-1)**n) / miFactorial(2 * n + 1) * x**(2 * n + 1)
        suma += termino
        n += 1
    return suma


def miCos(x, numTerminos):
    """Aproxima cos(x) con los primeros numTerminos de su serie de Maclaurin."""
    suma = 0
    n = 0
    while n < numTerminos:
        termino = ((-1)**n) / miFactorial(2 * n) * x**(2 * n)
        suma += termino
        n += 1
    return suma


def miTan(x, numTerminos):
    """Aproxima tan(x) con los primeros numTerminos de su serie de Maclaurin."""
    suma = 0
    n = 1
    while n <= numTerminos:
        coeficiente = ((-1)**(n - 1)) * 2**(2 * n) * (2**(2 * n) - 1) * miBernoulli(2 * n)
        termino = coeficiente / miFactorial(2 * n) * x**(2 * n - 1)
        suma += termino
        n += 1
    return suma


def miLn(x, numTerminos):
    """Aproxima ln(x) con los primeros numTerminos de su serie de Taylor centrada en x0 = 1."""
    suma = 0
    n = 1
    while n <= numTerminos:
        termino = ((-1)**(n + 1)) * (x - 1)**n / n
        suma += termino
        n += 1
    return suma


# -------------------------------------------------------------
# Vectorización (igual que en clase): 2 entradas (x, numTerminos), 1 salida
miExp = np.frompyfunc(miExp, 2, 1)
miSin = np.frompyfunc(miSin, 2, 1)
miCos = np.frompyfunc(miCos, 2, 1)
miTan = np.frompyfunc(miTan, 2, 1)
miLn = np.frompyfunc(miLn, 2, 1)

RESOLUCIONES = [5, 10, 50]   # número de puntos de muestreo
TERMINOS = [2, 4, 8]         # número de términos de cada aproximación

# Cada función con su referencia de NumPy, su serie, su dominio y su recorte del eje Y.
#   sin, cos, tan: [0, 2*pi] rad, un periodo completo (el mismo intervalo de clase).
#     tan se grafica completo a propósito para ver que la serie solo sirve antes de pi/2.
#   e^x: [-2, 3]. Converge en todo R, pero el error crece con |x|; este intervalo lo
#     muestra sin que los valores se disparen.
#   ln(x): [0.1, 3]. La serie en x0 = 1 solo converge en (0, 2]; se extiende hasta 3
#     para ver la divergencia, y empieza en 0.1 porque en 0 ln(x) -> -infinito.
FUNCIONES = [
    # (nombre,  fReal,   fTaylor, xMin, xMax,      limiteY, unidad X)
    ("e^x",    np.exp, miExp,   -2,   3,         None,    ""),
    ("sin(x)", np.sin, miSin,   0,    2 * np.pi, 3,       "rad"),
    ("cos(x)", np.cos, miCos,   0,    2 * np.pi, 3,       "rad"),
    ("tan(x)", np.tan, miTan,   0,    2 * np.pi, 5,       "rad"),
    ("ln(x)",  np.log, miLn,    0.1,  3,         3,       ""),
]


def graficarTodasJuntas(numFigura, numTerminos, numPuntos):
    """Un solo subplot con las cinco funciones reales (continuas) y sus aproximaciones
    de numTerminos términos (discontinuas), cada una en su dominio y del mismo color."""
    plt.figure(numFigura, figsize=(11, 7))
    plt.subplot(1, 1, 1)
    plt.title(f"Funciones reales vs. series de Taylor (N = {numTerminos} términos)")
    for nombre, fReal, fTaylor, xMin, xMax, _, _ in FUNCIONES:
        x = np.linspace(xMin, xMax, numPuntos)
        linea, = plt.plot(x, fReal(x), linewidth=2, label=f"{nombre} real")
        plt.plot(x, fTaylor(x, numTerminos).astype(float), "--", color=linea.get_color(),
                 label=f"{nombre} Taylor")
    # Límites de convergencia: más allá de estas rectas las series de tan y ln divergen
    plt.axvline(np.pi / 2, color="gray", linestyle=":", label="x = pi/2 (límite de tan)")
    plt.axvline(2, color="gray", linestyle="-.", label="x = 2 (límite de ln)")
    plt.ylim(-4, 6)
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.legend(fontsize=8, ncol=2)
    plt.grid(True)
    plt.tight_layout()


def graficarComparacion(numFigura, nombre, fReal, fTaylor, xMin, xMax, limiteY=None, unidadX=""):
    """Figura 3x2: por cada resolución, real vs. aproximaciones y su error absoluto.
    limiteY recorta el eje Y de la columna izquierda (útil si la función se dispara)."""
    etiquetaX = f"x ({unidadX})" if unidadX else "x"
    plt.figure(numFigura, figsize=(11, 9))
    for fila, numPuntos in enumerate(RESOLUCIONES):
        x = np.linspace(xMin, xMax, numPuntos)
        yReal = fReal(x)

        plt.subplot(3, 2, 2 * fila + 1)
        plt.title(f"{nombre}: real vs. Taylor ({numPuntos} puntos)")
        plt.plot(x, yReal, "k", linewidth=2, label=f"{nombre} real")
        for N in TERMINOS:
            plt.plot(x, fTaylor(x, N).astype(float), "--", label=f"N = {N}")
        if limiteY is not None:
            plt.ylim(-limiteY, limiteY)
        plt.xlabel(etiquetaX)
        plt.ylabel("f(x)")
        plt.legend(fontsize=8)
        plt.grid(True)

        plt.subplot(3, 2, 2 * fila + 2)
        plt.title(f"Error absoluto ({numPuntos} puntos)")
        for N in TERMINOS:
            error = np.abs(yReal - fTaylor(x, N).astype(float))
            plt.semilogy(x, error, "o-", markersize=3, label=f"N = {N}")
            if numPuntos == RESOLUCIONES[-1]:
                print(f"{nombre:6s} | N = {N} | error máx vs. NumPy = {error.max():.2e}")
        plt.xlabel(etiquetaX)
        plt.ylabel("|f(x) - P_N(x)|  (escala log)")
        plt.legend(fontsize=8)
        plt.grid(True, which="both")

    plt.tight_layout()


# Figura 1: comparativa directa de las cinco funciones en un mismo subplot
graficarTodasJuntas(1, TERMINOS[-1], RESOLUCIONES[-1])

# Figuras 2 a 6: detalle por función (resolución, número de términos y error)
for i, (nombre, fReal, fTaylor, xMin, xMax, limiteY, unidadX) in enumerate(FUNCIONES):
    graficarComparacion(i + 2, nombre, fReal, fTaylor, xMin, xMax, limiteY, unidadX)

if __name__ == "__main__":
    plt.show()

# =============================================================================
# Conclusión técnica:
# =============================================================================
# Una serie de Taylor truncada es un polinomio muy preciso cerca de su centro (x0 = 0, o 1
# en ln) que pierde precisión al alejarse. e^x, sin y cos convergen en todo R: con N = 8 el
# error máximo frente a NumPy baja a ~0.24, ~0.09 y ~0.25, aunque no de forma monótona
# (en cos, N = 4 es peor que N = 2 cerca de 2*pi). tan y ln tienen radio de convergencia
# finito (pi/2 y 1): lejos del borde, N = 8 da errores < 1e-3, pero fuera más términos
# empeoran el resultado (tan llega a ~1e9 y ln a ~20). Por eso el dominio debe
# justificarse según la función. El número de puntos no cambia la precisión, solo la
# resolución: con 5 puntos las muestras caen en las asíntotas de tan y la gráfica engaña.
