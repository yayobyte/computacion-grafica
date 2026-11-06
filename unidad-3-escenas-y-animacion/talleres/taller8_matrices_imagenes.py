"""
Taller 8 - Manejo de matrices y procesamiento de imágenes (Computación Gráfica, UTP).
"""

import numpy as np

import procesamiento_imagenes as pi

IMAGEN_PRINCIPAL = "imagenes/formula1.jpg"
IMAGEN_FUSION_A = "imagenes/Dubai1.jpg"
IMAGEN_FUSION_B = "imagenes/Dubai2.jpg"

# Punto 1: cian, blanco, rojo / magenta, gris, verde / amarillo, negro, azul
COLORES_MATRIZ = [
    [(0, 1, 1), (1, 1, 1), (1, 0, 0)],
    [(1, 0, 1), (0.5, 0.5, 0.5), (0, 1, 0)],
    [(1, 1, 0), (0, 0, 0), (0, 0, 1)],
]

# Punto 2: colores (0-255) tomados de la figura del enunciado
OLIVA, TURQUESA, VERDE = (152, 152, 47), (67, 150, 151), (67, 150, 42)
PURPURA, GRANATE, AZUL_OSCURO = (139, 26, 147), (139, 26, 16), (0, 0, 146)
GRISES = [(g, g, g) for g in (152, 137, 117, 97, 77, 47, 27)]
NEGRO = (0, 0, 0)
FILA_SUPERIOR = [OLIVA] + [c for c in (TURQUESA, VERDE, PURPURA, GRANATE, AZUL_OSCURO)
                           for _ in range(2)]                       # 11 bloques
FILA_INFERIOR = GRISES + [NEGRO] * 4                                # 11 bloques
ALTO_BLOQUE_SUPERIOR, ALTO_BLOQUE_INFERIOR, ANCHO_BLOQUE = 300, 100, 50


# =============================================================================
# CONSTRUCCIÓN DE IMÁGENES (puntos 1 y 2)
# =============================================================================

def crearMatrizColores():
    """Punto 1: matriz 3x3 de colores, cada celda de 100x100 píxeles."""
    return pi.crearImagenDesdeColores(COLORES_MATRIZ, 100, 100)


def crearBarrasDeColor():
    """Punto 2: barras de color. Las dos filas tienen altos distintos (3:1),
    así que se construyen por separado y se apilan con np.vstack."""
    superior = pi.crearImagenDesdeColores([FILA_SUPERIOR], ALTO_BLOQUE_SUPERIOR, ANCHO_BLOQUE)
    inferior = pi.crearImagenDesdeColores([FILA_INFERIOR], ALTO_BLOQUE_INFERIOR, ANCHO_BLOQUE)
    return np.vstack([superior, inferior]) / 255


# =============================================================================
# OPCIONES DEL MENÚ
# =============================================================================

def opcionMatriz():
    imagen = crearMatrizColores()
    print(f"  Matriz de forma {imagen.shape}: 3x3 celdas de 100x100 píxeles.")
    pi.mostrarImagenes("Punto 1 - Matriz de colores", [(imagen, "Matriz 3x3")])


def opcionBarras():
    imagen = crearBarrasDeColor()
    print(f"  Imagen de barras de forma {imagen.shape} (alto, ancho, canales).")
    pi.mostrarImagenes("Punto 2 - Barras de color", [(imagen, "Barras de color")])


def mostrarTransformacion(tituloVentana, funcion, subtitulo):
    """Aplica una función de una imagen y la muestra junto a la original."""
    original = pi.leerImagen(IMAGEN_PRINCIPAL)
    pi.mostrarImagenes(tituloVentana, [(original, "Original"), (funcion(original), subtitulo)])


def opcionReconstruir():
    original = pi.leerImagen(IMAGEN_PRINCIPAL)
    capaR, capaG, capaB = pi.capaRoja(original), pi.capaVerde(original), pi.capaAzul(original)
    reconstruida = pi.reconstruirRGB(capaR, capaG, capaB)
    print(f"  ¿La reconstrucción es igual a la original? {np.allclose(reconstruida, original)}")
    pi.mostrarImagenes("Punto 10 - Reconstrucción RGB",
                       [(capaR, "Capa roja"), (capaG, "Capa verde"),
                        (capaB, "Capa azul"), (reconstruida, "Reconstruida")], columnas=4)


def mostrarFusion(tituloVentana, resultado, subtitulo, imagenA, imagenB):
    pi.mostrarImagenes(tituloVentana, [(imagenA, "Imagen A"), (imagenB, "Imagen B"),
                                       (resultado, subtitulo)])


