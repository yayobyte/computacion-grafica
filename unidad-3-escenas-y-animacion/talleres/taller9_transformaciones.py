"""
Taller 9 - Transformaciones (Computación Gráfica, UTP).
"""

import numpy as np
import matplotlib.pyplot as plt

import procesamiento_imagenes as pi

IMAGEN = "imagenes/formula1.jpg"
LADO_MAXIMO_ZOOM = 2000  # píxeles por lado del resultado del zoom
COLORES_CANALES = ("red", "green", "blue")


# =============================================================================
# LÓGICA (funciones puras: no leen ni imprimen)
# =============================================================================

def ajustarBrillo(imagen, factor):
    """Punto 1: suma el factor a todos los canales y recorta a [0, 1]."""
    return np.clip(imagen + factor, 0, 1)


def ajustarBrilloCanal(imagen, canal, factor):
    """Punto 2: suma el factor solo al canal indicado (0=R, 1=G, 2=B)."""
    resultado = np.copy(imagen)
    resultado[:, :, canal] = np.clip(imagen[:, :, canal] + factor, 0, 1)
    return resultado


def ajustarContraste(imagen, factor):
    """Punto 3: estira (factor > 1) o comprime (factor < 1) alrededor de 0.5."""
    return np.clip((imagen - 0.5) * factor + 0.5, 0, 1)


def ampliarRegion(imagen, filaInicio, filaFin, columnaInicio, columnaFin, factor):
    """Punto 4: recorta la región y repite cada píxel en un bloque factor×factor."""
    recorte = imagen[filaInicio:filaFin, columnaInicio:columnaFin]
    bloque = np.ones((factor, factor, 1)) if recorte.ndim == 3 else np.ones((factor, factor))
    return np.kron(recorte, bloque)


def binarizar(imagen, umbral):
    """Punto 5: 1 donde el gris por luminosidad es >= umbral, 0 en otro caso."""
    gris = pi.grisLuminosidad(imagen) if imagen.ndim == 3 else imagen
    return (gris >= umbral).astype(float)


def rotarImagen(imagen, grados):
    """Punto 6: rota la imagen en sentido antihorario usando mapeo inverso.

    Para cada píxel del lienzo de salida se calcula de qué píxel del original
    viene (rotación con -θ). Así no quedan huecos en la imagen rotada.
    """
    theta = np.radians(grados)
    cosT, senT = np.cos(theta), np.sin(theta)
    alto, ancho = imagen.shape[:2]

    # Lienzo que contiene la imagen rotada completa
    nuevoAlto = int(np.ceil(abs(alto * cosT) + abs(ancho * senT)))
    nuevoAncho = int(np.ceil(abs(ancho * cosT) + abs(alto * senT)))

    # Coordenadas de cada píxel destino, relativas al centro del lienzo
    filas, columnas = np.indices((nuevoAlto, nuevoAncho))
    y = filas - nuevoAlto / 2
    x = columnas - nuevoAncho / 2

    # Mapeo inverso (el eje y apunta hacia abajo, por eso estos signos)
    xOrigen = np.round(cosT * x - senT * y + ancho / 2).astype(int)
    yOrigen = np.round(senT * x + cosT * y + alto / 2).astype(int)

    dentro = (xOrigen >= 0) & (xOrigen < ancho) & (yOrigen >= 0) & (yOrigen < alto)
    rotada = np.zeros((nuevoAlto, nuevoAncho) + imagen.shape[2:], dtype=imagen.dtype)
    rotada[filas[dentro], columnas[dentro]] = imagen[yOrigen[dentro], xOrigen[dentro]]
    return rotada


def calcularHistograma(capa):
    """Punto 7: cuántos píxeles tiene cada nivel 0-255 en una capa en [0, 1]."""
    niveles = np.round(capa * 255).astype(np.uint8)
    return np.bincount(niveles.ravel(), minlength=256)


# =============================================================================
# PRESENTACIÓN
# =============================================================================

def graficarHistogramasCapas(imagen):
    """Punto 7: figura con la imagen y el histograma de cada capa RGB."""
    plt.figure("Punto 7 - Histograma por capas", figsize=(14, 4))
    plt.subplot(1, 4, 1)
    plt.imshow(imagen)
    plt.title("Imagen")
    plt.axis("off")
    for canal in range(3):
        histograma = calcularHistograma(imagen[:, :, canal])
        plt.subplot(1, 4, canal + 2)
        plt.bar(np.arange(256), histograma, width=1, color=COLORES_CANALES[canal])
        plt.title(f"Histograma capa {pi.NOMBRES_CANALES[canal].lower()}")
        plt.xlabel("Nivel de intensidad (0-255)")
        plt.ylabel("Número de píxeles")
        plt.xlim(0, 255)
    plt.tight_layout()
    plt.show()


# =============================================================================
# OPCIONES DEL MENÚ
# =============================================================================

