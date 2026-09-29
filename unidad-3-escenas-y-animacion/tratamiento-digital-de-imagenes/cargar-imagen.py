import numpy as np
import matplotlib.pyplot as plt

# Lee el JPG como un arreglo de forma (alto, ancho, 3): cada píxel es [R, G, B] con
# valores uint8 de 0 a 255. np.array() hace una copia modificable. La ruta es relativa
# a la carpeta desde donde se ejecuta el programa (la raíz del repositorio).
imagen = np.array(plt.imread("unidad-3-escenas-y-animacion/tratamiento-digital-de-imagenes/formula1.jpg"))/255

# Crea una ventana llamada "Capas RGB"
plt.figure("Capas RGB")

# Divide la ventana en una cuadrícula de 2x2 y selecciona la posición 1 (arriba a la izquierda)
plt.subplot(2,2, 1)

# Dibuja la imagen original a color
plt.imshow(imagen)

capaR=np.copy(imagen)
capaR[:,:,1]=capaR[:,:,2]=0
plt.subplot(2,2, 2)
plt.imshow(capaR)

capaG=np.copy(imagen)
capaG[:,:,0]=capaG[:,:,2]=0
plt.subplot(2,2, 3)
plt.imshow(capaG)

capaB=np.copy(imagen)
capaB[:,:,0]=capaB[:,:,1]=0
plt.subplot(2,2, 4)
plt.imshow(capaB)

imgOriginal = capaR + capaG + capaB
plt.figure("Imagen reconstruida")
plt.imshow(imgOriginal)

imagen1 = np.array(plt.imread("unidad-3-escenas-y-animacion/tratamiento-digital-de-imagenes/Dubai1.jpg"))/255
imagen2 = np.array(plt.imread("unidad-3-escenas-y-animacion/tratamiento-digital-de-imagenes/Dubai2.jpg"))/255

plt.figure("Dubai1")
plt.imshow(imagen1)
plt.figure("Dubai2")
plt.imshow(imagen2)

plt.figure("Imagenes Dubai")
plt.imshow(imagen1 + imagen2)

factor = 0.9

suma = imagen1 * factor + imagen2 * (1-factor)
plt.figure("Suma ponderada")
plt.imshow(suma)

plt.show()
