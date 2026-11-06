import { createContext, useContext, useEffect, useState, type ReactNode } from "react";
import { tema, type Colores, type Esquema } from "./theme";

/** Convierte "rellenoFuerte" en "--relleno-fuerte". */
function nombreVariable(clave: string): string {
  return "--" + clave.replace(/[A-Z]/g, (m) => "-" + m.toLowerCase());
}

function bloqueVariables(colores: Colores): string {
  return Object.entries(colores)
    .map(([clave, valor]) => `${nombreVariable(clave)}: ${valor};`)
    .join(" ");
}

/** CSS generado a partir del tema: variables claras, oscuras y tipografía. */
function cssDelTema(): string {
  const otras = [
    ...Object.entries(tema.espacio).map(([k, v]) => `--esp-${k}: ${v};`),
    ...Object.entries(tema.tamanosTexto).map(([k, v]) => `--texto-${k}: ${v};`),
    `--fuente-manuscrita: ${tema.fuentes.manuscrita};`,
    `--fuente-mono: ${tema.fuentes.mono};`,
    `--ventana-ancho: ${tema.ventana.anchoMaximo};`,
    `--ventana-columnas: ${tema.ventana.columnas};`,
  ].join(" ");
  return `
:root { ${bloqueVariables(tema.colores.claro)} ${otras} color-scheme: light; }
@media (prefers-color-scheme: dark) {
  :root { ${bloqueVariables(tema.colores.oscuro)} color-scheme: dark; }
}`;
}

const ContextoEsquema = createContext<Esquema>("claro");

/** Esquema activo; lo necesitan las gráficas que se exportan como imagen. */
export function useEsquema(): Esquema {
  return useContext(ContextoEsquema);
}

export function useColores(): Colores {
  return tema.colores[useEsquema()];
}

export function ThemeProvider({ children }: { children: ReactNode }) {
  const consulta = "(prefers-color-scheme: dark)";
  const [esquema, setEsquema] = useState<Esquema>(() =>
    window.matchMedia(consulta).matches ? "oscuro" : "claro",
  );

  useEffect(() => {
    const media = window.matchMedia(consulta);
    const cambiar = () => setEsquema(media.matches ? "oscuro" : "claro");
    media.addEventListener("change", cambiar);
    return () => media.removeEventListener("change", cambiar);
  }, []);

  return (
    <ContextoEsquema.Provider value={esquema}>
      <style>{cssDelTema()}</style>
      {children}
    </ContextoEsquema.Provider>
  );
}
