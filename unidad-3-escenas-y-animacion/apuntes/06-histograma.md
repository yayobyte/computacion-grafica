# 6. Histograma de una imagen

## 6.1 Qué es (Diapositivas 35–36)

El histograma es una representación gráfica de **cómo se distribuyen los niveles de intensidad** (brillo) de los píxeles. Ignora **dónde** está cada píxel y solo cuenta **cuántos** hay de cada valor.

- En escala de grises, cada píxel tiene una intensidad entre **0 (negro)** y **255 (blanco)**.
- El histograma **cuenta cuántos píxeles tienen cada nivel**.
- En imágenes a color se calcula **un histograma por canal** (rojo, verde y azul).

## 6.2 Qué muestra y para qué sirve (Diapositiva 37)

- **Eje X:** niveles de intensidad, de 0 a 255.
- **Eje Y:** número de píxeles con ese nivel (o el porcentaje del total).

| Si el histograma… | La imagen es… |
| --- | --- |
| Se concentra a la **izquierda** | Oscura (subexpuesta) |
| Se concentra a la **derecha** | Clara (sobreexpuesta) |
| Ocupa un **rango estrecho** | De **bajo contraste** |
| Se extiende de 0 a 255 | De buen contraste |
| Tiene **dos montañas** (bimodal) | Probablemente un objeto sobre un fondo, fácil de binarizar con el umbral en el valle |
| Tiene un pico pegado a 0 o a 255 | Con zonas saturadas (detalle perdido) |

**Usos:** analizar el brillo, evaluar el contraste y **corregir imágenes**: ajustar brillo, contraste y exposición, y hacer **ecualización de histograma**.

### Efecto de las operaciones de la unidad sobre el histograma

| Operación | Efecto en el histograma |
| --- | --- |
| Brillo `+b` | Se **desplaza** a la derecha (a la izquierda si `b < 0`); lo que pasa de 255 se acumula en 255 |
| Negativo | Se **refleja** horizontalmente |
| Contraste logarítmico | **Estira** la parte izquierda (oscuros) y comprime la derecha |
| Contraste exponencial | Estira la parte derecha (claros) y comprime la izquierda |
| Binarización | Queda en **dos barras**: 0 y 1 |
| Reducción de resolución | Forma parecida, con menos píxeles en total |

## 6.3 Histograma con `plt.hist` por canal (Diapositiva 38)

```python
import numpy as np
import matplotlib.pyplot as plt

img = plt.imread('imagen.jpg')

# Asegurar que los valores estén entre 0 y 255
if img.max() <= 1.0:
    img = (img * 255).astype(np.uint8)

# Separar canales
R = img[..., 0]
G = img[..., 1]
B = img[..., 2]

plt.figure(figsize=(10, 6))

plt.subplot(3, 1, 1)
plt.hist(R.ravel(), bins=256, color='red', alpha=0.7)
plt.title('Histograma del canal Rojo'); plt.xlabel('Intensidad'); plt.ylabel('Frecuencia')

plt.subplot(3, 1, 2)
plt.hist(G.ravel(), bins=256, color='green', alpha=0.7)
plt.title('Histograma del canal Verde'); plt.xlabel('Intensidad'); plt.ylabel('Frecuencia')

plt.subplot(3, 1, 3)
plt.hist(B.ravel(), bins=256, color='blue', alpha=0.7)
plt.title('Histograma del canal Azul'); plt.xlabel('Intensidad'); plt.ylabel('Frecuencia')

plt.tight_layout()
plt.show()
```

- `ravel()` **aplana** la matriz 2D a un vector de `alto × ancho` valores. `plt.hist` necesita una lista de datos, no una matriz.
- `bins=256` crea una barra por nivel posible.
- `alpha=0.7` aplica transparencia. Permite superponer los tres canales en un solo gráfico si se omiten los `subplot`.
- La condición `img.max() <= 1.0` detecta imágenes que vienen normalizadas (como un PNG) y las lleva a 0–255.

## 6.4 Histograma propio (Diapositiva 39)

Construye el conteo a mano, con opción de mostrarlo en porcentaje:

```python
def mhist(RGB, tipo='n', color='gray'):
    """
    Grafica el histograma de una imagen.

    Parámetros:
    - RGB: imagen en escala de grises o un canal (2D array)
    - tipo: 'p' para porcentaje, 'n' para conteo absoluto
    - color: color del histograma (ej. 'red', 'green', 'blue', 'gray')
    """
    formato = tipo.lower()
    filas, columnas = RGB.shape[:2]

    if formato == 'p':
        factor = (filas * columnas) / 100   # para mostrar en porcentaje
    else:
        factor = 1                          # para mostrar en conteo

    histograma = np.zeros(256)
    for nivel in range(256):
        histograma[nivel] = np.sum(RGB == nivel) / factor

    plt.bar(np.arange(256), histograma, color=color, width=1)
    plt.title("Histograma")
    plt.xlabel("Nivel de Intensidad (0-255)")
    plt.ylabel("Porcentaje" if formato == 'p' else "Frecuencia")
    plt.xlim([0, 255])
    plt.tight_layout()
    plt.show()

# Ejemplo de uso
img = plt.imread('imagen.jpg')
if img.max() <= 1.0:
    img = (img * 255).astype(np.uint8)
if img.ndim == 3:                           # convertir a gris si es RGB
    gray = np.dot(img[..., :3], [0.299, 0.587, 0.114]).astype(np.uint8)
else:
    gray = img

mhist(gray, tipo='p', color='gray')         # en porcentaje
# mhist(gray, tipo='n', color='blue')       # en número de píxeles
```

**Cómo funciona:**

- `RGB == nivel` produce una matriz booleana con `True` donde el píxel vale `nivel`. `np.sum` cuenta los `True`.
- **Porcentaje:** se divide por `total/100`, así que las barras suman 100.
- `plt.bar(..., width=1)` dibuja barras contiguas, sin separación.
- **Requisito:** la imagen debe ser **entera de 0 a 255**. Con una imagen normalizada en [0, 1], `RGB == nivel` solo acertaría en 0 y 1. Por eso el ejemplo convierte antes con `* 255` y `astype(np.uint8)`.

### Equivalentes más rápidos

El ciclo recorre la imagen 256 veces. Verifiqué que estas dos formas dan exactamente el mismo conteo que `mhist` sobre una foto de prueba:

```python
histograma = np.bincount(gray.ravel(), minlength=256)                 # una sola pasada
histograma, bordes = np.histogram(gray, bins=256, range=(0, 256))
```

## 6.5 Ecualización de histograma

La Diapositiva 37 la menciona como uso del histograma. No hay código en la presentación. La idea es **redistribuir las intensidades** para que el histograma ocupe todo el rango de forma lo más uniforme posible, lo que aumenta el contraste global. Se usa la distribución acumulada (CDF) como función de transformación:

```python
hist = np.bincount(gray.ravel(), minlength=256)
cdf = hist.cumsum() / hist.sum()                 # acumulada normalizada en [0, 1]
ecualizada = (cdf[gray] * 255).astype(np.uint8)  # cada nivel se reemplaza por su CDF
```

`cdf[gray]` es *fancy indexing*: usa cada píxel como índice en la tabla `cdf`, así que la transformación se aplica a toda la imagen sin ciclos.

> Recuerda la infografía: **mezclar no es ecualizar**. La "imagen fusionada y ecualizada" de la Diapositiva 16 es una mezcla ponderada.

## 6.6 Termografía (infografía)

La infografía cierra el análisis con la **termografía**: una imagen en falso color donde la intensidad representa **temperatura**. Su advertencia es convertir los valores a temperatura **según el modelo del ejercicio, no con una regla universal**. La relación intensidad → °C depende de la cámara y de la escala que defina el enunciado. Para visualizar una matriz de intensidades como mapa de calor:

```python
plt.imshow(gris, cmap='jet')    # o 'inferno', 'hot'
plt.colorbar(label='Temperatura (°C)')
```

Ninguna de las fuentes trae el modelo de conversión; habrá que tomarlo del enunciado del taller.

## Preguntas para sustentar

- **¿Qué información pierde el histograma?** La posición de los píxeles. Dos imágenes muy distintas pueden tener el mismo histograma.
- **¿Cómo se ve en el histograma una imagen de bajo contraste?** Como un histograma concentrado en un rango estrecho.
- **¿Por qué se usa `ravel()`?** Porque `plt.hist` espera una secuencia de valores, no una matriz.
- **¿Por qué `mhist` necesita la imagen en 0–255 enteros?** Porque compara con igualdad exacta contra los niveles enteros 0…255.