def opcionBrillo():
    factor = pi.leerNumero("  Factor de brillo (-1 a 1; positivo aclara): ", minimo=-1, maximo=1)
    imagen = pi.leerImagen(IMAGEN)
    pi.mostrarImagenes("Punto 1 - Ajuste de brillo",
                       [(imagen, "Original"), (ajustarBrillo(imagen, factor), f"Brillo {factor:+g}")])


def opcionBrilloCanal():
    canal = int(pi.leerOpcion("  Canal (0 = rojo, 1 = verde, 2 = azul): ", ["0", "1", "2"]))
    factor = pi.leerNumero("  Factor de brillo (-1 a 1; positivo aclara): ", minimo=-1, maximo=1)
    imagen = pi.leerImagen(IMAGEN)
    pi.mostrarImagenes("Punto 2 - Brillo por canal",
                       [(imagen, "Original"),
                        (ajustarBrilloCanal(imagen, canal, factor),
                         f"Canal {pi.NOMBRES_CANALES[canal].lower()} {factor:+g}")])


def opcionContraste():
    factor = pi.leerNumero("  Factor de contraste (mayor que 1 aumenta, entre 0 y 1 reduce; máx. 5): ",
                           minimo=0.01, maximo=5)
    imagen = pi.leerImagen(IMAGEN)
    pi.mostrarImagenes("Punto 3 - Ajuste de contraste",
                       [(imagen, "Original"), (ajustarContraste(imagen, factor), f"Contraste ×{factor:g}")])


def leerRegion(alto, ancho):
    """Pide la región del zoom y el factor hasta que formen un recorte válido."""
    print(f"  La imagen mide {alto} filas × {ancho} columnas.")
    while True:
        filaInicio = pi.leerNumero("  Fila inicial: ", True, 0, alto - 1)
        filaFin = pi.leerNumero("  Fila final (exclusiva): ", True, 1, alto)
        columnaInicio = pi.leerNumero("  Columna inicial: ", True, 0, ancho - 1)
        columnaFin = pi.leerNumero("  Columna final (exclusiva): ", True, 1, ancho)
        factor = pi.leerNumero("  Factor de ampliación (2 a 10): ", True, 2, 10)
        if filaFin <= filaInicio or columnaFin <= columnaInicio:
            print("  ✗ El final debe ser mayor que el inicio. Ingresa la región de nuevo.")
        elif max(filaFin - filaInicio, columnaFin - columnaInicio) * factor > LADO_MAXIMO_ZOOM:
            print(f"  ✗ El resultado pasaría de {LADO_MAXIMO_ZOOM} píxeles por lado. "
                  "Usa una región o un factor menor.")
        else:
            return filaInicio, filaFin, columnaInicio, columnaFin, factor


def opcionZoom():
    imagen = pi.leerImagen(IMAGEN)
    filaInicio, filaFin, columnaInicio, columnaFin, factor = leerRegion(*imagen.shape[:2])
    ampliada = ampliarRegion(imagen, filaInicio, filaFin, columnaInicio, columnaFin, factor)
    print(f"  Región de {filaFin - filaInicio}×{columnaFin - columnaInicio} → "
          f"ampliada a {ampliada.shape[0]}×{ampliada.shape[1]} píxeles.")
    pi.mostrarImagenes("Punto 4 - Zoom", [(imagen, "Original"), (ampliada, f"Zoom ×{factor}")])


def opcionBinarizar():
    umbral = pi.leerNumero("  Umbral (0 a 1): ", minimo=0, maximo=1)
    imagen = pi.leerImagen(IMAGEN)
    binaria = binarizar(imagen, umbral)
    print(f"  Píxeles en blanco: {binaria.mean() * 100:.1f} %")
    pi.mostrarImagenes("Punto 5 - Binarización",
                       [(imagen, "Original"), (binaria, f"Binaria (umbral {umbral:g})")])


def opcionRotar():
    grados = pi.leerNumero("  Ángulo en grados (-360 a 360; positivo = antihorario): ",
                           minimo=-360, maximo=360)
    imagen = pi.leerImagen(IMAGEN)
    rotada = rotarImagen(imagen, grados)
    print(f"  Tamaño original {imagen.shape[:2]} → rotada {rotada.shape[:2]}")
    pi.mostrarImagenes("Punto 6 - Rotación", [(imagen, "Original"), (rotada, f"Rotada {grados:g}°")])


def opcionHistogramas():
    graficarHistogramasCapas(pi.leerImagen(IMAGEN))


OPCIONES = {
    "1": ("Ajustar el brillo", opcionBrillo),
    "2": ("Ajustar el brillo de un canal", opcionBrilloCanal),
    "3": ("Ajustar el contraste", opcionContraste),
    "4": ("Zoom a una parte de la imagen", opcionZoom),
    "5": ("Binarizar la imagen", opcionBinarizar),
    "6": ("Rotar la imagen", opcionRotar),
    "7": ("Histograma de cada capa", opcionHistogramas),
}


if __name__ == "__main__":
    try:
        pi.ejecutarMenu("TALLER 9 · TRANSFORMACIONES", OPCIONES)
    except (KeyboardInterrupt, EOFError):
        print("\n\nPrograma interrumpido. ¡Hasta luego!")
