# 4. Escala de grises y binarización

## 4.1 Qué es una imagen en escala de grises (Diapositiva 17)

Es un **arreglo de dos dimensiones** `(alto, ancho)` que informa la **intensidad de la luz** en cada punto. Pasa de 3 valores por píxel a 1. Como el píxel `(1, 1, 1)` es blanco y `(0, 0, 0)` es negro, cuanto mayores son los canales, más "claro" es el píxel. Todas las técnicas combinan R, G y B en un solo número.

Las tres técnicas de la unidad:

| Técnica | Fórmula | Idea |
| --- | --- | --- |
| Promedio (*Average*) | `(R + G + B) / 3` | Todos los canales pesan igual |
| Luminosidad (*Luminosity*) | `0.299R + 0.587G + 0.114B` | Pondera según la sensibilidad del ojo |
| Tonalidad (*Midgray*) | `(max(R,G,B) + min(R,G,B)) / 2` | Componente L del modelo HSL |

## 4.2 Técnica de promedio (Diapositiva 18)

Es la forma más simple: se suman las componentes RGB píxel a píxel y se divide por 3.

```python
img1 = plt.imread('Imagen.jpg') / 255
ImgGris = (img1[:, :, 0] + img1[:, :, 1] + img1[:, :, 2]) / 3
# equivalente: ImgGris = img1.mean(axis=2)
plt.figure("Escala de grises (Promedio)")
plt.imshow(ImgGris, cmap='gray')
plt.axis('off')
plt.show()
```

`axis=2` promedia a lo largo del tercer eje (los canales) y deja `(alto, ancho)`.

**Limitación:** un verde puro `(0, 1, 0)` y un azul puro `(0, 0, 1)` dan el mismo gris (0.33), aunque el ojo percibe el verde mucho más brillante.

### Versión con ciclos (ejercicio del tutorial)

Sirve para entender qué hace la versión vectorizada, aunque es mucho más lenta:

```python
alto, ancho, canales = img.shape
gris = np.zeros((alto, ancho))
for i in range(alto):
    for j in range(ancho):
        gris[i, j] = (img[i, j, 0] + img[i, j, 1] + img[i, j, 2]) / 3
```

El tutorial luego pide hacerlo "sin usar fors", que es exactamente la versión de la diapositiva.

## 4.3 Técnica de luminosidad (Diapositiva 19)

Mejora el promedio **ponderando** cada canal según la sensibilidad del ojo humano: más sensible al **verde**, luego al rojo y mucho menos al azul. Los coeficientes vienen del estándar **Rec. 601 (NTSC) de la UIT-R**, adoptado en la televisión a color compatible con los televisores en blanco y negro.

```
I_gris = 0.299·R + 0.587·G + 0.114·B
```

```python
ImgGris = 0.299*img1[:, :, 0] + 0.587*img1[:, :, 1] + 0.114*img1[:, :, 2]
plt.figure("Escala de grises (Luma (Percepción humana de brillo))")
plt.imshow(ImgGris, cmap='gray')
```

Forma compacta, que también usan las Diapositivas 30 y 39:

```python
ImgGris = np.dot(img1[..., :3], [0.299, 0.587, 0.114])
```

- `...` (*Ellipsis*) significa "todos los ejes anteriores". `img[..., :3]` toma los 3 primeros canales y descarta el alfa si la imagen es RGBA.
- `np.dot` con un vector de 3 pesos hace la suma ponderada en cada píxel.
- Los pesos suman 1 (0.299 + 0.587 + 0.114 = 1.000), así que el resultado queda en el mismo rango que la entrada.

## 4.4 Técnica de tonalidad o midgray (Diapositiva 20)

En el modelo **HSL** (*Hue, Saturation, Lightness*: tonalidad, saturación, luminancia), la luminancia L es la media entre la componente de color **máxima** y la **mínima** de cada píxel:

```
I_gris = (max(R, G, B) + min(R, G, B)) / 2
```

