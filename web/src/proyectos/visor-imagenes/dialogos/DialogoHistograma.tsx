import { useMemo, useRef, useState } from "react";
import rough from "roughjs";
import { Boton, Dialogo, Opcion } from "../../../sketch/componentes";
import { useColores } from "../../../theme/ThemeProvider";
import { tema } from "../../../theme/theme";
import { calcularHistograma } from "../engine/histograma";
import { descargar } from "../engine/archivos";
import type { Imagen } from "../engine/imagen";

const generador = rough.generator();
const ANCHO = 640;
const ALTO = 380;

interface Serie {
  nombre: string;
  color: string;
  datos: Uint32Array;
}

interface Panel {
  x: number;
  y: number;
  ancho: number;
  alto: number;
  titulo?: string;
  series: Serie[];
}

/** Caminos de rough.js de un panel: ejes y una línea por serie. */
function caminosPanel(p: Panel, colorEjes: string, semilla: number) {
  const opciones = { ...tema.trazoDatos, seed: semilla };
  const izq = p.x + 44;
  const der = p.x + p.ancho - 10;
  const arriba = p.y + (p.titulo ? 28 : 12);
  const abajo = p.y + p.alto - 30;
  const maximo = Math.max(1, ...p.series.map((s) => Math.max(...s.datos)));
  const caminos: { d: string; color: string; grosor: number }[] = [];
  const agregar = (dibujo: ReturnType<typeof generador.line>, color: string) =>
    generador.toPaths(dibujo).forEach((c) => caminos.push({ d: c.d, color, grosor: c.strokeWidth }));

  agregar(generador.line(izq, abajo, der, abajo, { ...opciones, stroke: "x" }), colorEjes);
  agregar(generador.line(izq, arriba, izq, abajo, { ...opciones, stroke: "x" }), colorEjes);
  p.series.forEach((s, i) => {
    const puntos: [number, number][] = Array.from(s.datos, (v, nivel) => [
      izq + (nivel / 255) * (der - izq),
      abajo - (v / maximo) * (abajo - arriba),
    ]);
    agregar(generador.linearPath(puntos, { ...opciones, seed: semilla + i + 1, stroke: "x" }), s.color);
  });
  return { caminos, izq, der, arriba, abajo, maximo };
}

function GraficaHistograma({ paneles, svgRef }: { paneles: Panel[]; svgRef: React.RefObject<SVGSVGElement> }) {
  const colores = useColores();
  const dibujos = useMemo(
    () => paneles.map((p, i) => ({ panel: p, ...caminosPanel(p, colores.tinta, 11 + i * 7) })),
    [paneles, colores.tinta],
  );

  return (
    <svg
      ref={svgRef}
      viewBox={`0 0 ${ANCHO} ${ALTO}`}
      width="100%"
      role="img"
      aria-label="Histograma de los canales rojo, verde, azul y de la luminosidad"
      style={{ fontFamily: tema.fuentes.manuscrita, display: "block" }}
    >
      <rect x="0" y="0" width={ANCHO} height={ALTO} fill={colores.superficie} />
      {dibujos.map(({ panel, caminos, izq, der, abajo, arriba, maximo }, i) => (
        <g key={i}>
          {panel.titulo && (
            <text x={panel.x + 8} y={panel.y + 18} fill={colores.tinta} fontSize="16">
              {panel.titulo}
            </text>
          )}
          {caminos.map((c, j) => (
            <path key={j} d={c.d} stroke={c.color} strokeWidth={c.grosor} fill="none" strokeLinecap="round" />
          ))}
          {[0, 128, 255].map((n) => (
            <text
              key={n}
              x={izq + (n / 255) * (der - izq)}
              y={abajo + 16}
              fill={colores.tintaSuave}
              fontSize="12"
              textAnchor="middle"
            >
              {n}
            </text>
          ))}
          <text x={izq - 6} y={arriba + 10} fill={colores.tintaSuave} fontSize="11" textAnchor="end">
            {maximo}
          </text>
          <text x={izq - 6} y={abajo} fill={colores.tintaSuave} fontSize="11" textAnchor="end">
            0
          </text>
        </g>
      ))}
    </svg>
  );
}

/** Pantalla 3: histograma de R, G, B y luminosidad, separados o superpuestos. */
export function DialogoHistograma({
  imagen,
  nombre,
  onCerrar,
}: {
  imagen: Imagen;
  nombre: string;
  onCerrar: () => void;
}) {
  const colores = useColores();
  const [vista, setVista] = useState<"separados" | "superpuestos">("separados");
  const svgRef = useRef<SVGSVGElement>(null);
  const histograma = useMemo(() => calcularHistograma(imagen), [imagen]);

  const series: Serie[] = useMemo(
    () => [
      { nombre: "Rojo", color: colores.rojo, datos: histograma.rojo },
      { nombre: "Verde", color: colores.verde, datos: histograma.verde },
      { nombre: "Azul", color: colores.azul, datos: histograma.azul },
      { nombre: "Luminosidad", color: colores.tinta, datos: histograma.luminosidad },
    ],
    [histograma, colores],
  );

  const paneles: Panel[] = useMemo(() => {
    if (vista === "superpuestos") {
      return [{ x: 0, y: 0, ancho: ANCHO, alto: ALTO, series }];
    }
    const w = ANCHO / 2;
    const h = ALTO / 2;
    return series.map((s, i) => ({
      x: (i % 2) * w,
      y: Math.floor(i / 2) * h,
      ancho: w,
      alto: h,
      titulo: s.nombre,
      series: [s],
    }));
  }, [vista, series]);

  const guardarGrafica = () => {
    const svg = svgRef.current;
    if (!svg) return;
    const texto = new XMLSerializer().serializeToString(svg);
    const url = URL.createObjectURL(new Blob([texto], { type: "image/svg+xml" }));
    const img = new Image();
    img.onload = () => {
      const lienzo = document.createElement("canvas");
      lienzo.width = ANCHO * 2;
      lienzo.height = ALTO * 2;
      const ctx = lienzo.getContext("2d")!;
      ctx.drawImage(img, 0, 0, lienzo.width, lienzo.height);
      URL.revokeObjectURL(url);
      lienzo.toBlob((b) => b && descargar(b, "histograma.png"), "image/png");
    };
    img.src = url;
  };

  return (
    <Dialogo
      titulo={`Histograma — ${nombre}`}
      onCerrar={onCerrar}
      ancho={720}
      pie={
        <>
          <Boton onClick={guardarGrafica}>Guardar gráfica…</Boton>
          <Boton principal onClick={onCerrar}>
            Cerrar
          </Boton>
        </>
      }
    >
      <div className="sk-fila">
        <span>Vista:</span>
        <Opcion nombre="vista-histograma" marcada={vista === "separados"} onElegir={() => setVista("separados")}>
          Separados
        </Opcion>
        <Opcion nombre="vista-histograma" marcada={vista === "superpuestos"} onElegir={() => setVista("superpuestos")}>
          Superpuestos
        </Opcion>
      </div>
      <GraficaHistograma paneles={paneles} svgRef={svgRef} />
      {vista === "superpuestos" && (
        <div className="sk-fila leyenda">
          {series.map((s) => (
            <span key={s.nombre}>
              <span className="muestra-color" style={{ background: s.color }} /> {s.nombre}
            </span>
          ))}
        </div>
      )}
      <span className="suave nota">
        Eje X: intensidad 0–255 · Eje Y: número de píxeles · {histograma.totalPixeles.toLocaleString("es-CO")} píxeles
        en la vista previa
      </span>
    </Dialogo>
  );
}
