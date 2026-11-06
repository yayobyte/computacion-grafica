import { useEffect, useRef } from "react";
import { Boton, Campo, Deslizador, Fase2 } from "../../../sketch/componentes";
import { aImageData } from "../engine/imagen";
import { redimensionar } from "../engine/geometria";
import { EXTENSIONES_VALIDAS } from "../engine/archivos";
import type { Visor } from "../estado";

const ANCHO_MINIATURA = 260;

/** Pantalla 2D: segunda imagen, transparencia y botones de fusión. */
export function PanelFusion({ visor, deshabilitado }: { visor: Visor; deshabilitado: boolean }) {
  const { ajustes, cambiar, segunda, elegirSegunda, quitarSegunda } = visor;
  const entrada = useRef<HTMLInputElement>(null);
  const lienzo = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    if (!segunda || !lienzo.current) return;
    const alto = Math.max(1, Math.round((segunda.vista.alto / segunda.vista.ancho) * ANCHO_MINIATURA));
    const mini = redimensionar(segunda.vista, ANCHO_MINIATURA, alto);
    lienzo.current.width = mini.ancho;
    lienzo.current.height = mini.alto;
    lienzo.current.getContext("2d")!.putImageData(aImageData(mini), 0, 0);
  }, [segunda]);

  return (
    <>
      <div className="sk-fila fila-ruta-panel">
        <Campo
          readOnly
          value={segunda?.nombre ?? ""}
          placeholder="Segunda imagen"
          aria-label="Segunda imagen"
          disabled={deshabilitado}
        />
        <Boton disabled={deshabilitado} onClick={() => entrada.current?.click()}>
          Explorar…
        </Boton>
        <input
          ref={entrada}
          type="file"
          accept={EXTENSIONES_VALIDAS.join(",")}
          hidden
          onChange={(e) => {
            const archivo = e.target.files?.[0];
            if (archivo) void elegirSegunda(archivo);
            e.target.value = "";
          }}
        />
      </div>
      <div className="miniatura-zoom">
        {segunda ? (
          <canvas ref={lienzo} aria-label={`Miniatura de ${segunda.nombre}`} />
        ) : (
          <span className="suave">Elige la imagen que se fusionará con la principal.</span>
        )}
      </div>
      <Deslizador
        id="transparencia"
        etiqueta="Transpar."
        valor={ajustes.fusion.transparencia}
        min={0}
        max={1}
        paso={0.01}
        decimales={2}
        etiquetaMin="0 opaca"
        etiquetaMax="1 transp."
        onCambio={(transparencia) => cambiar({ fusion: { ...ajustes.fusion, transparencia } })}
        deshabilitado={deshabilitado || !segunda}
      />
      <div className="sk-fila">
        <span>Modo</span>
        <Campo value="Normal" readOnly disabled aria-label="Modo de fusión" />
        <Fase2 />
      </div>
      <div className="botones-panel">
        <Boton disabled={deshabilitado || !segunda} onClick={quitarSegunda}>
          Quitar fusión
        </Boton>
        <Boton
          principal
          disabled={deshabilitado || !segunda}
          onClick={() => cambiar({ fusion: { ...ajustes.fusion, activa: true } })}
        >
          Fusionar
        </Boton>
      </div>
    </>
  );
}
