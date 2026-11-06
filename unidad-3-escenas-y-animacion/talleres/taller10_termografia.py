"""
Taller 10 - Imágenes termográficas (Computación Gráfica, UTP).
"""

import numpy as np
import matplotlib.pyplot as plt

import procesamiento_imagenes as pi

TEM_MIN = -40     # °C
TEM_MAX = 160     # °C
N_BITS = 14
IMAGENES_TERMICAS = {
    "1": "FLIR_00088.tiff",
    "2": "FLIR_00641.tiff",
    "3": "FLIR_02399.tiff",
    "4": "FLIR_06983.tiff",
}
BINS_HISTOGRAMA = 200


# =============================================================================
# LÓGICA (funciones puras: no leen ni imprimen)
# =============================================================================

def convertirACentigrados(datos):
    """Convierte la matriz de la cámara (0 a 2^14) a grados centígrados."""
    return (TEM_MAX - TEM_MIN) * datos.astype(float) / 2 ** N_BITS + TEM_MIN


def ubicarPunto(matriz, indicePlano):
    """Convierte un índice del arreglo aplanado en coordenadas (x, y)."""
    fila, columna = np.unravel_index(indicePlano, matriz.shape)
    return int(columna), int(fila)


def calcularModa(matriz):
    """Valor que más se repite y cuántas veces aparece."""
    valores, conteos = np.unique(matriz, return_counts=True)
    posicion = np.argmax(conteos)
    return valores[posicion], conteos[posicion]


def calcularEstadisticas(MatrizCenti):
    """Punto 1: estadísticas de la matriz en °C, en un diccionario."""
    moda, repeticionesModa = calcularModa(MatrizCenti)
    maximo, minimo = MatrizCenti.max(), MatrizCenti.min()
    return {
        "promedio": MatrizCenti.mean(),
        "mediana": np.median(MatrizCenti),
        "moda": moda,
        "repeticionesModa": repeticionesModa,
        "maximo": maximo,
        "puntoMaximo": ubicarPunto(MatrizCenti, np.argmax(MatrizCenti)),
        "empatesMaximo": int(np.sum(MatrizCenti == maximo)),
        "minimo": minimo,
        "puntoMinimo": ubicarPunto(MatrizCenti, np.argmin(MatrizCenti)),
        "empatesMinimo": int(np.sum(MatrizCenti == minimo)),
    }


# =============================================================================
# PRESENTACIÓN
# =============================================================================

def mostrarDimensiones(MatrizCenti):
    """Filas, columnas y capas con shape (una imagen 2D tiene 1 capa)."""
    filas, columnas = MatrizCenti.shape[:2]
    capas = MatrizCenti.shape[2] if MatrizCenti.ndim == 3 else 1
    print(f"  Dimensiones: {filas} filas, {columnas} columnas, {capas} capa(s)")


def mostrarEstadisticas(estadisticas):
    e = estadisticas
    print(f"  Temperatura promedio: {e['promedio']:.2f} °C")
    print(f"  Temperatura mediana:  {e['mediana']:.2f} °C")
    print(f"  Temperatura moda:     {e['moda']:.2f} °C ({e['repeticionesModa']} píxeles)")
    x, y = e["puntoMaximo"]
    print(f"  Temperatura máxima:   {e['maximo']:.2f} °C en el punto (x={x}, y={y})"
          + (f" — {e['empatesMaximo']} píxeles con ese valor" if e["empatesMaximo"] > 1 else ""))
    x, y = e["puntoMinimo"]
    print(f"  Temperatura mínima:   {e['minimo']:.2f} °C en el punto (x={x}, y={y})"
          + (f" — {e['empatesMinimo']} píxeles con ese valor" if e["empatesMinimo"] > 1 else ""))


def graficarTermografia(MatrizCenti, nombreArchivo, marcarMaximo=False, marcarMinimo=False):
    """Puntos 2 a 4: imagen térmica con escala en °C e histograma.

    Opcionalmente marca el máximo (círculo magenta) y el mínimo (rombo cian).
    """
    plt.figure("Imagen Termográfica", figsize=(13, 5))

    plt.subplot(1, 2, 1)
    plt.imshow(MatrizCenti, cmap="hot_r")
    plt.colorbar(label="Temperatura (°C)")
    if marcarMaximo:
        x, y = ubicarPunto(MatrizCenti, np.argmax(MatrizCenti))
        plt.plot(x, y, "o", color="magenta", markersize=10, label=f"Máx {MatrizCenti.max():.2f} °C")
    if marcarMinimo:
        x, y = ubicarPunto(MatrizCenti, np.argmin(MatrizCenti))
        plt.plot(x, y, "D", color="cyan", markersize=10, label=f"Mín {MatrizCenti.min():.2f} °C")
    if marcarMaximo or marcarMinimo:
        plt.legend(loc="lower right")
    plt.title(f"Imagen termográfica ({nombreArchivo})")
    plt.xlabel("x (columna)")
    plt.ylabel("y (fila)")

    plt.subplot(1, 2, 2)
    conteos, bordes = np.histogram(MatrizCenti, bins=BINS_HISTOGRAMA)
    plt.hist(bordes[:-1], bins=bordes, weights=conteos, color="tab:green", alpha=0.7)
    plt.title("Histograma de temperaturas")
    plt.xlabel("Temperatura (°C)")
    plt.ylabel("Número de píxeles")

    plt.tight_layout()
    plt.show()


# =============================================================================
# OPCIONES DEL MENÚ
# =============================================================================

def elegirImagen():
    """Pide cuál de las imágenes FLIR analizar y retorna (nombre, MatrizCenti)."""
    print("Imágenes termográficas disponibles:")
    for clave, nombre in IMAGENES_TERMICAS.items():
        print(f"  {clave}. {nombre}")
    clave = pi.leerOpcion(f"Elige una imagen (1-{len(IMAGENES_TERMICAS)}): ", list(IMAGENES_TERMICAS))
    nombre = IMAGENES_TERMICAS[clave]
    datos = plt.imread(pi.rutaRecurso(nombre))
    return nombre, convertirACentigrados(datos)


def crearOpciones(nombre, MatrizCenti):
    """Arma el menú con la imagen elegida."""
    def opcionEstadisticas():
        print(f"\n  Imagen: {nombre}")
        mostrarDimensiones(MatrizCenti)
        mostrarEstadisticas(calcularEstadisticas(MatrizCenti))

    return {
        "1": ("Estadísticas de temperatura (promedio, mediana, moda, máx, mín)", opcionEstadisticas),
        "2": ("Figura: imagen termográfica e histograma",
              lambda: graficarTermografia(MatrizCenti, nombre)),
        "3": ("Figura con el punto máximo (círculo magenta)",
              lambda: graficarTermografia(MatrizCenti, nombre, marcarMaximo=True)),
        "4": ("Figura con el máximo y el mínimo (rombo cian)",
              lambda: graficarTermografia(MatrizCenti, nombre, marcarMaximo=True, marcarMinimo=True)),
    }


if __name__ == "__main__":
    try:
        nombreImagen, MatrizCenti = elegirImagen()
        pi.ejecutarMenu(f"TALLER 10 · IMÁGENES TERMOGRÁFICAS ({nombreImagen})",
                        crearOpciones(nombreImagen, MatrizCenti))
    except (KeyboardInterrupt, EOFError):
        print("\n\nPrograma interrumpido. ¡Hasta luego!")
