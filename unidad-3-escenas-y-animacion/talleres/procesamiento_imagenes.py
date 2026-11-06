"""
Módulo reutilizable de la Unidad 4 - Procesamiento de imágenes.

Uso desde un taller (en la misma carpeta):
    import procesamiento_imagenes as pi
    imagen = pi.leerImagen("imagenes/formula1.jpg")
    pi.mostrarImagenes("Negativo", [(imagen, "Original"), (pi.invertirColores(imagen), "Negativo")])

Herramientas: Python 3, NumPy, Matplotlib.
"""

from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

CARPETA_BASE = Path(__file__).resolve().parent  # carpeta de los talleres

# Pesos del estándar Rec. 601 (NTSC) para la técnica de luminosidad
PESOS_LUMINOSIDAD = np.array([0.299, 0.587, 0.114])

NOMBRES_CANALES = {0: "Rojo", 1: "Verde", 2: "Azul"}


# =============================================================================
# 1. LECTURA Y VALIDACIÓN DE DATOS (adaptadas de los talleres 1 y 2)
# =============================================================================

def convertirNumero(texto, soloEnteros=False):
    """Convierte texto a int o float (acepta coma decimal). Lanza ValueError si no es válido."""
    texto = texto.strip().replace(",", ".")
    if soloEnteros:
        return int(texto)
    return float(texto)


def leerNumero(mensaje, soloEnteros=False, minimo=None, maximo=None):
    """Pide un número hasta que sea válido y esté dentro de [minimo, maximo]."""
    while True:
        try:
            valor = convertirNumero(input(mensaje), soloEnteros)
        except ValueError:
            print("  ✗ Debe ser un número" + (" entero." if soloEnteros else "."))
            continue
        if minimo is not None and valor < minimo:
            print(f"  ✗ El valor no puede ser menor que {minimo}.")
        elif maximo is not None and valor > maximo:
            print(f"  ✗ El valor no puede ser mayor que {maximo}.")
        else:
            return valor


def leerOpcion(mensaje, opcionesValidas):
    """Pide una opción hasta que el usuario escriba una de opcionesValidas."""
    while True:
        opcion = input(mensaje).strip().lower()
        if opcion in opcionesValidas:
            return opcion
        print(f"  ✗ Opción no válida. Elige entre: {', '.join(opcionesValidas)}.")


# =============================================================================
# 2. CARGA DE IMÁGENES
# =============================================================================

def rutaRecurso(nombre):
    """Ruta absoluta de un archivo relativo a la carpeta de los talleres.

    Así los programas funcionan sin importar desde qué carpeta se ejecuten.
    """
    return CARPETA_BASE / nombre


def leerImagen(nombre):
    """Lee una imagen y la retorna normalizada a [0, 1] como float.

    - JPG: plt.imread retorna uint8 (0 a 255), se divide por 255.
    - PNG: plt.imread ya retorna float en [0, 1], no se divide.
    - Si trae canal alfa (RGBA) se descarta y quedan los 3 canales RGB.
    """
    imagen = plt.imread(rutaRecurso(nombre))
    if np.issubdtype(imagen.dtype, np.integer):
        imagen = imagen / np.iinfo(imagen.dtype).max
    else:
        imagen = imagen.astype(float)  # copia modificable
    if imagen.ndim == 3:
        imagen = imagen[:, :, :3]
    return imagen


# =============================================================================
# 3. FUNCIONES DE IMAGEN (Taller 8)
# =============================================================================

# --- Puntos 1 y 2: imágenes construidas desde una matriz ---------------------

def crearImagenDesdeColores(matrizColores, altoCelda, anchoCelda):
    """Construye una imagen donde cada color de la matriz ocupa un bloque.

    matrizColores tiene forma (filas, columnas, 3). Cada celda se repite en un
    bloque de altoCelda x anchoCelda píxeles con np.kron (producto de Kronecker).
    """
    matriz = np.asarray(matrizColores, dtype=float)
    return np.kron(matriz, np.ones((altoCelda, anchoCelda, 1)))


# --- Punto 3: negativo --------------------------------------------------------

def invertirColores(imagen):
    """Negativo de la imagen: cada canal pasa a 1 - valor."""
    return 1 - imagen


# --- Puntos 4, 5 y 6: capas RGB -----------------------------------------------

def extraerCapa(imagen, canal):
    """Retorna una copia donde solo queda el canal indicado (0=R, 1=G, 2=B).

    Los otros dos canales se ponen en 0, que en RGB significa "sin luz".
    """
    capa = np.copy(imagen)
    for otroCanal in range(3):
        if otroCanal != canal:
            capa[:, :, otroCanal] = 0
    return capa


def capaRoja(imagen):
    return extraerCapa(imagen, 0)


def capaVerde(imagen):
    return extraerCapa(imagen, 1)


def capaAzul(imagen):
    return extraerCapa(imagen, 2)


# --- Puntos 7, 8 y 9: capas CMY -----------------------------------------------

def capaTinta(imagen, canalLibre):
    """Capa de tinta (CMY): fija en 1 los dos canales que la tinta no absorbe.

    En CMY el 1 significa "sin tinta" (el papel refleja ese canal). Solo queda
    libre el canal que la tinta absorbe:
        cian -> rojo (0), magenta -> verde (1), amarillo -> azul (2).
    """
    capa = np.copy(imagen)
    for otroCanal in range(3):
        if otroCanal != canalLibre:
            capa[:, :, otroCanal] = 1
    return capa


