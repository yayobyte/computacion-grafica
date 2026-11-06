/**
 * Representación de una imagen para el motor de procesamiento.
 *
 * Igual que en los talleres de Python (imagen normalizada con NumPy), cada
 * píxel guarda R, G y B como reales en [0, 1]. Los datos van entrelazados en
 * un Float32Array: el píxel (fila, columna) empieza en (fila * ancho + columna) * 3.
 */
export interface Imagen {
  ancho: number;
  alto: number;
  datos: Float32Array;
}

export function crearImagen(ancho: number, alto: number): Imagen {
  return { ancho, alto, datos: new Float32Array(ancho * alto * 3) };
}

export function clonar(imagen: Imagen): Imagen {
  return { ancho: imagen.ancho, alto: imagen.alto, datos: new Float32Array(imagen.datos) };
}

export function recortar01(valor: number): number {
  return valor < 0 ? 0 : valor > 1 ? 1 : valor;
}

/** De ImageData del canvas (0–255, RGBA) a Imagen (0–1, RGB). Se ignora el alfa. */
export function desdeImageData(origen: ImageData): Imagen {
  const imagen = crearImagen(origen.width, origen.height);
  const { data } = origen;
  for (let p = 0, q = 0; p < data.length; p += 4, q += 3) {
    imagen.datos[q] = data[p] / 255;
    imagen.datos[q + 1] = data[p + 1] / 255;
    imagen.datos[q + 2] = data[p + 2] / 255;
  }
  return imagen;
}

/** De Imagen a ImageData, recortando a [0, 1] y con alfa opaco. */
export function aImageData(imagen: Imagen): ImageData {
  const salida = new ImageData(imagen.ancho, imagen.alto);
  const { data } = salida;
  for (let p = 0, q = 0; q < imagen.datos.length; p += 4, q += 3) {
    data[p] = Math.round(recortar01(imagen.datos[q]) * 255);
    data[p + 1] = Math.round(recortar01(imagen.datos[q + 1]) * 255);
    data[p + 2] = Math.round(recortar01(imagen.datos[q + 2]) * 255);
    data[p + 3] = 255;
  }
  return salida;
}
