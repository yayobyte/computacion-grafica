# 7. Temas avanzados con SciPy (material de referencia)

Resumen de *Scipy lecture notes, 2.6: Manipulación y procesamiento de imágenes usando Numpy y Scipy* (Emmanuelle Gouillart y Gaël Varoquaux), incluido en `InfoUnidad4/`. **Va más allá de la presentación de clase**: es contexto para profundizar, no algo que la unidad haya pedido implementar.

> **Antes de usarlo:**
>
> - SciPy **no** está en `requirements.txt`. Hay que instalarlo (`.venv/bin/pip install scipy`) y avisar al profesor si se entrega código que lo use.
> - El documento es de 2012–2013. Varias llamadas ya no existen; ver la [tabla de equivalencias](#78-equivalencias-con-versiones-actuales).

## 7.1 Panorama

Imagen = arreglo de NumPy en 2D (o 3D: tomografía, resonancia, 2D + tiempo…). Tareas comunes:

- Entrada, salida y visualización.
- Manipulación básica: recortar, voltear, rotar.
- **Filtrado:** reducción de ruido, enfoque (*sharpening*).
- **Segmentación:** etiquetar píxeles según el objeto al que pertenecen.
- Clasificación, extracción de patrones, registro.

Herramientas: `numpy`, `scipy.ndimage` (procesamiento n-dimensional), `scikit-image` y `scikit-learn`. Hay librerías más completas como **OpenCV**, CellProfiler e ITK.

## 7.2 Filtros locales

Un **filtro local** reemplaza cada píxel por una función de sus **vecinos**. La vecindad puede ser un cuadrado, un círculo u otro elemento estructurante.

### Desenfoque o suavizado

```python
from scipy import ndimage
borrosa      = ndimage.gaussian_filter(img, sigma=3)    # σ mayor → más borroso
muy_borrosa  = ndimage.gaussian_filter(img, sigma=5)
media_local  = ndimage.uniform_filter(img, size=11)     # promedio en ventana 11×11
```

### Enfoque o *sharpening*

Se refuerzan los bordes sumando una aproximación del laplaciano, que es la diferencia entre la imagen y una versión más borrosa de sí misma:

```python
borrosa = ndimage.gaussian_filter(img, 3)
mas_borrosa = ndimage.gaussian_filter(borrosa, 1)
alfa = 30
enfocada = borrosa + alfa * (borrosa - mas_borrosa)
```

## 7.3 Reducción de ruido

```python
ruidosa = img + 0.4 * img.std() * np.random.random(img.shape)

gauss   = ndimage.gaussian_filter(ruidosa, 2)   # quita ruido… y también bordes
mediana = ndimage.median_filter(ruidosa, 3)     # conserva mejor los bordes
```

| Filtro | Tipo | Bordes |
| --- | --- | --- |
| Gaussiano, uniforme | Lineal | Los desenfoca |
| Mediana | No lineal (de rango) | Los conserva, sobre todo los rectos |
| Variación total (TV) | No local | Los conserva; minimiza la integral de la norma L1 del gradiente sin alejarse de los datos |

Otros: `ndimage.maximum_filter`, `ndimage.percentile_filter` y `scipy.signal.wiener`.

## 7.4 Morfología matemática

Se "sondea" la imagen con una forma simple (el **elemento estructurante**) y se modifica según cómo encaje:

```python
el = ndimage.generate_binary_structure(2, 1)
# [[0 1 0]
#  [1 1 1]     cruz (vecindad 4)
#  [0 1 0]]
```

| Operación | Definición | Efecto |
| --- | --- | --- |
| **Erosión** | Filtro mínimo | Adelgaza objetos; elimina los más pequeños que el elemento |
| **Dilatación** | Filtro máximo | Engrosa objetos; rellena huecos pequeños |
| **Apertura** (*opening*) | Erosión + dilatación | Elimina objetos pequeños y suaviza esquinas |
| **Cierre** (*closing*) | Dilatación + erosión | Elimina agujeros pequeños |
| **Esqueletización** | — | Reduce objetos a líneas de 1 píxel conservando la topología |

```python
a = np.zeros((7, 7), dtype=int); a[1:6, 2:5] = 1      # rectángulo 5×3
ndimage.binary_erosion(a).astype(a.dtype)              # queda una línea central
ndimage.binary_erosion(a, structure=np.ones((5, 5)))   # desaparece (más pequeño que 5×5)
ndimage.binary_dilation(a)
ndimage.binary_opening(a, structure=np.ones((3, 3)))
ndimage.binary_closing(a)
ndimage.grey_dilation(img, size=(5, 5))                # también en escala de grises
```

**Reconstrucción** (erosión + propagación): elimina el ruido sin deformar los objetos grandes, y suele dar mejor resultado que la apertura y el cierre:

```python
erosionada = ndimage.binary_erosion(binaria)
reconstruida = ndimage.binary_propagation(erosionada, mask=binaria)
```

## 7.5 Detección de bordes

```python
sx = ndimage.sobel(img, axis=0, mode='constant')   # gradiente vertical
sy = ndimage.sobel(img, axis=1, mode='constant')   # gradiente horizontal
bordes = np.hypot(sx, sy)                          # magnitud = √(sx² + sy²)
```

Los bordes son zonas de **alta variación de intensidad**. El operador de **Sobel** aproxima el gradiente. El filtro de **Canny** (`skimage.feature.canny`) produce bordes finos y limpios, pero depende de varios parámetros, con riesgo de sobreajuste.

## 7.6 Segmentación

**Basada en histograma** (sin información espacial): es la binarización del [apunte 4](./04-escala-de-grises-y-binarizacion.md), con un umbral elegido en el valle del histograma.

```python
hist, bordes = np.histogram(img, bins=60)
binaria = img > 0.5
```

- **Umbral automático:** un modelo de mezcla gaussiana con 2 componentes; el umbral es la media de las dos medias.
- **Limpieza:** `binary_opening` quita manchas blancas pequeñas y `binary_closing` quita agujeros negros pequeños.
- **Watershed** (línea divisoria): separa objetos que se tocan. Toma como marcadores los máximos locales de la transformada de distancia al fondo.
- **Spectral clustering:** convierte la imagen en un grafo ponderado por el gradiente y lo particiona.

## 7.7 Medir objetos (`ndimage.measurements`)

```python
etiquetas, n = ndimage.label(mascara)                         # componentes conectados
tamanos = ndimage.sum(mascara, etiquetas, range(n + 1))      # área de cada región
etiquetas[(tamanos < 1000)[etiquetas]] = 0                    # borrar regiones pequeñas
sl_x, sl_y = ndimage.find_objects(etiquetas == 4)[0]          # caja de la región 4
roi = img[sl_x, sl_y]                                         # región de interés
```

Otras medidas: `center_of_mass`, `maximum_position`, promedios por bloque o radiales (`ndimage.mean` con etiquetas) y granulometría (aperturas con discos de tamaño creciente).

## 7.8 Equivalencias con versiones actuales

| En el documento | Hoy |
| --- | --- |
| `scipy.misc.lena()`, `scipy.lena()` | Ya no existe; `scipy.datasets.face()` o `skimage.data.camera()` |
| `misc.imread`, `misc.imsave` | `plt.imread`/`plt.imsave` o `skimage.io` |
| `np.int`, `np.float`, `np.bool` | `int`, `float`, `bool` (eliminados en NumPy ≥ 1.24) |
| `np.random.random_integers` | `np.random.randint` |
| `skimage.filter` | `skimage.filters` |
| `skimage.filter.canny` | `skimage.feature.canny` |
| `skimage.filter.tv_denoise` | `skimage.restoration.denoise_tv_chambolle` |
| `skimage.morphology.watershed`, `is_local_maximum` | `skimage.segmentation.watershed`, `skimage.feature.peak_local_max` |
| `sklearn.mixture.GMM` | `sklearn.mixture.GaussianMixture` |
| División `/` en índices (`lx/4`) | División entera `//` (en Python 3, `/` da `float` y falla como índice) |

## 7.9 Ejercicios propuestos en el documento

1. **Manipulación:** abrir una imagen, recortar una parte significativa, mostrarla con distintas interpolaciones, pasarla a gris, aumentar el contraste cambiando el mínimo y el máximo, saturar el 5 % más oscuro y el 5 % más claro (`np.percentile`), y guardarla en PNG, JPG y TIFF.
2. **Ruido:** crear una imagen binaria con figuras, añadir un 20 % de ruido, quitarlo con los filtros gaussiano, de mediana y TV, y comparar sus histogramas con el de la imagen sin ruido.
3. **Segmentación de monedas** (`skimage.data.coins()`): segmentar por histograma, por bordes (Canny + `binary_fill_holes`) y por regiones (Sobel + watershed), y medir el tamaño de cada moneda.
