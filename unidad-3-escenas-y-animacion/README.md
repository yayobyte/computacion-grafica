# Unidad 4: Procesamiento de Imágenes Digitales con Geometría Vectorial

Apuntes de la unidad sobre el tratamiento de imágenes como matrices numéricas con NumPy y Matplotlib. Reúnen el resumen ejecutivo de Moodle, la presentación del profesor (Francisco Alejandro Medina), la infografía de la unidad y los dos tutoriales de referencia.

> **Idea central:** una imagen es un arreglo numérico. Cada operación de la unidad (negativo, mezcla, gris, brillo, recorte, rotación, histograma) es una operación de NumPy sobre ese arreglo.

## Ruta de la unidad

Según la infografía: **matrices y canales → operaciones → transformaciones e histogramas → termografía → visor.**

| # | Apunte | Contenido |
| --- | --- | --- |
| 1 | [Imagen digital y lectura](./apuntes/01-imagen-digital-y-lectura.md) | Píxel, resolución, forma `(alto, ancho, 3)`, `dtype`, normalización, convención de ejes, imágenes sintéticas |
| 2 | [Color: RGB, CMYK y canales](./apuntes/02-color-rgb-cmyk-y-canales.md) | Modelo aditivo y sustractivo, descomposición RGB, capas CMYK, ajuste de un canal, reconstrucción |
| 3 | [Operaciones aritméticas, brillo y contraste](./apuntes/03-operaciones-aritmeticas-brillo-contraste.md) | Negativo, suma, resta, mezcla ponderada, desbordamiento `uint8`, brillo, contraste logarítmico y exponencial |
| 4 | [Escala de grises y binarización](./apuntes/04-escala-de-grises-y-binarizacion.md) | Promedio, luminosidad (Rec. 601), midgray (HSL), umbral |
| 5 | [Transformaciones geométricas](./apuntes/05-transformaciones-geometricas.md) | Traslación, recorte, volteo, rotación, reducción de resolución, ampliación de una región |
| 6 | [Histograma](./apuntes/06-histograma.md) | Qué mide, cómo se interpreta, `plt.hist`, histograma propio por canal y en porcentaje |
| 7 | [Temas avanzados con SciPy](./apuntes/07-scipy-filtros-morfologia-segmentacion.md) | Filtros, ruido, morfología, bordes, segmentación y medición (material de referencia) |

## Chuleta de fórmulas

Notación: `I` es la imagen normalizada a [0, 1] (salvo que se indique 0–255); `R`, `G`, `B` son `I[:, :, 0]`, `I[:, :, 1]`, `I[:, :, 2]`.

| Operación | Fórmula | NumPy |
| --- | --- | --- |
| Normalizar | `I = I₈ / 255` | `img = plt.imread("a.jpg") / 255` |
| Negativo | `N = 1 − I` (o `255 − I`) | `1 - img` |
| Suma | `S = A + B` | `np.clip(a + b, 0, 1)` |
| Mezcla | `F = αA + (1 − α)B`, `0 ≤ α ≤ 1` | `alfa*a + (1-alfa)*b` |
| Brillo | `I' = clip(I + b)` | `np.clip(img + b, 0, 1)` |
| Contraste (oscuras) | `I' = K · log₁₀(1 + I)` | `K*np.log10(1 + img)` |
| Contraste (claras) | `I' = K · exp(I − 1)` | `K*np.exp(img - 1)` |
| Gris promedio | `(R + G + B) / 3` | `img.mean(axis=2)` |
| Gris luminosidad | `0.299R + 0.587G + 0.114B` | `img[..., :3] @ [0.299, 0.587, 0.114]` |
| Gris midgray | `(max + min) / 2` | `(img.max(axis=2) + img.min(axis=2)) / 2` |
| Binarizar | `1 si L ≥ umbral, 0 si no` | `gris >= umbral` |
| Traslación | `(x', y') = (x + Δx, y + Δy)` | asignación por rebanadas |
| Recorte | sub-matriz | `img[f0:f1, c0:c1]` |
| Reducción ×k | 1 de cada k píxeles | `img[::k, ::k]` |
| Ampliación ×k | cada píxel → bloque k×k | `np.kron(rec, np.ones((k, k, 1)))` |
| Histograma | conteo por nivel 0–255 | `np.bincount(gris8.ravel(), minlength=256)` |

## Plantilla base de los ejemplos de clase

Todos los ejemplos de la presentación siguen el mismo esqueleto:

```python
import numpy as np
import matplotlib.pyplot as plt

img1 = plt.imread('Imagen.jpg') / 255      # leer y normalizar a [0, 1]

resultado = 1 - img1                        # ← aquí va la operación

plt.figure("Título de la ventana")
plt.subplot(1, 2, 1); plt.imshow(img1);      plt.axis('off'); plt.title('Original')
plt.subplot(1, 2, 2); plt.imshow(resultado); plt.axis('off'); plt.title('Resultado')
plt.show()
```

## Fuentes

| Fuente | Ubicación | Qué aporta |
| --- | --- | --- |
| Resumen ejecutivo (Moodle) | texto del curso | Definiciones, fórmulas, precaución con `uint8` |
| Presentación del profesor (39 diapositivas) | `InfoUnidad4/Presentación Procesamiento Imagenes.pdf` | Código de clase de cada técnica |
| Infografía IS623 | imagen del curso | Ruta de la unidad, ejemplos numéricos |
| Tutorial de procesamiento de imágenes con NumPy | `InfoUnidad4/Tutorial ... .html` | Imágenes sintéticas, canales, ejercicios |
| Scipy lecture notes 2.6 (Gouillart y Varoquaux) | `InfoUnidad4/2.6 ... .html` | Filtros, morfología, segmentación, medición |

En los apuntes, las referencias "Diapositiva N" remiten a la presentación del profesor.

Navegación: [Inicio](../) | [← Unidad 3](../unidad-3-escenas-y-animacion/)
