import { useEffect, useRef } from "react";
import { Boton, Campo, Casilla, Deslizador, Fase2, Grupo } from "../../../sketch/componentes";
import { aImageData } from "../engine/imagen";
import { redimensionar, regionZoom } from "../engine/geometria";
import type { Visor } from "../estado";

const ANCHO_MINIATURA = 260;

/** Pantalla 2C: punto inicial (X, Y), factor y vista previa de la región. */
export function PanelZoom({ visor, deshabilitado }: { visor: Visor; deshabilitado: boolean }) {
  const { ajustes, cambiar, original, vistaBase } = visor;
  const lienzo = useRef<HTMLCanvasElement>(null);
  const maxX = original ? original.ancho - 1 : 0;
  const maxY = original ? original.alto - 1 : 0;

  // Miniatura de la imagen original (sin ajustes)
  useEffect(() => {
    if (!vistaBase || !lienzo.current) return;
    const alto = Math.max(1, Math.round((vistaBase.alto / vistaBase.ancho) * ANCHO_MINIATURA));
    const mini = redimensionar(vistaBase, ANCHO_MINIATURA, alto);
    lienzo.current.width = mini.ancho;
    lienzo.current.height = mini.alto;
    lienzo.current.getContext("2d")!.putImageData(aImageData(mini), 0, 0);
  }, [vistaBase]);

  const region = original
    ? regionZoom(original.ancho, original.alto, ajustes.zoom.x, ajustes.zoom.y, ajustes.zoom.factor)
    : null;

  const cambiarZoom = (parcial: Partial<typeof ajustes.zoom>) => cambiar({ zoom: { ...ajustes.zoom, ...parcial } });

  const leerEntero = (texto: string, max: number) => {
    const n = Math.round(Number(texto));
    return Number.isFinite(n) ? Math.min(max, Math.max(0, n)) : 0;
  };

  return (
    <>
      <Grupo titulo="Punto inicial (px)">
        <div className="sk-fila">
          <label className="campo-xy">
            X
            <Campo
              type="number"
              min={0}
              max={maxX}
              value={ajustes.zoom.x}
              disabled={deshabilitado}
              onChange={(e) => cambiarZoom({ x: leerEntero(e.target.value, maxX) })}
            />
          </label>
          <label className="campo-xy">
            Y
            <Campo
              type="number"
              min={0}
              max={maxY}
              value={ajustes.zoom.y}
              disabled={deshabilitado}
              onChange={(e) => cambiarZoom({ y: leerEntero(e.target.value, maxY) })}
            />
          </label>
        </div>
        <span className="suave nota">
          Máx.: X {maxX} · Y {maxY}
        </span>
      </Grupo>
      <Deslizador
        id="factor"
        etiqueta="Factor"
        valor={ajustes.zoom.factor}
        min={1}
        max={10}
        paso={0.5}
        decimales={1}
        sufijo="×"
        etiquetaMin="1×"
        etiquetaMax="10×"
        onCambio={(factor) => cambiarZoom({ factor })}
        deshabilitado={deshabilitado}
      />
      <div className="miniatura-zoom">
        {vistaBase && <canvas ref={lienzo} aria-label="Miniatura con la región del zoom" />}
        {original && region && (
          <span
            className="marco-zoom"
            style={{
              left: `${(region.x / original.ancho) * 100}%`,
              top: `${(region.y / original.alto) * 100}%`,
              width: `${(region.ancho / original.ancho) * 100}%`,
              height: `${(region.alto / original.alto) * 100}%`,
            }}
          />
        )}
        {!vistaBase && <span className="suave">Carga una imagen para ver la región.</span>}
      </div>
      <Casilla marcada={false} onCambio={() => undefined} deshabilitada>
        Seleccionar con el ratón <Fase2 />
      </Casilla>
      <div className="botones-panel">
        <Boton disabled={deshabilitado || !ajustes.zoom.activo} onClick={() => cambiarZoom({ activo: false })}>
          Quitar zoom
        </Boton>
        <Boton principal disabled={deshabilitado} onClick={() => cambiarZoom({ activo: true })}>
          Aplicar zoom
        </Boton>
      </div>
    </>
  );
}
