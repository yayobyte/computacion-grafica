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
    return (fact)


def miCos(x, numTerminos):
    suma = 0
    termino = 0
    n = 0
    while (n < numTerminos):
        termino = ((-1)**n) / (miFactorial(2 * n)) * (x**(2 * n))
        suma += termino
        n += 1
    return (suma)


# -------------------------------------------------------------
miCos = np.frompyfunc(miCos, 2, 1)

# Dominio justificado: [0, 2*pi] con 200 puntos para garantizar curvas suaves
x = np.linspace(0, 2 * np.pi, 200)
y1 = np.cos(x)

plt.figure(1, figsize=(11, 8.5))

# Primer bloque: 1 término
y2_1 = miCos(x, 1)
error_1 = np.abs(y1 - y2_1)

plt.subplot(3, 2, 1)
plt.title("Coseno original vs. Taylor (1 término)")
plt.plot(x, y1, label="cos(x) real")
plt.plot(x, y2_1, "--", label="Taylor (1 térm.)")
plt.ylim(-2.5, 2.5)
plt.legend()
plt.grid(True)

plt.subplot(3, 2, 2)
plt.title("Error absoluto (1 término)")
plt.plot(x, error_1, "r")
plt.grid(True)

# Segundo bloque: 3 términos
y2_3 = miCos(x, 3)
error_3 = np.abs(y1 - y2_3)

plt.subplot(3, 2, 3)
plt.title("Coseno original vs. Taylor (3 términos)")
plt.plot(x, y1, label="cos(x) real")
plt.plot(x, y2_3, "--", label="Taylor (3 térm.)")
plt.ylim(-2.5, 2.5)
plt.legend()
plt.grid(True)

plt.subplot(3, 2, 4)
plt.title("Error absoluto (3 términos)")
plt.plot(x, error_3, "r")
plt.grid(True)

# Tercer bloque: 5 términos
y2_5 = miCos(x, 5)
error_5 = np.abs(y1 - y2_5)

plt.subplot(3, 2, 5)
plt.title("Coseno original vs. Taylor (5 términos)")
plt.plot(x, y1, label="cos(x) real")
plt.plot(x, y2_5, "--", label="Taylor (5 térm.)")
plt.ylim(-2.5, 2.5)
plt.legend()
plt.grid(True)

plt.subplot(3, 2, 6)
plt.title("Error absoluto (5 términos)")
plt.plot(x, error_5, "r")
plt.grid(True)

plt.tight_layout()

if __name__ == "__main__":
    plt.show()

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
