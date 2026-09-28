"""
Taller 6 - Análisis numérico y visualización con NumPy y Matplotlib.

Resuelve los 10 puntos del taller en orden: primero los cálculos (puntos 1 a 6) con
sus verificaciones en consola, y luego las gráficas (puntos 7 a 10), que se muestran
al final en tres ventanas.

Archivos de datos requeridos:
    imagen.png  (punto 10) - debe estar en la misma carpeta que este archivo.
                Puede reemplazarse por cualquier imagen .png o .jpg a color.

-------------------------------------------------------------------------------
DECISIONES
-------------------------------------------------------------------------------
- D: 100 números con distribución uniforme en [0, 1) y semilla fija (SEMILLA = 42),
  para que los resultados y las conclusiones sean reproducibles. Para una uniforme en
  [0, 1) la teoría predice media 0.5 y desviación estándar 1/sqrt(12) ~ 0.2887, lo que
  sirve para verificar los resultados.
- Histograma: se usan 8 bins, por la regla de Sturges k = ceil(log2(n) + 1) con
  n = 100. Con pocos bins se pierde la forma de la distribución, y con muchos cada bin
  queda con 1 o 2 datos y la gráfica se vuelve ruido.
- Escala de grises por luminancia: gris = 0.299 R + 0.587 G + 0.114 B. El ojo es más
  sensible al verde, así que un promedio simple (R + G + B) / 3 daría grises menos
  fieles al brillo percibido.

Herramientas: Python 3, NumPy, Matplotlib.
Asistencia de IA: Claude OPUS 5.5 (Anthropic).
"""

import math
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

SEMILLA = 42
RUTA_IMAGEN = Path(__file__).with_name("imagen.png")
PESOS_LUMINANCIA = np.array([0.299, 0.587, 0.114])  # pesos de R, G y B


# =============================================================================
# Utilidades
# =============================================================================

def mostrar(descripcion, valor):
    """Imprime un resultado; si es un arreglo, también su forma y tipo."""
    texto = str(valor).replace("\n", "\n      ")
    print(f"\n  {descripcion}:\n      {texto}")
    if isinstance(valor, np.ndarray):
        print(f"      shape = {valor.shape}, dtype = {valor.dtype}")


def verificar(descripcion, condicion):
    """Muestra el resultado de una verificación con su valor esperado."""
    print(f"      {'✓' if condicion else '✗'} Verificación: {descripcion}")


# =============================================================================
# Puntos 1 a 6: cálculos
# =============================================================================

def punto1CrearMatriz():
    print("\n=== 1) Creación y manipulación de arrays ===")
    # arange(1, 16) genera 1..15 (excluye el 16); reshape los organiza en 3 filas x 5
    matrizA = np.arange(1, 16).reshape(3, 5)
    mostrar("A (3x5)", matrizA)
    verificar("3 x 5 = 15 elementos", matrizA.shape == (3, 5) and matrizA.size == 15)
    return matrizA


def punto2OperacionesBasicas(matrizA):
    print("\n=== 2) Operaciones básicas ===")
    suma = np.sum(matrizA)
    media = np.mean(matrizA)
    producto = np.prod(matrizA)  # 1 * 2 * ... * 15 = 15!
    mostrar("Suma de los elementos de A", suma)
    mostrar("Media de los elementos de A", media)
    mostrar("Producto de los elementos de A", producto)
    verificar("suma = 15 * 16 / 2 = 120", suma == 120)
    verificar("media = 120 / 15 = 8.0", media == 8.0)
    verificar("producto = 15! = 1 307 674 368 000 (cabe en int64 sin desbordarse)",
              producto == math.factorial(15))


def punto3Slicing(matrizA):
    print("\n=== 3) Acceso y slicing ===")
    # Fila 2 -> índice 1. Elementos 2.º y 3.º -> columnas 1 y 2 -> slice 1:3 (excluye el 3)
    seleccion = matrizA[1, 1:3]
    mostrar("2.º y 3.er elemento de la 2.ª fila (A[1, 1:3])", seleccion)
    verificar("la 2.ª fila es [6..10], así que el resultado es [7, 8]",
              np.array_equal(seleccion, [7, 8]))


def punto4IndexacionBooleana(matrizA):
    print("\n=== 4) Indexación booleana ===")
    # La máscara A > 7 tiene la misma forma 3x5; al aplicarla el resultado es 1D
    vectorB = matrizA[matrizA > 7]
    mostrar("B = elementos de A mayores que 7", vectorB)
    verificar("B = [8..15], 8 elementos", np.array_equal(vectorB, np.arange(8, 16)))


