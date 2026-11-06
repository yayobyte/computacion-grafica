import { aImageData, desdeImageData, type Imagen } from "./imagen";

/** Formatos que acepta el visor (requisito: JPG, PNG y BMP). */
export const EXTENSIONES_VALIDAS = [".jpg", ".jpeg", ".png", ".bmp"];

export function esFormatoValido(nombre: string): boolean {
  const n = nombre.toLowerCase();
  return EXTENSIONES_VALIDAS.some((ext) => n.endsWith(ext));
}

/** Decodifica un archivo de imagen con el navegador y lo convierte a Imagen. */
export async function leerArchivo(archivo: File): Promise<Imagen> {
  const mapa = await createImageBitmap(archivo);
  const lienzo = document.createElement("canvas");
  lienzo.width = mapa.width;
  lienzo.height = mapa.height;
  const ctx = lienzo.getContext("2d", { willReadFrequently: true });
  if (!ctx) throw new Error("El navegador no permite leer la imagen.");
  // Fondo blanco: un PNG transparente se ve sobre blanco, como en la mayoría de visores
  ctx.fillStyle = "#ffffff";
  ctx.fillRect(0, 0, mapa.width, mapa.height);
  ctx.drawImage(mapa, 0, 0);
  mapa.close();
  return desdeImageData(ctx.getImageData(0, 0, lienzo.width, lienzo.height));
}

export function aLienzo(imagen: Imagen): HTMLCanvasElement {
  const lienzo = document.createElement("canvas");
  lienzo.width = imagen.ancho;
  lienzo.height = imagen.alto;
  lienzo.getContext("2d")!.putImageData(aImageData(imagen), 0, 0);
  return lienzo;
}

/**
 * Codifica BMP de 24 bits sin compresión (los navegadores no exportan BMP).
 * Filas de abajo hacia arriba, píxeles en orden B, G, R, cada fila rellena a
 * múltiplo de 4 bytes.
 */
export function codificarBMP(imagen: Imagen): Blob {
  const { width: ancho, height: alto, data } = aImageData(imagen);
  const bytesFila = Math.ceil((ancho * 3) / 4) * 4;
  const tamanoDatos = bytesFila * alto;
  const buffer = new ArrayBuffer(54 + tamanoDatos);
  const v = new DataView(buffer);
  v.setUint8(0, 0x42); // 'B'
  v.setUint8(1, 0x4d); // 'M'
  v.setUint32(2, 54 + tamanoDatos, true);
  v.setUint32(10, 54, true); // inicio de los píxeles
  v.setUint32(14, 40, true); // tamaño de la cabecera BITMAPINFOHEADER
  v.setInt32(18, ancho, true);
  v.setInt32(22, alto, true);
  v.setUint16(26, 1, true); // planos
  v.setUint16(28, 24, true); // bits por píxel
  v.setUint32(34, tamanoDatos, true);
  v.setInt32(38, 2835, true); // 72 ppp
  v.setInt32(42, 2835, true);
  const bytes = new Uint8Array(buffer);
  for (let fila = 0; fila < alto; fila++) {
    const destino = 54 + (alto - 1 - fila) * bytesFila;
    for (let col = 0; col < ancho; col++) {
      const o = (fila * ancho + col) * 4;
      const d = destino + col * 3;
      bytes[d] = data[o + 2];
      bytes[d + 1] = data[o + 1];
      bytes[d + 2] = data[o];
    }
  }
  return new Blob([buffer], { type: "image/bmp" });
}

export type FormatoGuardado = "png" | "jpg" | "bmp";

export async function codificar(imagen: Imagen, formato: FormatoGuardado): Promise<Blob> {
  if (formato === "bmp") return codificarBMP(imagen);
  const tipo = formato === "png" ? "image/png" : "image/jpeg";
  return new Promise((resolver, rechazar) =>
    aLienzo(imagen).toBlob((b) => (b ? resolver(b) : rechazar(new Error("No se pudo codificar la imagen."))), tipo, 0.92),
  );
}

/** Descarga un Blob con el nombre dado. */
export function descargar(blob: Blob, nombre: string): void {
  const url = URL.createObjectURL(blob);
  const enlace = document.createElement("a");
  enlace.href = url;
  enlace.download = nombre;
  document.body.appendChild(enlace);
  enlace.click();
  enlace.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}
