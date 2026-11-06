# 1. Imagen digital y lectura

## 1.1 Qué es una imagen

Una **imagen** es una representación esculpida, pintada o fotografiada de un objeto o escena. Hoy se despliega sobre monitores electrónicos como las pantallas LED (Diapositiva 2).

Una **imagen digital** es una celda (arreglo) compuesta por **píxeles** (*picture elements*), las unidades mínimas de información. Cada píxel almacena un valor numérico que representa su color y brillo (Diapositivas 3, 5 y 6).

- **Resolución:** cantidad total de píxeles. Más píxeles implica más información y más detalle.
- **Imagen a color:** 3 valores por píxel (R, G, B).
- **Imagen en escala de grises o blanco y negro:** 1 valor por píxel.

La Diapositiva 5 lo ilustra ampliando una bandera: de cerca, la imagen es una cuadrícula de cuadros de color uniforme.

## 1.2 La imagen como matriz

| Tipo | Forma del arreglo (`shape`) | Acceso a un píxel |
| --- | --- | --- |
| Escala de grises | `(alto, ancho)` | `img[fila, columna]` → un número |
| Color RGB | `(alto, ancho, 3)` | `img[fila, columna]` → `[R, G, B]` |
| Color RGBA (PNG con transparencia) | `(alto, ancho, 4)` | `[R, G, B, A]` |

**Convención de ejes** (infografía y Scipy notes): el primer índice es la **fila** (eje vertical, crece **hacia abajo**) y el segundo es la **columna** (eje horizontal, crece hacia la derecha). El origen `(0, 0)` es la esquina superior izquierda.

```
        columna (x) →
      ┌──────────────
fila  │ (0,0) (0,1) ...
(y)   │ (1,0) (1,1) ...
 ↓    │  ...
```

Por eso `img.shape[:2]` devuelve `(alto, ancho)`, en ese orden, y no `(ancho, alto)`.

## 1.3 Leer y mostrar una imagen (Diapositiva 4)

```python
import numpy as np
import matplotlib.pyplot as plt

img1 = plt.imread('Imagen.jpg') / 255   # normaliza de 0–255 a 0–1

plt.figure("Imagen Original")
plt.imshow(img1)
plt.axis('off')     # oculta los ejes y las marcas
plt.show()
```

- `plt.imread` de un **JPG** devuelve `uint8` con valores 0–255 y forma `(alto, ancho, 3)`. Por ejemplo, `formula1.jpg` es `uint8 (1304, 980, 3)`.
- `plt.imread` de un **PNG** ya devuelve `float32` en [0, 1], a veces con 4 canales (RGBA). **Dividir un PNG por 255 lo deja casi negro.** Se puede comprobar con `img.dtype` y `img.max()`.
- `plt.imread` devuelve un arreglo de **solo lectura** para JPG. `np.array(...)` o `np.copy(...)` crean una copia modificable. Dividir por 255 también crea un arreglo nuevo.
- `/ 255` convierte a `float64`, lo que evita desbordamientos en las operaciones siguientes (ver [apunte 3](./03-operaciones-aritmeticas-brillo-contraste.md#34-precaución-con-imágenes-uint8)).

### Cómo interpreta `imshow` los valores

| Arreglo | Rango esperado | Fuera de rango |
| --- | --- | --- |
| RGB `float` | [0, 1] | Recorta y avisa: *Clipping input data to the valid range* |
| RGB `uint8` | [0, 255] | No puede salir de rango |
| 2D (gris) | Cualquiera | Aplica un **mapa de color** (por defecto *viridis*, morado-amarillo) y estira el contraste entre el mínimo y el máximo |

Para una imagen 2D en gris real:

```python
plt.imshow(gris, cmap='gray', vmin=0, vmax=1)
```

Sin `vmin`/`vmax`, una imagen toda en 0.5 se vería negra o con un color arbitrario, porque matplotlib estira su único valor. El tutorial de NumPy fija `plt.rcParams['image.cmap'] = 'gray'` al inicio para no repetir `cmap`.

### Inspección de detalle

Para ver los píxeles individuales sin suavizado (Scipy notes):

```python
plt.imshow(img[200:220, 200:220], cmap='gray', interpolation='nearest')
```

## 1.4 Imágenes sintéticas: crear matrices y verlas (tutorial de NumPy)

Como cualquier matriz se puede visualizar, se pueden "dibujar" imágenes con NumPy:

```python
tamano = (20, 30)                       # 20 filas × 30 columnas

negra  = np.zeros(tamano)               # todo 0 → negro
blanca = np.ones(tamano)                # todo 1 → blanco
gris   = np.ones(tamano) * 0.5          # todo 0.5 → gris medio
oscuro = np.ones(tamano) * 0.2          # gris oscuro
ruido  = np.random.rand(*tamano)        # intensidad aleatoria por píxel

plt.imshow(gris, cmap='gray', vmin=0, vmax=1)
```

`plt.figure()` crea una figura nueva. Sin ella, cada `imshow` sobrescribe la imagen anterior.

### Ejercicios propuestos en el tutorial

1. Generar una imagen de 20×30 que sea **blanca de la mitad para abajo** y cuya parte de arriba sea **negra a la izquierda y gris a la derecha** (patrón `NG / BB`). Se resuelve con rebanadas (*slicing*) como `img[filas, columnas] = valor`.
2. Construir un **gradiente** de 20×11 donde la columna `k` tenga intensidad `k/10` (de 0 a 1). Se puede resolver con un ciclo o con `np.linspace(0, 1, 11)` y *broadcasting*.

## 1.5 Manipulación directa con NumPy (Scipy notes)

```python
img[0, 40]                 # valor de un píxel
img[10:13, 20:23]          # sub-matriz 3×3 (slicing)
img[100:120] = 255         # pinta de blanco las filas 100 a 119

# Máscara circular: pone en negro todo lo que queda fuera de un círculo
lx, ly = img.shape
X, Y = np.ogrid[0:lx, 0:ly]
mascara = (X - lx/2)**2 + (Y - ly/2)**2 > lx*ly/4
img[mascara] = 0

img[range(400), range(400)] = 255   # fancy indexing: dibuja la diagonal
```

### Estadísticas básicas

```python
img.mean()                 # intensidad promedio
img.max(), img.min()       # extremos
np.histogram(img)          # distribución (ver apunte 6)
```

## 1.6 Guardar imágenes

```python
plt.imsave('salida.png', img)                 # RGB float [0, 1] o uint8
plt.imsave('gris.png', gris, cmap='gray')     # 2D: hay que indicar el mapa
```

El tutorial usa `skimage.io.imread`/`imsave` y las Scipy notes usan `scipy.misc.imread`/`imsave`. `scipy.misc` ya no incluye esas funciones en versiones actuales de SciPy. Con matplotlib basta para lo que pide la unidad, y es la librería que ya está en `requirements.txt`.

## Preguntas para sustentar

- **¿Por qué se divide por 255?** Para pasar de enteros `uint8` (0–255) a reales en [0, 1]. Así las fórmulas no dependen de la escala, y las operaciones no desbordan.
- **¿Qué devuelve `img.shape` para una foto a color?** `(alto, ancho, 3)`: filas, columnas y canales.
- **¿Cuántos colores puede representar una imagen RGB de 8 bits?** 256³ = 16 777 216.
- **¿Por qué una imagen 2D sale morada y amarilla?** Porque `imshow` aplica el mapa de color *viridis*. Hay que pasar `cmap='gray'`.