def punto5AlgebraLineal():
    print("\n=== 5) Álgebra lineal ===")
    matrizC = np.array([[2, 1, 0],
                        [1, 3, 1],
                        [0, 1, 4]])
    determinante = np.linalg.det(matrizC)
    mostrar("C (3x3)", matrizC)
    mostrar("Determinante de C", round(determinante, 4))
    # Una matriz solo tiene inversa si su determinante es distinto de 0
    if np.isclose(determinante, 0):
        print("      C es singular (det = 0): no tiene inversa.")
        return
    inversa = np.linalg.inv(matrizC)
    mostrar("Inversa de C", np.round(inversa, 4))
    # Cálculo manual por la primera fila: 2(3*4 - 1*1) - 1(1*4 - 1*0) + 0 = 22 - 4 = 18
    verificar("det(C) = 2(12 - 1) - 1(4 - 0) + 0 = 18", np.isclose(determinante, 18))
    verificar("C @ C^-1 = I (identidad 3x3)", np.allclose(matrizC @ inversa, np.eye(3)))


def punto6Estadisticas():
    print("\n=== 6) Estadísticas con NumPy ===")
    generador = np.random.default_rng(SEMILLA)
    datosD = generador.random(100)  # uniforme en [0, 1)
    # Inspección de los datos: forma, rango y valores faltantes
    print(f"\n  Inspección de D: shape = {datosD.shape}, dtype = {datosD.dtype}, "
          f"faltantes (nan) = {np.isnan(datosD).sum()}")
    maximo = np.max(datosD)
    minimo = np.min(datosD)
    media = np.mean(datosD)
    desviacion = np.std(datosD)
    print(f"  Máximo:              {maximo:.4f}")
    print(f"  Mínimo:              {minimo:.4f}")
    print(f"  Media:               {media:.4f}   (teórica 0.5)")
    print(f"  Desviación estándar: {desviacion:.4f}   (teórica 1/sqrt(12) = {1 / math.sqrt(12):.4f})")
    verificar("todos los valores en [0, 1)", minimo >= 0 and maximo < 1)
    verificar("media a menos de 0.1 de la teórica (0.5)", abs(media - 0.5) < 0.1)
    verificar("desviación a menos de 0.05 de la teórica (0.2887)",
              abs(desviacion - 1 / math.sqrt(12)) < 0.05)
    return datosD, media, desviacion


# =============================================================================
# Puntos 7 a 10: gráficas
# =============================================================================

def punto7GraficoSenoCoseno():
    print("\n=== 7) Gráfico básico: seno y coseno ===")
    x = np.linspace(-2 * np.pi, 2 * np.pi, 400)  # 400 puntos para curvas suaves
    seno = np.sin(x)
    coseno = np.cos(x)
    verificar("sin^2(x) + cos^2(x) = 1 en todos los puntos", np.allclose(seno ** 2 + coseno ** 2, 1))

    plt.figure("Punto 7", figsize=(9, 5))
    plt.plot(x, seno, label="sin(x)")
    plt.plot(x, coseno, "--", label="cos(x)")
    # Marcas del eje x en múltiplos de pi/2 para leer la periodicidad
    marcas = np.arange(-2, 2.5, 0.5) * np.pi
    plt.xticks(marcas, ["-2π", "-3π/2", "-π", "-π/2", "0", "π/2", "π", "3π/2", "2π"])
    plt.title("Funciones seno y coseno en [-2π, 2π]")
    plt.xlabel("x (rad)")
    plt.ylabel("f(x) (adimensional)")
    plt.axhline(0, color="gray", linewidth=0.8)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()


def punto8Y9Dispersion(datosD, media, desviacion):
    print("\n=== 8) Dispersión y 9) Histograma de D ===")
    indices = np.arange(datosD.size)
    numeroBins = math.ceil(math.log2(datosD.size) + 1)  # regla de Sturges: 8 para n = 100

    plt.figure("Puntos 8 y 9", figsize=(12, 5))

    # 8. Dispersión: cada punto es (índice, valor). La línea de la media sirve para
    #    comprobar visualmente que el valor calculado pasa por el centro de la nube.
    plt.subplot(1, 2, 1)
    plt.scatter(indices, datosD, s=15, label="D[i]")
    plt.axhline(media, color="red", label=f"media = {media:.3f}")
    plt.axhspan(media - desviacion, media + desviacion, color="red", alpha=0.1,
                label=f"media ± σ (σ = {desviacion:.3f})")
    plt.title("Punto 8: valores de D contra su índice")
    plt.xlabel("Índice i")
    plt.ylabel("D[i] (adimensional)")
    plt.legend(fontsize=8, loc="upper right")
    plt.grid(True)

    # 9. Histograma: plt.hist retorna los conteos por bin, que se verifican abajo
    plt.subplot(1, 2, 2)
    conteos, bordes, _ = plt.hist(datosD, bins=numeroBins, range=(0, 1), edgecolor="black")
    plt.axhline(datosD.size / numeroBins, color="red", linestyle="--",
                label=f"esperado si es uniforme = {datosD.size / numeroBins:.1f}")
    plt.title(f"Punto 9: histograma de D ({numeroBins} bins, regla de Sturges)")
    plt.xlabel("Valor de D (adimensional)")
    plt.ylabel("Frecuencia (cantidad de datos)")
    plt.legend(fontsize=8)
    plt.grid(True, axis="y")
    plt.tight_layout()

    print(f"\n  Bins: {numeroBins}, ancho de cada bin = {bordes[1] - bordes[0]:.3f}")
    print(f"  Conteos por bin: {conteos.astype(int)}")
    # Comprobar que la gráfica corresponde a los datos: mismos conteos que np.histogram
    conteosNumpy, _ = np.histogram(datosD, bins=numeroBins, range=(0, 1))
    verificar("la suma de las barras es 100 (ningún dato queda fuera)", conteos.sum() == datosD.size)
    verificar("las barras coinciden con np.histogram", np.array_equal(conteos, conteosNumpy))


