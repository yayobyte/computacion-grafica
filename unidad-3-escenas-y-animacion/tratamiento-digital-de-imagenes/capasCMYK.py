import numpy as np
import matplotlib.pyplot as plt

# Lee el JPG como un arreglo de forma (alto, ancho, 3): cada píxel es [R, G, B] con
# valores uint8 de 0 a 255. np.array() hace una copia modificable. La ruta es relativa
# a la carpeta desde donde se ejecuta el programa (la raíz del repositorio).
imagen = np.array(plt.imread("unidad-3-escenas-y-animacion/tratamiento-digital-de-imagenes/formula1.jpg"))/255
imagen1 = np.array(plt.imread("unidad-3-escenas-y-animacion/tratamiento-digital-de-imagenes/Dubai1.jpg"))/255
imagen2 = np.array(plt.imread("unidad-3-escenas-y-animacion/tratamiento-digital-de-imagenes/Dubai2.jpg"))/255

# Crea una ventana llamada "Capas RGB"
plt.figure("Capas CMYK")

# Divide la ventana en una cuadrícula de 2x2 y selecciona la posición 1 (arriba a la izquierda)
plt.subplot(3,3, 1)

# Dibuja la imagen original a color
plt.imshow(imagen)

capaC=np.copy(imagen)
capaC[:,:,1]=capaC[:,:,2]=1
plt.subplot(3,3, 2)
plt.imshow(capaC)

capaM=np.copy(imagen)
capaM[:,:,0]=capaM[:,:,2]=1
plt.subplot(3,3, 3)
plt.imshow(capaM)

capaY=np.copy(imagen)
capaY[:,:,0]=capaY[:,:,1]=1
plt.subplot(3,3, 4)
plt.imshow(capaY)

# Reconstrucción: multiplicar las capas equivale a superponer las tintas.
# Por píxel: (R·1·1, 1·G·1, 1·1·B) = (R, G, B), la imagen original.
reconstruida = capaC * capaM * capaY
plt.subplot(3,3, 5)
plt.imshow(reconstruida)

reconstruida = capaC + capaM + capaY
plt.subplot(3,3, 6)
plt.imshow(1-reconstruida)

invertida=1-np.copy(imagen)
plt.subplot(3,3, 7)
plt.imshow(invertida)

plt.show()
