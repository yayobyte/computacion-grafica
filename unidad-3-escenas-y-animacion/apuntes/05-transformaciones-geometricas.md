# 5. Transformaciones geométricas

La infografía separa dos familias de transformaciones:

| Transforman… | Ejemplos | Qué cambia |
| --- | --- | --- |
| **Valores** | Brillo, contraste, negativo, gris | El color de cada píxel; la posición no cambia |
| **Coordenadas** | Traslación, recorte, rotación, zoom | Dónde queda cada píxel; el color no cambia |

Este apunte trata la segunda familia. Todas se apoyan en el **slicing** de NumPy, `img[filas, columnas]`. Hay que recordar que el primer índice es la fila (eje y, hacia abajo) y el segundo la columna (eje x, hacia la derecha).

## 5.1 Traslación (Diapositivas 26–27)

Es una operación de **geometría afín** que suma una cantidad fija a las coordenadas de cada píxel:

```
(x', y') = (x + Δx, y + Δy)
```

- **Δx:** desplazamiento horizontal. Positivo hacia la **derecha**, negativo hacia la izquierda.
- **Δy:** desplazamiento vertical. Positivo hacia **abajo**, negativo hacia arriba (porque las filas crecen hacia abajo).

```python
dx, dy = 50, 30                                # desplazamiento en píxeles (≥ 0)

# Nueva imagen del mismo tamaño llena de ceros (fondo negro)
trasladada = np.zeros_like(img)

# Límites válidos para el copiado
h, w = img.shape[:2]
x_origen_inicio, x_origen_fin = 0, w - dx
y_origen_inicio, y_origen_fin = 0, h - dy

# Asignar los valores trasladados
trasladada[dy:h, dx:w] = img[y_origen_inicio:y_origen_fin, x_origen_inicio:x_origen_fin]
```

**Cómo leerlo:** el bloque de origen (todo menos las últimas `dy` filas y `dx` columnas) se copia en el destino empezando en `(dy, dx)`. Lo que "se sale" por la derecha y por abajo se pierde, y la franja que queda libre arriba y a la izquierda es negra.

- La diapositiva no define `dx` ni `dy`. Hay que asignarlos antes de usar el código.
- El código solo funciona con `dx, dy ≥ 0`. Para valores negativos se invierten los papeles: `trasladada[0:h+dy, 0:w+dx] = img[-dy:h, -dx:w]`.
- La figura se titula "Traslación sin `np.roll`". `np.roll(img, (dy, dx), axis=(0, 1))` también desplaza, pero **envuelve**: lo que sale por un borde entra por el opuesto, en lugar de dejar negro.

## 5.2 Recorte (Diapositiva 28)

Se extrae una porción de la imagen: una **sub-matriz** delimitada por un inicio y un fin en cada eje.

```python
img1 = plt.imread('Imagen.jpg') / 255
print("Tamaño imagen original :", img1.shape)
xIni, xFin = 50, 200
yIni, yFin = 50, 200
ImgRecorte = img1[xIni:xFin, yIni:yFin]
print("Tamaño imagen recortada :", ImgRecorte.shape)   # (150, 150, 3)
```

- **Ojo con los nombres:** en `img1[xIni:xFin, yIni:yFin]` el primer rango recorre **filas** (vertical). Aunque se llame `x`, ahí actúa como y. Una versión menos confusa es `img1[filaIni:filaFin, colIni:colFin]`.
- El fin es **exclusivo**: `50:200` toma de la 50 a la 199, es decir, 150 elementos.
- El recorte es una **vista** del original, no una copia. Modificarlo modifica `img1`. Para independizarlo se usa `.copy()`.
- La diapositiva titula la figura "Escalado de una imagen" e imprime "Tamaño imagen escalada", pero la operación es un recorte.

Recorte del centro, con divisiones enteras (Scipy notes):

```python
lx, ly = img.shape[:2]
centro = img[lx//4 : -lx//4, ly//4 : -ly//4]    # quita un cuarto por cada lado
```

## 5.3 Volteos (Scipy notes)

```python
np.flipud(img)    # arriba ↔ abajo  (img[::-1, :])
np.fliplr(img)    # izquierda ↔ derecha  (img[:, ::-1])
np.rot90(img, k)  # rota k × 90° antihorario, sin pérdida ni interpolación
```

## 5.4 Rotación (Diapositivas 29–30)

Los algoritmos de giro son los **más complejos** y costosos en tiempo de procesado. Por eso solo se usan cuando la nueva orientación simplifica procesos posteriores (por ejemplo, enderezar un documento escaneado antes de leerlo).

### Matemática

Rotar un punto un ángulo θ en sentido antihorario alrededor del origen:

```
x' = x·cos θ − y·sin θ
y' = x·sin θ + y·cos θ
```

