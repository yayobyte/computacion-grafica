import { type Imagen } from "./imagen";

/**
 * Fusión de dos imágenes del mismo tamaño (fusionarConFactor del Taller 8).
 *
 * A es la imagen principal y B la segunda. La transparencia t se refiere a B,
 * como pide el enunciado: 0 = B completamente opaca, 1 = B completamente
 * transparente (solo se ve A).
 *   F = (1 − t)·B + t·A
 */
export function fusionar(principal: Imagen, segunda: Imagen, transparencia: number): Imagen {
  if (principal.ancho !== segunda.ancho || principal.alto !== segunda.alto) {
    throw new Error("Las imágenes deben tener el mismo tamaño para fusionarlas.");
  }
  const t = Math.min(1, Math.max(0, transparencia));
  const datos = new Float32Array(principal.datos.length);
  for (let i = 0; i < datos.length; i++) {
    datos[i] = (1 - t) * segunda.datos[i] + t * principal.datos[i];
  }
  return { ancho: principal.ancho, alto: principal.alto, datos };
}
