# 3. Operaciones aritméticas, brillo y contraste

El procesamiento de imágenes usa el álgebra lineal: las operaciones entre matrices modifican la apariencia visual. Como las imágenes son arreglos de NumPy, cada operación se aplica **elemento a elemento** a todos los píxeles a la vez, sin ciclos.

## 3.1 Inversión de color o negativo (Diapositiva 13)

Cada canal se convierte en su complemento, como en una película fotográfica:

```
I_invertida = 255 − I_original      (0–255)
I_invertida = 1 − I_original        (normalizada)
```

```python
img1 = plt.imread('Imagen.jpg') / 255
ImgNegativo = 1 - img1
plt.figure("Negativo de una imagen")
plt.imshow(ImgNegativo)
plt.axis('off')
plt.show()
```

| Original | Negativo |
| --- | --- |
| Blanco (1, 1, 1) | Negro (0, 0, 0) |
| Azul (0, 0, 1) | Amarillo (1, 1, 0) |
| Verde (0, 1, 0) | Magenta (1, 0, 1) |
| Rojo (1, 0, 0) | Cian (0, 1, 1) |
| Naranja (255, 128, 0) | (0, 127, 255), un azul claro (infografía) |

**Uso principal:** digitalizar negativos fotográficos. Aplicar el negativo dos veces devuelve la imagen original.

## 3.2 Suma y resta de matrices (Diapositivas 14–15)

Se suman o restan los píxeles **correspondientes** (misma fila, columna y canal):

```
A = |2 0 1|   B = |1 0 1|   A + B = |3 0 2|   A − B = |1  0  0|
    |3 0 0|       |1 2 1|           |4 2 1|           |2 −2 −1|
    |5 1 1|       |1 1 0|           |6 2 1|           |4  0  1|
```

**Requisito:** ambas imágenes deben tener **la misma forma** (`shape`) y la **misma escala** (las dos en 0–1 o las dos en 0–255). Si no, NumPy lanza `ValueError: operands could not be broadcast together`. La infografía lo resume así: "usa imágenes de formas compatibles y el mismo rango".

```python
img1 = plt.imread('Bote.jpg') / 255
img2 = plt.imread('Mar.jpg') / 255
SumaImg = img1 + img2          # R = Mar + Bote
plt.imshow(SumaImg)            # se ve "lavada"
```

**Por qué se ve lavada:** la imagen del bote tiene el fondo blanco (1). Donde hay blanco, la suma da `1 + Mar ≥ 1`, que `imshow` recorta a 1, y casi todo queda blanquecino. Solo el bote (oscuro) deja ver algo del mar.

**Resta:** resaltar diferencias entre dos imágenes, por ejemplo para detectar cambios o movimiento entre dos fotos de la misma escena. Los valores negativos se recortan a 0.

## 3.3 Suma ponderada o mezcla (Diapositiva 16)

Un **factor de mezcla** α controla cuánto aporta cada imagen:

```
F = α·A + (1 − α)·B,      0 ≤ α ≤ 1
```

```python
Factor = 0.2
SumaImg = img1 * Factor + img2 * (1 - Factor)   # 20 % bote, 80 % mar
```

- Como `α + (1 − α) = 1`, el resultado **nunca sale de [0, 1]**: es un promedio ponderado. Por eso esta versión no se ve lavada.
- α = 1 da solo A, α = 0 da solo B, y α = 0.5 es una mezcla al 50 %.
- Ejemplo de la infografía: naranja (255, 128, 0) y azul (0, 127, 255) con α = 0.5 dan (127.5, 127.5, 127.5), un gris.
- La diapositiva la titula "Imágenes fusionadas y **ecualizadas**", pero la infografía aclara que **mezclar no es ecualizar**. La ecualización de histograma es otra técnica ([apunte 6](./06-histograma.md)).
- Es la base del *cross-fade* (fundido) en video: se anima α de 0 a 1.

## 3.4 Precaución con imágenes `uint8`

Una imagen leída sin normalizar es `uint8` (enteros de 0 a 255). La aritmética en `uint8` es **modular**: da la vuelta en lugar de saturar. Valores verificados con NumPy:

```python
a = np.array([240], dtype=np.uint8)
a + np.uint8(30)      # → 14   (270 − 256), ¡no 255!
np.array([10], np.uint8) - np.uint8(30)   # → 236  (−20 + 256), ¡no 0!
```

