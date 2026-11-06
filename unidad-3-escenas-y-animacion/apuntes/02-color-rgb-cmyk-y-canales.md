# 2. Color: RGB, CMYK y canales

## 2.1 Modelo RGB (aditivo)

**RGB** (*Red, Green, Blue*) representa cada color como la **suma de los tres colores primarios de la luz**, cada uno con su propia intensidad (Diapositivas 7 y 10).

- **0** → el canal no interviene en la mezcla.
- **255** → el canal aporta su máxima intensidad.
- Hay 256 niveles por canal → **256 × 256 × 256 = 16 777 216** colores.
- Es el estándar de las **pantallas**, que emiten luz.

### Colores de referencia (Diapositiva 8)

| Color | RGB (0–255) | RGB normalizado |
| --- | --- | --- |
| Negro | (0, 0, 0) | (0, 0, 0) |
| Blanco | (255, 255, 255) | (1, 1, 1) |
| Rojo | (255, 0, 0) | (1, 0, 0) |
| Verde | (0, 255, 0) | (0, 1, 0) |
| Azul | (0, 0, 255) | (0, 0, 1) |
| Amarillo | (255, 255, 0) | (1, 1, 0) |
| Cian | (0, 255, 255) | (0, 1, 1) |
| Magenta | (255, 0, 255) | (1, 0, 1) |
| Naranja (infografía) | (255, 128, 0) | (1, 0.5, 0) |

Al superponer luces (Diapositiva 9): rojo + verde = amarillo, verde + azul = cian, rojo + azul = magenta, y los tres juntos dan **blanco**.

## 2.2 Modelo CMYK (sustractivo)

**CMYK** (*Cyan, Magenta, Yellow, Key/negro*) describe **tintas** sobre papel. Cada tinta **absorbe** (resta) parte de la luz blanca. Es el modelo de la **impresión**.

- Cian absorbe el rojo, magenta absorbe el verde y amarillo absorbe el azul.
- Al superponer tintas: cian + magenta = azul, magenta + amarillo = rojo, cian + amarillo = verde, y las tres juntas dan **negro** (en la práctica un negro sucio; por eso existe la tinta K).

### Relación entre ambos modelos (valores normalizados)

```
C = 1 − R        M = 1 − G        Y = 1 − B
```

Cada tinta es el **complemento** de un canal de luz. Esa es la misma idea del negativo ([apunte 3](./03-operaciones-aritmeticas-brillo-contraste.md)).

| | RGB | CMYK |
| --- | --- | --- |
| Tipo | Aditivo (luz) | Sustractivo (tinta) |
| Partida | Negro (sin luz) | Blanco (papel) |
| Los tres al máximo | Blanco | Negro |
| Uso | Pantallas | Impresión |

## 2.3 Descomposición RGB (Diapositiva 11)

Para ver la contribución de un canal, se **apagan los otros dos** (se ponen en 0):

```python
imgUTP = np.array(plt.imread("Imagen.jpg")) / 255

CapaR = np.copy(imgUTP)
CapaR[:, :, 1] = CapaR[:, :, 2] = 0     # sin verde ni azul → solo rojo

CapaG = np.copy(imgUTP)
CapaG[:, :, 0] = CapaG[:, :, 2] = 0     # solo verde

CapaB = np.copy(imgUTP)
CapaB[:, :, 0] = CapaB[:, :, 1] = 0     # solo azul

plt.subplot(2, 2, 1); plt.imshow(imgUTP); plt.axis('off'); plt.title("Imagen Original")
plt.subplot(2, 2, 2); plt.imshow(CapaR);  plt.axis('off'); plt.title("Capa Roja")
plt.subplot(2, 2, 3); plt.imshow(CapaG);  plt.axis('off'); plt.title("Capa Verde")
plt.subplot(2, 2, 4); plt.imshow(CapaB);  plt.axis('off'); plt.title("Capa Azul")
plt.show()
```

### Sintaxis clave

- `img[:, :, k]` significa todas las filas, todas las columnas, canal `k` (0 = R, 1 = G, 2 = B).
- `a[...] = b[...] = 0` es una **asignación encadenada**: equivale a `a[...] = 0` y `b[...] = 0`.
- Asignar un escalar a una rebanada lo replica en todos sus elementos (*broadcasting*).
- `np.copy` es indispensable. Sin la copia, `CapaR = imgUTP` sería otro nombre para el mismo arreglo, y modificarla alteraría la original.

