import { type Imagen } from "./imagen";
import { luminosidad } from "./color";

export interface Histograma {
  rojo: Uint32Array;
  verde: Uint32Array;
  azul: Uint32Array;
  luminosidad: Uint32Array;
  totalPixeles: number;
}

function nivel(valor: number): number {
  const n = Math.round(valor * 255);
  return n < 0 ? 0 : n > 255 ? 255 : n;
}

/**
 * Cuántos píxeles tiene cada nivel 0–255 en cada canal y en la luminosidad
 * (calcularHistograma del Taller 9, equivalente a np.bincount).
 */
export function calcularHistograma(imagen: Imagen): Histograma {
  const rojo = new Uint32Array(256);
  const verde = new Uint32Array(256);
  const azul = new Uint32Array(256);
  const lum = new Uint32Array(256);
  const d = imagen.datos;
  for (let i = 0; i < d.length; i += 3) {
    rojo[nivel(d[i])]++;
    verde[nivel(d[i + 1])]++;
    azul[nivel(d[i + 2])]++;
  }
  for (const v of luminosidad(imagen)) lum[nivel(v)]++;
  return { rojo, verde, azul, luminosidad: lum, totalPixeles: imagen.ancho * imagen.alto };
}