def punto10EscalaDeGrises():
    print("\n=== 10) Manipulación de imágenes ===")
    imagen = plt.imread(RUTA_IMAGEN)
    print(f"\n  Imagen leída: {RUTA_IMAGEN.name}, shape = {imagen.shape}, dtype = {imagen.dtype}")
    # PNG se lee como float en [0, 1]; JPG como uint8 en [0, 255]. Se normaliza a [0, 1].
    if imagen.dtype == np.uint8:
        imagen = imagen / 255.0
    rgb = imagen[..., :3]  # descarta el canal alfa (transparencia) si existe
    # Producto punto de cada píxel (R, G, B) con los pesos: (alto, ancho, 3) @ (3,) -> (alto, ancho)
    grises = rgb @ PESOS_LUMINANCIA
    print(f"  Escala de grises:  shape = {grises.shape}, rango = [{grises.min():.3f}, {grises.max():.3f}]")
    verificar("la imagen gris tiene 2 dimensiones (un solo canal) y el mismo alto x ancho",
              grises.ndim == 2 and grises.shape == rgb.shape[:2])
    verificar("los pesos suman 1, así que el gris queda en [0, 1]",
              np.isclose(PESOS_LUMINANCIA.sum(), 1) and 0 <= grises.min() and grises.max() <= 1)

    plt.figure("Punto 10", figsize=(11, 4.5))
    plt.subplot(1, 2, 1)
    plt.imshow(rgb)
    plt.title("Imagen original (RGB)")
    plt.axis("off")
    plt.subplot(1, 2, 2)
    # vmin y vmax fijan la escala: sin ellos Matplotlib estiraría el contraste
    plt.imshow(grises, cmap="gray", vmin=0, vmax=1)
    plt.title("Escala de grises (luminancia)")
    plt.axis("off")
    plt.tight_layout()


def main():
    matrizA = punto1CrearMatriz()
    punto2OperacionesBasicas(matrizA)
    punto3Slicing(matrizA)
    punto4IndexacionBooleana(matrizA)
    punto5AlgebraLineal()
    datosD, media, desviacion = punto6Estadisticas()
    punto7GraficoSenoCoseno()
    punto8Y9Dispersion(datosD, media, desviacion)
    punto10EscalaDeGrises()
    plt.show()


if __name__ == "__main__":
    main()

# =============================================================================
# INTERPRETACIÓN (conclusiones)
# =============================================================================
# 1. Los cálculos con NumPy coinciden con los manuales: suma de A = 120, media = 8.0,
#    producto = 15! y det(C) = 18. Además, C @ C^-1 da la identidad, lo que confirma
#    que la inversa es correcta.
# 2. D (uniforme en [0, 1), semilla 42) tiene media 0.4867 y desviación 0.2722, cerca
#    de los valores teóricos 0.5 y 0.2887. Con solo 100 datos es normal que se desvíen
#    un poco; con más datos se acercarían a la teoría.
# 3. La gráfica corresponde a los valores calculados: en la dispersión, la línea de la
#    media (0.487) atraviesa el centro de la nube y los puntos llenan todo el rango
#    [0, 1] sin patrón con el índice. En el histograma, las 8 barras suman 100.
# 4. El histograma no es plano (barras entre 6 y 17 frente a 12.5 esperadas): con 100
#    datos, la variación aleatoria por bin es grande. Por eso la forma de una
#    distribución no se debe juzgar con pocas muestras.
# 5. En la escala de grises, el círculo verde queda más claro y el azul más oscuro,
#    aunque en color parecen igual de intensos. Esto refleja los pesos de luminancia
#    (0.587 para G y 0.114 para B), es decir, cómo percibe el brillo el ojo humano.