Al rotar, las esquinas se salen del rectángulo original. Por eso el lienzo de salida crece hasta:

```
alto'  = |alto·cos θ| + |ancho·sin θ|
ancho' = |ancho·cos θ| + |alto·sin θ|
```

**Mapeo inverso:** en lugar de mover cada píxel del original (lo que deja huecos, porque las coordenadas rotadas no son enteras), se recorre **cada píxel del destino** y se pregunta de qué píxel del original viene, aplicando la rotación con −θ. Así cada píxel del destino recibe un valor.

### Código de la diapositiva

Define `rotarImg(a, ang)` para imágenes 2D (en gris), con el ángulo en grados y dos casos: `0 < ang ≤ 90°` y `90° < ang ≤ 180°`. Usa ciclos `for` anidados y mapeo inverso:

```python
def rotarImg(a, ang):
    ang = np.radians(ang)                  # convertir a radianes
    m, n = a.shape
    cos_ang, sin_ang = np.cos(ang), np.sin(ang)

    if ang > 0 and ang <= np.pi / 2:
        c = int(round(m * sin_ang + n * cos_ang)) + 1
        d = int(round(m * cos_ang + n * sin_ang)) + 1
        b = np.zeros((c, d), dtype=a.dtype)
        for i in range(c):
            for j in range(d):
                iii = i - int(n * sin_ang) - 1
                ii = int(round(j * sin_ang + iii * cos_ang))
                jj = int(round(j * cos_ang - iii * sin_ang))
                if 0 <= ii < m and 0 <= jj < n:
                    b[i, j] = a[ii, jj]
    elif ang > np.pi / 2 and ang <= np.pi:
        c = int(round(m * sin_ang - n * cos_ang)) + 1
        d = int(round(m * sin_ang - n * cos_ang)) + 1
        e = -n * cos_ang
        b = np.zeros((c, d), dtype=a.dtype)
        for i in range(c):
            iii = c - i - 1
            for j in range(d):
                jjj = d - j - 1
                ii = int(round(jjj * sin_ang + iii * cos_ang))
                jj = int(round(jjj * cos_ang - iii * sin_ang))
                if 0 <= ii < m and 0 <= jj < n:
                    b[i, j] = a[ii, jj]
    else:
        raise ValueError("Ángulo fuera del rango esperado (0 < ang <= π)")
    return b

# Ejemplo de uso
img = plt.imread('imagen.jpg')
if img.ndim == 3:
    img = np.dot(img[..., :3], [0.299, 0.587, 0.114])   # convertir a escala de grises
rotada = rotarImg(img, 45)
plt.imshow(rotada, cmap='gray')
```

### Lo que encontré al ejecutarlo

Probé la función transcrita con una foto reducida, de 163×123 en gris y de 120×120. "Cobertura" es el porcentaje de píxeles del original que aparecen en la salida:

| Ángulo | Rectangular 163×123 | Cuadrada 120×120 |
| --- | --- | --- |
| 30° | 99 % | 100 % |
| 45° | 100 % | 99 % |
| 90° | 76 % (sale de 164×124, sin intercambiar alto y ancho) | 99 % |
| 120°, 150°, 180° | **0 %** (imagen negra) | **0 %** |

- **Primer caso (0°–90°):** funciona, y es el caso que muestra la diapositiva (45°). Las fórmulas de `c` y `d` tienen intercambiados `m` y `n` respecto a `alto'`/`ancho'`. En imágenes casi cuadradas no se nota. En una rectangular a 90° se recorta parte.
- **Segundo caso (90°–180°):** la salida queda vacía en todas las pruebas. Además, `c` y `d` se calculan con la misma fórmula, y la variable `e` nunca se usa.

### Versión vectorizada y para cualquier ángulo

La misma idea de mapeo inverso, sin ciclos y centrada en la imagen. Sirve para gris o RGB y para cualquier ángulo (probada en 0°, 30°, 90°, 120°, 180° y 270°: cobertura del 100 % en todos):

```python
def rotarImagen(img, grados):
    """Rota img (2D o RGB) en sentido antihorario usando mapeo inverso."""
    theta = np.radians(grados)
    cos_t, sin_t = np.cos(theta), np.sin(theta)
    alto, ancho = img.shape[:2]

    # Tamaño del lienzo que contiene la imagen rotada completa
    nuevoAlto = int(np.ceil(abs(alto * cos_t) + abs(ancho * sin_t)))
    nuevoAncho = int(np.ceil(abs(ancho * cos_t) + abs(alto * sin_t)))

    # Coordenadas de cada píxel destino, relativas al centro del lienzo
    filas, cols = np.indices((nuevoAlto, nuevoAncho))
    y = filas - nuevoAlto / 2
    x = cols - nuevoAncho / 2

    # Mapeo inverso: de qué píxel del original viene cada píxel destino
    xOrig = np.round(cos_t * x - sin_t * y + ancho / 2).astype(int)
    yOrig = np.round(sin_t * x + cos_t * y + alto / 2).astype(int)

    dentro = (xOrig >= 0) & (xOrig < ancho) & (yOrig >= 0) & (yOrig < alto)
    salida = np.zeros((nuevoAlto, nuevoAncho) + img.shape[2:], dtype=img.dtype)
    salida[filas[dentro], cols[dentro]] = img[yOrig[dentro], xOrig[dentro]]
    return salida
```

