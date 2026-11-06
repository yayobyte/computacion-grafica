import { recortar01, type Imagen } from "./imagen";

/** Aplica la misma función a cada canal de cada píxel. Retorna una imagen nueva. */
export function mapearValores(imagen: Imagen, f: (valor: number) => number): Imagen {
  const datos = new Float32Array(imagen.datos.length);
  for (let i = 0; i < datos.length; i++) datos[i] = f(imagen.datos[i]);
  return { ancho: imagen.ancho, alto: imagen.alto, datos };
}

/**
 * Brillo: I' = clip(I + b, 0, 1), con b en [-1, 1].
 * (ajustarBrillo del Taller 9)
 */
export function ajustarBrillo(imagen: Imagen, b: number): Imagen {
  return mapearValores(imagen, (v) => recortar01(v + b));
}

/**
 * Contraste: I' = clip((I - 0.5)·k + 0.5, 0, 1). k > 1 aumenta, k < 1 reduce.
 * (ajustarContraste del Taller 9)
 */
export function ajustarContraste(imagen: Imagen, k: number): Imagen {
  return mapearValores(imagen, (v) => recortar01((v - 0.5) * k + 0.5));
}

export type Zonas = "ninguno" | "claras" | "oscuras";

const LOG10_2 = Math.log10(2);
const E_MENOS_1 = Math.E - 1;

/**
 * Filtro de zonas (apuntes, sección 3.6), en forma normalizada para que el
 * resultado ocupe todo [0, 1]:
 *  - oscuras: log10(1 + I) / log10(2)  → realza el contraste de las zonas oscuras
 *  - claras:  (e^I − 1) / (e − 1)      → realza el contraste de las zonas claras
 */
export function filtrarZonas(imagen: Imagen, zonas: Zonas): Imagen {
  if (zonas === "oscuras") return mapearValores(imagen, (v) => Math.log10(1 + v) / LOG10_2);
  if (zonas === "claras") return mapearValores(imagen, (v) => (Math.exp(v) - 1) / E_MENOS_1);
  return imagen;
}
