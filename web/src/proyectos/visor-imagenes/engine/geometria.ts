import { crearImagen, type Imagen } from "./imagen";

/**
 * Rotación antihoraria por mapeo inverso (rotarImagen del Taller 9).
 *
 * Para cada píxel del lienzo de salida se calcula de qué píxel del original
 * viene (rotación con −θ), así no quedan huecos. El lienzo crece para que no
 * se corten las esquinas:
 *   alto'  = |alto·cos θ| + |ancho·sen θ|
 *   ancho' = |ancho·cos θ| + |alto·sen θ|
 * Lo que queda fuera de la imagen rotada es negro.
 */
export function rotar(imagen: Imagen, grados: number): Imagen {
  const normalizado = ((grados % 360) + 360) % 360;
  if (normalizado === 0) return imagen;
  const theta = (normalizado * Math.PI) / 180;
  const cos = Math.cos(theta);
  const sen = Math.sin(theta);
  const { ancho, alto, datos } = imagen;

  const nuevoAlto = Math.ceil(Math.abs(alto * cos) + Math.abs(ancho * sen) - 1e-9);
  const nuevoAncho = Math.ceil(Math.abs(ancho * cos) + Math.abs(alto * sen) - 1e-9);
  const salida = crearImagen(nuevoAncho, nuevoAlto);

  for (let fila = 0; fila < nuevoAlto; fila++) {
    const y = fila - nuevoAlto / 2;
    for (let col = 0; col < nuevoAncho; col++) {
      const x = col - nuevoAncho / 2;
      // Mapeo inverso; el eje y apunta hacia abajo, por eso estos signos
      const xo = Math.round(cos * x - sen * y + ancho / 2);
      const yo = Math.round(sen * x + cos * y + alto / 2);
      if (xo < 0 || xo >= ancho || yo < 0 || yo >= alto) continue;
      const o = (yo * ancho + xo) * 3;
      const s = (fila * nuevoAncho + col) * 3;
      salida.datos[s] = datos[o];
      salida.datos[s + 1] = datos[o + 1];
      salida.datos[s + 2] = datos[o + 2];
    }
  }
  return salida;
}

export interface RegionZoom {
  x: number; // columna de la esquina superior izquierda
  y: number; // fila de la esquina superior izquierda
  ancho: number;
  alto: number;
}

/**
 * Región que se amplía: empieza en (x, y) y mide ancho/factor × alto/factor,
 * para que al ampliarla ocupe aproximadamente lo mismo que la imagen original.
 * Si (x, y) dejaría la región fuera de la imagen, se desplaza hacia adentro.
 */
export function regionZoom(ancho: number, alto: number, x: number, y: number, factor: number): RegionZoom {
  const anchoRegion = Math.max(1, Math.floor(ancho / factor));
  const altoRegion = Math.max(1, Math.floor(alto / factor));
  return {
    x: Math.min(Math.max(0, Math.round(x)), ancho - anchoRegion),
    y: Math.min(Math.max(0, Math.round(y)), alto - altoRegion),
    ancho: anchoRegion,
    alto: altoRegion,
  };
}

/**
 * Zoom: recorta la región y repite cada píxel en un bloque factor × factor
 * (vecino más cercano; la idea de np.kron del Taller 9). No agrega detalle.
 */
export function ampliarRegion(imagen: Imagen, x: number, y: number, factor: number): Imagen {
  if (factor <= 1) return imagen;
  const r = regionZoom(imagen.ancho, imagen.alto, x, y, factor);
  const anchoSalida = Math.round(r.ancho * factor);
  const altoSalida = Math.round(r.alto * factor);
  const salida = crearImagen(anchoSalida, altoSalida);
  for (let fila = 0; fila < altoSalida; fila++) {
    const fo = r.y + Math.min(r.alto - 1, Math.floor(fila / factor));
    for (let col = 0; col < anchoSalida; col++) {
      const co = r.x + Math.min(r.ancho - 1, Math.floor(col / factor));
      const o = (fo * imagen.ancho + co) * 3;
      const s = (fila * anchoSalida + col) * 3;
      salida.datos[s] = imagen.datos[o];
      salida.datos[s + 1] = imagen.datos[o + 1];
      salida.datos[s + 2] = imagen.datos[o + 2];
    }
  }
  return salida;
}

/** Cambia el tamaño con interpolación bilineal (para fusionar y para la vista previa). */
export function redimensionar(imagen: Imagen, nuevoAncho: number, nuevoAlto: number): Imagen {
  if (nuevoAncho === imagen.ancho && nuevoAlto === imagen.alto) return imagen;
  const salida = crearImagen(nuevoAncho, nuevoAlto);
  const { ancho, alto, datos } = imagen;
  const ex = ancho / nuevoAncho;
  const ey = alto / nuevoAlto;
  for (let fila = 0; fila < nuevoAlto; fila++) {
    const yf = Math.min(alto - 1, Math.max(0, (fila + 0.5) * ey - 0.5));
    const y0 = Math.floor(yf);
    const y1 = Math.min(alto - 1, y0 + 1);
    const dy = yf - y0;
    for (let col = 0; col < nuevoAncho; col++) {
      const xf = Math.min(ancho - 1, Math.max(0, (col + 0.5) * ex - 0.5));
      const x0 = Math.floor(xf);
      const x1 = Math.min(ancho - 1, x0 + 1);
      const dx = xf - x0;
      const s = (fila * nuevoAncho + col) * 3;
      for (let c = 0; c < 3; c++) {
        const a = datos[(y0 * ancho + x0) * 3 + c];
        const b = datos[(y0 * ancho + x1) * 3 + c];
        const d = datos[(y1 * ancho + x0) * 3 + c];
        const e = datos[(y1 * ancho + x1) * 3 + c];
        salida.datos[s + c] = (a * (1 - dx) + b * dx) * (1 - dy) + (d * (1 - dx) + e * dx) * dy;
      }
    }
  }
  return salida;
}
