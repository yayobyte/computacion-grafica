import { crearImagen, type Imagen } from "./imagen";
import { mapearValores } from "./ajustes";

/** Pesos del estándar Rec. 601 (NTSC) para la luminosidad. */
export const PESOS_LUMINOSIDAD = [0.299, 0.587, 0.114] as const;

export type TresCanales = [boolean, boolean, boolean];

/**
 * Canales RGB: el canal desactivado se pone en 0 ("sin luz").
 * Con los tres activos la imagen no cambia. (extraerCapa del Taller 8)
 */
export function filtrarCanalesRGB(imagen: Imagen, activos: TresCanales): Imagen {
  if (activos.every(Boolean)) return imagen;
  const salida = crearImagen(imagen.ancho, imagen.alto);
  const d = imagen.datos;
  for (let i = 0; i < d.length; i += 3) {
    salida.datos[i] = activos[0] ? d[i] : 0;
    salida.datos[i + 1] = activos[1] ? d[i + 1] : 0;
    salida.datos[i + 2] = activos[2] ? d[i + 2] : 0;
  }
  return salida;
}

/**
 * Tintas CMY. Cada tinta activa es la capa capaTinta del Taller 8: deja libre el
 * canal que la tinta absorbe (cian → R, magenta → G, amarillo → B) y fija en 1
 * los demás. Las tintas activas se superponen multiplicando, como filtros:
 *   canal R = R si cian está activa, si no 1; igual para G (magenta) y B (amarillo).
 * Con las tres activas se recupera la imagen; sin ninguna no se aplica el filtro.
 */
export function filtrarTintasCMY(imagen: Imagen, activas: TresCanales): Imagen {
  if (!activas.some(Boolean) || activas.every(Boolean)) return imagen;
  const salida = crearImagen(imagen.ancho, imagen.alto);
  const d = imagen.datos;
  for (let i = 0; i < d.length; i += 3) {
    salida.datos[i] = activas[0] ? d[i] : 1;
    salida.datos[i + 1] = activas[1] ? d[i + 1] : 1;
    salida.datos[i + 2] = activas[2] ? d[i + 2] : 1;
  }
  return salida;
}

/** Negativo: N = 1 − I. (invertirColores del Taller 8) */
export function negativo(imagen: Imagen): Imagen {
  return mapearValores(imagen, (v) => 1 - v);
}

/** Luminosidad de cada píxel: 0.299R + 0.587G + 0.114B. (grisLuminosidad del Taller 8) */
export function luminosidad(imagen: Imagen): Float32Array {
  const n = imagen.ancho * imagen.alto;
  const gris = new Float32Array(n);
  const d = imagen.datos;
  const [pr, pg, pb] = PESOS_LUMINOSIDAD;
  for (let p = 0, i = 0; p < n; p++, i += 3) gris[p] = pr * d[i] + pg * d[i + 1] + pb * d[i + 2];
  return gris;
}

/** Binarizar: blanco si la luminosidad ≥ umbral, negro si no. (binarizar del Taller 9) */
export function binarizar(imagen: Imagen, umbral: number): Imagen {
  const gris = luminosidad(imagen);
  const salida = crearImagen(imagen.ancho, imagen.alto);
  for (let p = 0, i = 0; p < gris.length; p++, i += 3) {
    const v = gris[p] >= umbral ? 1 : 0;
    salida.datos[i] = salida.datos[i + 1] = salida.datos[i + 2] = v;
  }
  return salida;
}