def imagenMagenta(imagen):
    return capaTinta(imagen, 1)


def imagenCian(imagen):
    return capaTinta(imagen, 0)


def imagenAmarillo(imagen):
    return capaTinta(imagen, 2)


# --- Punto 10: reconstrucción -------------------------------------------------

def reconstruirRGB(capaR, capaG, capaB):
    """Reconstruye la imagen a color sumando las tres capas RGB.

    Cada capa tiene ceros en los canales que no usa, así que la suma deja en
    cada píxel (R, 0, 0) + (0, G, 0) + (0, 0, B) = (R, G, B).
    """
    return capaR + capaG + capaB


# --- Puntos 11, 12 y 13: fusión de dos imágenes ---------------------------------

def validarMismaForma(imagenA, imagenB):
    """Lanza ValueError si las dos imágenes no tienen la misma forma."""
    if imagenA.shape != imagenB.shape:
        raise ValueError(f"Las imágenes deben tener la misma forma: "
                         f"{imagenA.shape} != {imagenB.shape}")


def fusionarSinEcualizar(imagenA, imagenB):
    """Suma simple A + B, recortada a [0, 1].

    Donde la suma pasa de 1 se satura en blanco: por eso se ve "lavada".
    """
    validarMismaForma(imagenA, imagenB)
    return np.clip(imagenA + imagenB, 0, 1)


def fusionarConFactor(imagenA, imagenB, factor):
    """Suma ponderada F = factor*A + (1 - factor)*B, con 0 <= factor <= 1.

    Como los pesos suman 1, el resultado nunca sale de [0, 1].
    """
    validarMismaForma(imagenA, imagenB)
    if not 0 <= factor <= 1:
        raise ValueError("El factor debe estar entre 0 y 1.")
    return imagenA * factor + imagenB * (1 - factor)


def fusionarEcualizada(imagenA, imagenB):
    """Fusión ecualizada: las dos imágenes aportan lo mismo (factor 0.5)."""
    return fusionarConFactor(imagenA, imagenB, 0.5)


# --- Puntos 14 a 17: escala de grises -------------------------------------------

def aportePromedioPorCanal(imagen):
    """Imagen a color con el aporte de cada canal al promedio: (R/3, G/3, B/3).

    Sumar sus tres canales da exactamente el gris por promedio del punto 15.
    """
    return imagen[:, :, :3] / 3


def grisPromedio(imagen):
    """Escala de grises por promedio: (R + G + B) / 3."""
    return (imagen[:, :, 0] + imagen[:, :, 1] + imagen[:, :, 2]) / 3


def grisLuminosidad(imagen):
    """Escala de grises por luminosidad (Rec. 601): 0.299R + 0.587G + 0.114B."""
    return np.dot(imagen[:, :, :3], PESOS_LUMINOSIDAD)


def grisMidgray(imagen):
    """Escala de grises por tonalidad (HSL): (max(R,G,B) + min(R,G,B)) / 2.

    Se usa max/min con axis=2: np.maximum solo compara dos arreglos y su tercer
    argumento es la salida, no un tercer canal.
    """
    canales = imagen[:, :, :3]
    return (canales.max(axis=2) + canales.min(axis=2)) / 2


# =============================================================================
# 4. PRESENTACIÓN
# =============================================================================

def mostrarImagenes(tituloVentana, imagenes, columnas=None):
    """Muestra varias imágenes en una misma figura, una por subplot.

    imagenes es una lista de tuplas (imagen, subtitulo). Las imágenes 2D se
    muestran en gris con escala fija [0, 1], para que no se estire el contraste.
    """
    total = len(imagenes)
    columnas = columnas or min(total, 3)
    filas = int(np.ceil(total / columnas))
    plt.figure(tituloVentana, figsize=(4 * columnas, 3.5 * filas))
    for posicion, (imagen, subtitulo) in enumerate(imagenes, start=1):
        plt.subplot(filas, columnas, posicion)
        if imagen.ndim == 2:
            plt.imshow(imagen, cmap="gray", vmin=0, vmax=1)
        else:
            plt.imshow(np.clip(imagen, 0, 1))
        plt.title(subtitulo)
        plt.axis("off")
    plt.tight_layout()
    plt.show()


# =============================================================================
# 5. MENÚ
# =============================================================================

def ejecutarMenu(titulo, opciones):
    """Ciclo de menú común a los talleres.

    opciones es un diccionario {"1": (descripcion, funcion), ...}. Se agrega
    automáticamente "Salir" como última opción. La opción se valida y se pide
    de nuevo si no es válida.
    """
    claveSalir = str(len(opciones) + 1)
    while True:
        print("\n" + "=" * 60)
        print(f"  {titulo}")
        print("=" * 60)
        for clave, (descripcion, _) in opciones.items():
            print(f"  {clave:>2}. {descripcion}")
        print(f"  {claveSalir:>2}. Salir")
        opcion = leerOpcion(f"Elige una opción (1-{claveSalir}): ",
                            list(opciones) + [claveSalir])
        if opcion == claveSalir:
            print("\n¡Hasta luego!")
            break
        opciones[opcion][1]()
