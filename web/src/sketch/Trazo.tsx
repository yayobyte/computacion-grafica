import { useId, useLayoutEffect, useMemo, useRef, useState } from "react";
import rough from "roughjs";
import type { Options } from "roughjs/bin/core";
import { tema } from "../theme/theme";
import "./sketch.css";

/**
 * Dibujo a mano alzada que se ajusta al tamaño de su contenedor.
 *
 * Se pone como primer hijo de un elemento con `position: relative`; mide ese
 * elemento y dibuja la forma con rough.js. Los colores son variables CSS, así
 * que el dibujo cambia solo entre modo claro y oscuro.
 */

export type Forma = "rect" | "elipse" | "lineaInferior" | "lineaSuperior" | "lineaDerecha" | "marca";

export interface PropsTrazo {
  forma?: Forma;
  trazo?: string; // color CSS del borde, p. ej. "var(--tinta)"
  relleno?: string; // color CSS del relleno; sin relleno si se omite
  estiloRelleno?: "hachure" | "solid" | "cross-hatch" | "zigzag";
  grosor?: number;
  discontinuo?: boolean;
  margen?: number; // separación entre el borde del elemento y el trazo
  opciones?: Options; // ajustes finos de rough.js
}

const generador = rough.generator();
const COLOR_TRAZO = "#000001"; // marcadores que luego se cambian por variables CSS
const COLOR_RELLENO = "#000002";

/** Semilla estable a partir del id de React: el dibujo no "tiembla" al re-renderizar. */
function semillaDesde(texto: string): number {
  let h = 2166136261;
  for (let i = 0; i < texto.length; i++) {
    h ^= texto.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return (Math.abs(h) % 2_000_000) + 1;
}

export function Trazo({
  forma = "rect",
  trazo = "var(--tinta)",
  relleno,
  estiloRelleno = tema.trazo.fillStyle,
  grosor = tema.trazo.strokeWidth,
  discontinuo = false,
  margen = 2,
  opciones,
}: PropsTrazo) {
  const ref = useRef<SVGSVGElement>(null);
  const [tamano, setTamano] = useState({ ancho: 0, alto: 0 });
  const semilla = semillaDesde(useId());

  useLayoutEffect(() => {
    const padre = ref.current?.parentElement;
    if (!padre) return;
    const medir = () => setTamano({ ancho: padre.offsetWidth, alto: padre.offsetHeight });
    medir();
    const observador = new ResizeObserver(medir);
    observador.observe(padre);
    return () => observador.disconnect();
  }, []);

  const caminos = useMemo(() => {
    const { ancho, alto } = tamano;
    if (ancho < 2 || alto < 2) return [];
    const o: Options = {
      roughness: tema.trazo.roughness,
      bowing: tema.trazo.bowing,
      strokeWidth: grosor,
      stroke: COLOR_TRAZO,
      fill: relleno ? COLOR_RELLENO : undefined,
      fillStyle: estiloRelleno,
      hachureGap: tema.trazo.hachureGap,
      hachureAngle: tema.trazo.hachureAngle,
      fillWeight: tema.trazo.fillWeight,
      strokeLineDash: discontinuo ? [8, 7] : undefined,
      seed: semilla,
      // Formas pequeñas: menos descuido para que sigan siendo legibles
      ...(Math.min(ancho, alto) < 28 ? { roughness: Math.min(tema.trazo.roughness, 1.2), bowing: 0.8 } : {}),
      ...opciones,
    };
    const m = margen;
    let dibujo;
    switch (forma) {
      case "elipse":
        dibujo = generador.ellipse(ancho / 2, alto / 2, ancho - 2 * m, alto - 2 * m, o);
        break;
      case "lineaInferior":
        dibujo = generador.line(0, alto - m, ancho, alto - m, o);
        break;
      case "lineaSuperior":
        dibujo = generador.line(0, m, ancho, m, o);
        break;
      case "lineaDerecha":
        dibujo = generador.line(ancho - m, 0, ancho - m, alto, o);
        break;
      case "marca":
        dibujo = generador.linearPath(
          [
            [ancho * 0.18, alto * 0.52],
            [ancho * 0.42, alto * 0.78],
            [ancho * 0.84, alto * 0.2],
          ],
          o,
        );
        break;
      default:
        dibujo = generador.rectangle(m, m, ancho - 2 * m, alto - 2 * m, o);
    }
    return generador.toPaths(dibujo);
  }, [tamano, forma, relleno, estiloRelleno, grosor, discontinuo, margen, opciones, semilla]);

  return (
    <svg ref={ref} className="trazo" width={tamano.ancho} height={tamano.alto} aria-hidden="true">
      {caminos.map((c, i) => {
        const esRelleno = c.stroke === COLOR_RELLENO || c.fill === COLOR_RELLENO;
        const colorTrazo = c.stroke === COLOR_TRAZO ? trazo : c.stroke === COLOR_RELLENO ? relleno : "none";
        return (
          <path
            key={i}
            d={c.d}
            style={{
              stroke: colorTrazo,
              strokeWidth: c.strokeWidth,
              fill: c.fill === COLOR_RELLENO ? relleno : "none",
              strokeDasharray: discontinuo && !esRelleno ? "8 7" : undefined,
            }}
          />
        );
      })}
    </svg>
  );
}