```python
R, G, B = img1[:, :, 0], img1[:, :, 1], img1[:, :, 2]
ImgGris = (np.maximum(R, np.maximum(G, B)) + np.minimum(R, np.minimum(G, B))) / 2
# equivalente: (img1.max(axis=2) + img1.min(axis=2)) / 2
```

> **Detalle de la diapositiva:** escribe `np.maximum(img1[:,:,0], img1[:,:,1], img1[:,:,2])`. `np.maximum` compara solo **dos** arreglos. El tercer argumento posicional es `out` (dónde guardar el resultado), así que:
>
> 1. El canal azul **no** se compara. Se usa como depósito y **se sobrescribe dentro de `img1`**.
> 2. `np.maximum` y `np.minimum` escriben en ese mismo depósito, así que la segunda llamada pisa a la primera. El resultado final es `min(R, G)`, no el midgray.
>
> Lo verifiqué con NumPy 2.5 sobre una foto: la salida coincide exactamente con `min(R, G)`. NumPy además emite una `DeprecationWarning` por pasar 3 argumentos. Para tres canales se anida (`np.maximum(R, np.maximum(G, B))`) o se usa `img1.max(axis=2)`, y ambas formas dan el midgray correcto.

**Comparación con un píxel naranja (1, 0.5, 0):**

| Técnica | Cálculo | Gris |
| --- | --- | --- |
| Promedio | (1 + 0.5 + 0) / 3 | 0.500 |
| Luminosidad | 0.299 + 0.2935 + 0 | 0.593 |
| Midgray | (1 + 0) / 2 | 0.500 |

## 4.5 Binarización (Diapositiva 25)

Convierte la imagen a **blanco y negro absoluto**: solo 0 y 1. Se fija un **umbral**. Los píxeles menores al umbral pasan a 0 y los mayores o iguales pasan a 1.

```
IMB(i, j) = (IMA(i, j) ≥ umbral)
```

```python
Gris = (img1[:, :, 0] + img1[:, :, 1] + img1[:, :, 2]) / 3   # primero a gris
Umbral = 0.5
ImgBin = (Gris > Umbral)          # arreglo de booleanos (True/False)
plt.figure("Imagen Binarizada")
plt.imshow(ImgBin, cmap='gray')
plt.axis('off')
plt.show()
```

- La comparación devuelve un arreglo `bool`. `imshow` lo muestra como 0/1. Para operar con él como números: `ImgBin.astype(float)` o `astype(np.uint8)`.
- La fórmula dice `≥` y el código usa `>`. Solo difieren en los píxeles exactamente iguales al umbral. Para seguir la definición, se usa `Gris >= Umbral`.
- **Siempre se binariza sobre una imagen en gris** (2D). Sobre la imagen RGB se obtendría un umbral por canal.

| | Imagen en gris | Imagen binaria |
| --- | --- | --- |
| Valores | Intensidades continuas en [0, 1] | Solo 0 y 1 |
| Uso | Análisis de brillo | Segmentar: separar objeto y fondo |

### Cómo elegir el umbral

- **A mano:** 0.5, o probar varios valores y comparar.
- **Con el promedio:** `umbral = gris.mean()` (lo usan las Scipy notes).
- **Mirando el histograma:** si es bimodal (dos montañas), el umbral va en el valle entre ellas ([apunte 6](./06-histograma.md)). Automatizar esta idea es el método de Otsu.

## Preguntas para sustentar

- **¿Por qué la luminosidad es mejor que el promedio?** Porque modela la percepción humana: el verde se ve más brillante que el azul con la misma intensidad física.
- **¿Por qué los pesos suman 1?** Para que un blanco `(1, 1, 1)` siga siendo 1 y el resultado no salga del rango.
- **¿Qué tipo de dato devuelve `gris > umbral`?** Un arreglo booleano, que se puede convertir con `astype`.
- **¿Qué información se pierde al binarizar?** Toda la gradación de intensidades. Solo queda si cada píxel está por encima o por debajo del umbral.