### Reconstrucción

Cada píxel `(R, G, B)` queda repartido en `(R, 0, 0)`, `(0, G, 0)` y `(0, 0, B)`, así que **sumar** las capas recupera la imagen:

```python
reconstruida = CapaR + CapaG + CapaB      # == imgUTP
```

### Otra forma de ver un canal (tutorial)

Un canal se puede mostrar solo, como una imagen en gris:

```python
plt.imshow(img[:, :, 0], cmap='gray', vmin=0, vmax=1)   # intensidad del rojo
```

En la foto de Lena, el **rojo** es el canal más activo (mucha piel y un fondo crema), el **verde** es el que tiene más detalle y el **azul** es el que menos aporta. Por eso quitar solo el azul cambia poco la imagen.

## 2.4 Capas CMYK (Diapositiva 12)

Para cada tinta se fija en **1** (máximo) los dos canales que esa tinta **no** absorbe, y se deja libre el que sí absorbe:

```python
CapaC = np.copy(imgUTP)
CapaC[:, :, 1] = CapaC[:, :, 2] = 1     # (R, 1, 1) → cian

CapaM = np.copy(imgUTP)
CapaM[:, :, 0] = CapaM[:, :, 2] = 1     # (1, G, 1) → magenta

CapaY = np.copy(imgUTP)
CapaY[:, :, 0] = CapaY[:, :, 1] = 1     # (1, 1, B) → amarillo
```

Por qué funciona, tomando la capa amarilla: un píxel `(1, 1, B)` con `B = 1` es blanco (no lleva tinta amarilla) y con `B = 0` es amarillo puro. El canal azul controla cuánto amarillo se ve (`Y = 1 − B`).

> En la diapositiva, las variables se llaman `CapaR`, `CapaG` y `CapaB` aunque representan cian, magenta y amarillo. Los títulos sí dicen "Canal Cian/Magenta/Amarillo".

### Reconstrucción desde CMYK

Aquí **no** sirve sumar, porque cada capa tiene unos en los canales que no usa. Se **multiplica**, igual que al superponer filtros de tinta:

```python
reconstruida = CapaC * CapaM * CapaY            # (R·1·1, 1·G·1, 1·1·B) = (R, G, B)
# equivalente con suma: CapaC + CapaM + CapaY - 2
```

`np.allclose(reconstruida, imgUTP)` da `True` (verificado en `capasCMYK.py` de la unidad 3).

| Descomposición | Valor "neutro" de los otros canales | Reconstrucción |
| --- | --- | --- |
| RGB | 0 | Suma |
| CMYK | 1 | Producto |

## 2.5 Ajuste de canal (Diapositiva 22)

Consiste en modificar la intensidad de **un solo canal** a la vez:

```python
img1 = plt.imread('Imagen.jpg') / 255
brillo = 0.5
imgCanal = np.copy(img1)
Canal = 0                                         # 0 = rojo, 1 = verde, 2 = azul
imgCanal[:, :, Canal] = img1[:, :, Canal] + brillo
plt.imshow(imgCanal)                              # imagen con tono rojizo
```

El resultado supera 1 en muchos píxeles. `imshow` lo recorta y muestra una advertencia. Lo correcto es `np.clip(..., 0, 1)` (ver [apunte 3](./03-operaciones-aritmeticas-brillo-contraste.md)).

> La diapositiva reutiliza el título de figura "Ajuste de brillo" para este ejemplo.

## Preguntas para sustentar

- **¿Por qué en RGB se apagan los otros canales con 0 y en CMYK se fijan en 1?** En RGB el 0 significa "sin luz de ese color". En CMYK el 1 significa "sin tinta" (el papel blanco refleja ese canal).
- **¿Por qué la reconstrucción RGB es una suma y la CMYK un producto?** La luz se suma (aditivo). Las tintas filtran (sustractivo), y filtrar en cadena equivale a multiplicar transmitancias.
- **¿Qué pasa si se olvida `np.copy`?** Todas las "capas" serían el mismo arreglo, y la última modificación arruinaría las anteriores y la original.