def opcionFusionSinEcualizar():
    imagenA, imagenB = pi.leerImagen(IMAGEN_FUSION_A), pi.leerImagen(IMAGEN_FUSION_B)
    mostrarFusion("Punto 11 - Fusión sin ecualizar",
                  pi.fusionarSinEcualizar(imagenA, imagenB), "A + B", imagenA, imagenB)


def opcionFusionEcualizada():
    imagenA, imagenB = pi.leerImagen(IMAGEN_FUSION_A), pi.leerImagen(IMAGEN_FUSION_B)
    mostrarFusion("Punto 12 - Fusión ecualizada",
                  pi.fusionarEcualizada(imagenA, imagenB), "0.5·A + 0.5·B", imagenA, imagenB)


def opcionFusionConFactor():
    factor = pi.leerNumero("  Factor de mezcla (0 = solo B, 1 = solo A): ", minimo=0, maximo=1)
    imagenA, imagenB = pi.leerImagen(IMAGEN_FUSION_A), pi.leerImagen(IMAGEN_FUSION_B)
    mostrarFusion("Punto 13 - Fusión según el factor",
                  pi.fusionarConFactor(imagenA, imagenB, factor),
                  f"{factor:g}·A + {1 - factor:g}·B", imagenA, imagenB)


def opcionAportePromedio():
    original = pi.leerImagen(IMAGEN_PRINCIPAL)
    aporte = pi.aportePromedioPorCanal(original)
    print(f"  ¿La suma de sus canales es el gris por promedio? "
          f"{np.allclose(aporte.sum(axis=2), pi.grisPromedio(original))}")
    pi.mostrarImagenes("Punto 14 - Técnica de promedio",
                       [(original, "Original"), (aporte, "Aporte (R/3, G/3, B/3)")])


OPCIONES = {
    "1": ("Diseñar la matriz de colores", opcionMatriz),
    "2": ("Diseñar la imagen de barras de color", opcionBarras),
    "3": ("Invertir los colores (negativo)",
          lambda: mostrarTransformacion("Punto 3 - Negativo", pi.invertirColores, "Negativo")),
    "4": ("Capa roja",
          lambda: mostrarTransformacion("Punto 4 - Capa roja", pi.capaRoja, "Capa roja")),
    "5": ("Capa verde",
          lambda: mostrarTransformacion("Punto 5 - Capa verde", pi.capaVerde, "Capa verde")),
    "6": ("Capa azul",
          lambda: mostrarTransformacion("Punto 6 - Capa azul", pi.capaAzul, "Capa azul")),
    "7": ("Imagen en magenta",
          lambda: mostrarTransformacion("Punto 7 - Magenta", pi.imagenMagenta, "Magenta")),
    "8": ("Imagen en cian",
          lambda: mostrarTransformacion("Punto 8 - Cian", pi.imagenCian, "Cian")),
    "9": ("Imagen en amarillo",
          lambda: mostrarTransformacion("Punto 9 - Amarillo", pi.imagenAmarillo, "Amarillo")),
    "10": ("Reconstruir la imagen desde sus capas RGB", opcionReconstruir),
    "11": ("Fusión de dos imágenes sin ecualizar", opcionFusionSinEcualizar),
    "12": ("Fusión de dos imágenes ecualizadas", opcionFusionEcualizada),
    "13": ("Fusión ecualizada según un factor", opcionFusionConFactor),
    "14": ("Imagen con la técnica de promedio", opcionAportePromedio),
    "15": ("Escala de grises por promedio",
           lambda: mostrarTransformacion("Punto 15 - Gris (promedio)",
                                         pi.grisPromedio, "Gris por promedio")),
    "16": ("Escala de grises por luminosidad",
           lambda: mostrarTransformacion("Punto 16 - Gris (luminosidad)",
                                         pi.grisLuminosidad, "Gris por luminosidad")),
    "17": ("Escala de grises por tonalidad (midgray)",
           lambda: mostrarTransformacion("Punto 17 - Gris (midgray)",
                                         pi.grisMidgray, "Gris por midgray")),
}


if __name__ == "__main__":
    try:
        pi.ejecutarMenu("TALLER 8 · MATRICES Y PROCESAMIENTO DE IMÁGENES", OPCIONES)
    except (KeyboardInterrupt, EOFError):
        print("\n\nPrograma interrumpido. ¡Hasta luego!")
