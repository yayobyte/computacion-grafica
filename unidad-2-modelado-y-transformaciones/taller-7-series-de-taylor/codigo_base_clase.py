"""
Código base visto en clase (transcripción exacta de las imágenes de referencia).
Muestra el cálculo de factorial recursivo, la aproximación de la función seno mediante
serie de Taylor truncada por tolerancia (aporteMin), vectorizada con np.frompyfunc,
y la visualización comparando la resolución de muestreo (5, 10 y 50 puntos).
"""

import numpy as np
import matplotlib.pyplot as plt
import math


def miFactorial(n):
    if (n == 0 or n == 1):
        fact = 1
    elif (n > 1):
        fact = n * miFactorial(n - 1)
    else:
        return "NaN"
    return fact


def miSin(x):
    suma = 0
    termino = 0
    n = 0
    aporteMin = 0.00001
    while True:
        termino = ((-1)**n) / (miFactorial(2*n + 1)) * x**(2*n + 1)
        suma += termino
        n += 1
        if math.fabs(termino) < aporteMin:
            break
    return suma


# -------------------------------------------------------------
miSin = np.frompyfunc(miSin, 1, 1)

# Primer bloque: 5 puntos
x = np.linspace(0, 2 * np.pi, 5)
y1 = np.sin(x)
y2 = miSin(x)

plt.figure(1, figsize=(10, 8))
plt.subplot(3, 2, 1)
plt.title("Función Seno original (5 puntos)")
plt.plot(x, y1)

plt.subplot(3, 2, 2)
plt.title("Función Seno usando series de Taylor (5 puntos)")
plt.plot(x, y2)

# Segundo bloque: 10 puntos
x = np.linspace(0, 2 * np.pi, 10)
y1 = np.sin(x)
y2 = miSin(x)

plt.subplot(3, 2, 3)
plt.title("Función Seno original (10 puntos)")
plt.plot(x, y1)

plt.subplot(3, 2, 4)
plt.title("Función Seno usando series de Taylor (10 puntos)")
plt.plot(x, y2)

# Tercer bloque: 50 puntos
x = np.linspace(0, 2 * np.pi, 50)
y1 = np.sin(x)
y2 = miSin(x)

plt.subplot(3, 2, 5)
plt.title("Función Seno original (50 puntos)")
plt.plot(x, y1)

plt.subplot(3, 2, 6)
plt.title("Función Seno usando series de Taylor (50 puntos)")
plt.plot(x, y2)

plt.tight_layout()

if __name__ == "__main__":
    plt.show()