Los signos de las fórmulas de `xOrig` y `yOrig` difieren del `x' = x·cos θ − y·sin θ` de arriba porque aquí el eje y apunta hacia **abajo**. Con esos signos, la rotación se ve antihoraria en pantalla.

**Con librerías:** `scipy.ndimage.rotate(img, 45)` amplía el lienzo y `ndimage.rotate(img, 45, reshape=False)` conserva el tamaño y recorta las esquinas (Scipy notes). SciPy **no** está en `requirements.txt`.

## 5.5 Reducción de resolución (Diapositivas 31–33)

Consiste en disminuir el número de píxeles, lo que implica una **pérdida inevitable de detalle**. La técnica de clase es el **submuestreo** (*downsampling*): tomar 1 de cada k píxeles en filas y columnas.

Ejemplo visual de la Diapositiva 32 (6×6 → 3×3 con factor 2):

```
[A B C D E F]
[G H I J K L]            [A C E]
[M N O P Q R]   ::2 →    [M O Q]
[S T U V W X]            [Y a c]
[Y Z a b c d]
[e f g h i j]
```

```python
zoom_factor = 5
zoomed = img1[::zoom_factor, ::zoom_factor]   # filas y columnas 0, 5, 10, 15...
print("Tamaño imagen original :", img1.shape)          # p. ej. (1304, 980, 3)
print("Tamaño con la reducción de resolución :", zoomed.shape)   # (261, 196, 3)
```

- `inicio:fin:paso` con inicio y fin vacíos recorre todo con el paso indicado.
- El nuevo tamaño es `ceil(alto/k) × ceil(ancho/k)`.
- Al mostrar `zoomed` con `imshow` al mismo tamaño de ventana, se ve **pixelada** (Diapositiva 33).
- Saltar píxeles puede producir *aliasing* (patrones falsos en texturas finas). Promediar cada bloque k×k en lugar de tomar uno suaviza el resultado. Las Scipy notes lo hacen con `ndimage.mean` (bloque promedio).

## 5.6 Ampliación de una región o zoom (Diapositiva 34)

Se recorta una región y se **agranda** repitiendo cada píxel en un bloque k×k (vecino más cercano):

```python
img1 = plt.imread('Imagen.jpg') / 255

# Coordenadas para recortar el centro (100×100)
h, w = img1.shape[:2]
zoom_area = 100
start_row = h // 2 - zoom_area // 2
end_row   = h // 2 + zoom_area // 2
start_col = w // 2 - zoom_area // 2
end_col   = w // 2 + zoom_area // 2
recorte = img1[start_row:end_row, start_col:end_col]

# Aumentar el tamaño del recorte (ampliación)
zoom_factor = 5
zoomed = np.kron(recorte, np.ones((zoom_factor, zoom_factor, 1)))   # (100,100,3) → (500,500,3)
```

**`np.kron` (producto de Kronecker):** reemplaza cada elemento de `recorte` por ese elemento multiplicado por el bloque `np.ones((5, 5, 1))`. Cada píxel se convierte en un cuadro de 5×5 del mismo color. El `1` del tercer eje deja los 3 canales sin repetir. Para una imagen 2D se usa `np.ones((k, k))`.

Alternativa equivalente y más explícita:

```python
zoomed = recorte.repeat(zoom_factor, axis=0).repeat(zoom_factor, axis=1)
```

La ampliación **no agrega detalle**: solo hace más grandes los píxeles existentes. Es la operación inversa del submuestreo en tamaño, no en información.

## Preguntas para sustentar

- **¿Por qué en la traslación Δy positivo baja la imagen?** Porque el índice de fila crece hacia abajo.
- **¿Qué diferencia hay entre trasladar con slicing y con `np.roll`?** El slicing deja fondo negro; `np.roll` envuelve los píxeles al borde opuesto.
- **¿Por qué la rotación usa mapeo inverso?** Porque el mapeo directo produce coordenadas no enteras y deja huecos en el destino.
- **¿Por qué la imagen rotada es más grande?** Para que quepan las esquinas, que al girar se salen del rectángulo original.
- **¿Reducir y luego ampliar devuelve la imagen original?** No. La reducción descarta píxeles, y la ampliación solo repite los que quedaron.
