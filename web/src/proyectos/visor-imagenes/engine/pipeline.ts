import { type Imagen } from "./imagen";
import { ajustarBrillo, ajustarContraste, filtrarZonas, type Zonas } from "./ajustes";
import { binarizar, filtrarCanalesRGB, filtrarTintasCMY, negativo, type TresCanales } from "./color";
import { ampliarRegion, rotar } from "./geometria";
import { fusionar } from "./fusion";

/** Todos los ajustes del visor. Los valores están en las unidades de los controles. */
export interface Ajustes {
  brillo: number; // −100 … 100 (%)
  contraste: number; // 0.2 … 3 (factor)
  rotacion: number; // 0 … 360 (grados)
  zonas: Zonas;
  canalesRGB: TresCanales;
  tintasCMY: TresCanales;
  negativo: boolean;
  binarizar: boolean;
  umbral: number; // 0 … 1
  zoom: { activo: boolean; x: number; y: number; factor: number }; // x, y en píxeles de la imagen original
  fusion: { activa: boolean; transparencia: number }; // 0 = segunda opaca … 1 = transparente
}

export const AJUSTES_INICIALES: Ajustes = {
  brillo: 0,
  contraste: 1,
  rotacion: 0,
  zonas: "ninguno",
  canalesRGB: [true, true, true],
  tintasCMY: [false, false, false],
  negativo: false,
  binarizar: false,
  umbral: 0.5,
  zoom: { activo: false, x: 0, y: 0, factor: 2 },
  fusion: { activa: false, transparencia: 0.5 },
};

/**
 * Aplica los ajustes en un orden fijo:
 *   fusión → brillo → contraste → zonas → canales RGB → tintas CMY
 *   → negativo → binarizar → zoom → rotación
 *
 * El zoom va antes de la rotación para que (x, y) se refieran siempre a la
 * imagen original. `escala` es la relación entre la imagen procesada y la
 * original (la vista previa se procesa reducida); sirve para convertir (x, y).
 * `segunda` debe tener ya el mismo tamaño que `base`.
 */
export function aplicarAjustes(base: Imagen, segunda: Imagen | null, a: Ajustes, escala = 1): Imagen {
  let img = base;
  if (a.fusion.activa && segunda) img = fusionar(img, segunda, a.fusion.transparencia);
  if (a.brillo !== 0) img = ajustarBrillo(img, a.brillo / 100);
  if (a.contraste !== 1) img = ajustarContraste(img, a.contraste);
  img = filtrarZonas(img, a.zonas);
  img = filtrarCanalesRGB(img, a.canalesRGB);
  img = filtrarTintasCMY(img, a.tintasCMY);
  if (a.negativo) img = negativo(img);
  if (a.binarizar) img = binarizar(img, a.umbral);
  if (a.zoom.activo) img = ampliarRegion(img, a.zoom.x * escala, a.zoom.y * escala, a.zoom.factor);
  img = rotar(img, a.rotacion);
  return img;
}