**Regla:** primero se convierte a un tipo de mayor rango, después se calcula, se recorta y solo al final se vuelve a `uint8`.

```python
resultado = np.clip(img8.astype(np.float32) + 30, 0, 255).astype(np.uint8)  # 240 → 255
```

Recortar **después** de desbordar no sirve: el 14 ya es un 14 válido para `clip`. Si se trabaja en [0, 1], se recorta con `np.clip(resultado, 0, 1)`.

## 3.5 Ajuste de brillo (Diapositiva 21)

El brillo modifica la **luminancia global**. Va del 0 % (negro) al 100 % (blanco) y es uno de los controles más básicos.

```
I_mod = I + b       (b > 0 aclara, b < 0 oscurece)
```

```python
brillo = 0.5
imgBrillo = img1 + brillo                  # versión de la diapositiva
imgBrillo = np.clip(img1 + brillo, 0, 1)   # versión correcta, sin advertencia
```

Ejemplo de la infografía en 0–255: `I = 240`, `b = 30` → `clip(270, 0, 255) = 255`.

El brillo **desplaza** todos los valores por igual, así que no cambia la diferencia entre píxeles (el contraste). Lo que sí ocurre es que los píxeles que se saturan en 1 o en 0 **pierden detalle**: varios valores distintos terminan iguales.

## 3.6 Ajuste de contraste (Diapositivas 23–24)

El **contraste** es la diferencia entre las zonas oscuras y las claras de la imagen. Se modifica con funciones no lineales que "estiran" un rango de intensidades y "comprimen" otro:

| Función | Fórmula de la diapositiva | Efecto |
| --- | --- | --- |
| Logarítmica | `IMB(i,j) = K · log₁₀(1 + IMA(i,j))` | Aumenta el contraste de las **zonas oscuras** a costa de las claras |
| Exponencial | `IMB(i,j) = K · exp(IMA(i,j) − 1)` | Aumenta el contraste de las **zonas claras** a costa de las oscuras |

```python
Contraste = 0.5
ImgContraste = Contraste * np.log10(1 + img1)   # 'Contraste Zonas Oscuras'
ImgContraste = Contraste * np.exp(img1 - 1)     # 'Contraste Zonas Claras'
```

**Por qué funciona:** la pendiente del logaritmo es grande cerca de 0 y pequeña cerca de 1. Dos píxeles oscuros parecidos quedan más separados, y dos claros quedan más juntos. La exponencial hace lo contrario.

### Observación: con K = 0.5 el resultado sale oscuro

Rangos verificados sobre una foto normalizada:

| Expresión | Rango de salida |
| --- | --- |
| `0.5 · log₁₀(1 + I)` | [0, 0.15] |
| `0.5 · exp(I − 1)` | [0.18, 0.50] |

Por eso las dos imágenes de la Diapositiva 24 se ven oscuras: `log₁₀(2) ≈ 0.301`, así que ni con `I = 1` se llega a blanco. Para que la salida ocupe todo [0, 1], `K` debe **normalizar**:

```python
oscuras = np.log10(1 + img1) / np.log10(2)        # K = 1/log10(2) ≈ 3.32 → rango [0, 1]
claras  = (np.exp(img1) - 1) / (np.e - 1)         # forma normalizada de la exponencial → [0, 1]
```

Otra opción común es la **corrección gamma**, `I' = I^γ`: con γ < 1 aclara las zonas oscuras y con γ > 1 resalta las claras. Siempre queda en [0, 1].

### Contraste al visualizar (Scipy notes)

Sin modificar los datos, se puede estirar el contraste solo en pantalla:

```python
plt.imshow(gris, cmap='gray', vmin=0.12, vmax=0.78)   # lo menor a vmin se ve negro, lo mayor a vmax blanco
```

## Preguntas para sustentar

- **¿Por qué la suma simple se ve lavada y la ponderada no?** La simple puede superar 1 y se recorta. La ponderada es un promedio (α + (1 − α) = 1), así que queda en [0, 1].
- **¿Qué pasa al sumar 30 a un píxel de 240 en `uint8`?** Da 14 por desbordamiento modular. Hay que convertir a `float` antes.
- **¿Cuál es la diferencia entre brillo y contraste?** El brillo suma una constante (desplaza los valores). El contraste aplica una función no lineal (cambia la separación entre valores).
- **¿Por qué el logaritmo realza las zonas oscuras?** Porque su pendiente es mayor cerca de 0.
