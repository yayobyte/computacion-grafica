/**
 * Tema de la aplicación: el ÚNICO lugar donde se definen colores, fuentes,
 * espaciados y el "trazo a mano" de los bocetos.
 *
 * - Cambiar `trazo.roughness` cambia el descuido de todos los dibujos:
 *   0 = Arquitecto, 1 = Artista, 2 = Caricaturista (opciones de Excalidraw).
 * - Los colores se convierten en variables CSS (--papel, --tinta, ...) y
 *   tienen versión clara y oscura; el modo oscuro sigue al sistema operativo.
 */

export type Esquema = "claro" | "oscuro";

export interface Colores {
  papel: string; // fondo de la página
  superficie: string; // fondo de ventanas y tarjetas
  tinta: string; // trazo y texto principal
  tintaSuave: string; // texto secundario, controles deshabilitados
  relleno: string; // barras de título, botones
  rellenoFuerte: string; // botón principal, pestaña activa
  acento: string; // selección, foco, enlaces (azul de Excalidraw)
  acentoSuave: string; // fondo de elementos destacados
  aviso: string; // errores y advertencias
  rojo: string; // histograma: canal rojo
  verde: string; // histograma: canal verde
  azul: string; // histograma: canal azul
}

export const tema = {
  colores: {
    claro: {
      papel: "#fdfcf8",
      superficie: "#ffffff",
      tinta: "#1e1e1e",
      tintaSuave: "#868e96",
      relleno: "#e9ecef",
      rellenoFuerte: "#d0ebff",
      acento: "#1971c2",
      acentoSuave: "#e7f5ff",
      aviso: "#e8590c",
      rojo: "#e03131",
      verde: "#2f9e44",
      azul: "#1971c2",
    },
    oscuro: {
      papel: "#121212",
      superficie: "#1b1b1f",
      tinta: "#e3e3e8",
      tintaSuave: "#8b8b96",
      relleno: "#2a2a31",
      rellenoFuerte: "#1c3a57",
      acento: "#74c0fc",
      acentoSuave: "#16283a",
      aviso: "#ff922b",
      rojo: "#ff6b6b",
      verde: "#69db7c",
      azul: "#74c0fc",
    },
  } satisfies Record<Esquema, Colores>,

  fuentes: {
    // Excalifont (OFL) está en /public/fonts; Kalam es el respaldo de Google Fonts.
    manuscrita: '"Excalifont", "Kalam", "Comic Sans MS", cursive',
    mono: '"Cascadia Code", ui-monospace, "SFMono-Regular", Menlo, monospace',
  },

  tamanosTexto: {
    pequeno: "0.95rem",
    normal: "1.1rem",
    grande: "1.35rem",
    titulo: "2.6rem",
  },

  /** Parámetros de rough.js para todos los trazos de la interfaz. */
  trazo: {
    roughness: 2, // Caricaturista
    bowing: 1.6, // curvatura de las líneas rectas
    strokeWidth: 1.8,
    strokeWidthPrincipal: 3, // botón principal, pestaña activa
    fillStyle: "hachure" as const, // relleno con rayado a mano
    hachureGap: 7,
    hachureAngle: -41,
    fillWeight: 1.2,
  },

  /** Trazo más sereno para gráficas, para que los datos se lean bien. */
  trazoDatos: {
    roughness: 0.8,
    bowing: 0.5,
    strokeWidth: 1.6,
  },

  espacio: {
    xs: "4px",
    s: "8px",
    m: "14px",
    l: "22px",
    xl: "36px",
  },

  ventana: {
    anchoMaximo: "1240px",
    columnas: "minmax(0, 1.9fr) minmax(330px, 1fr)", // área de imagen : panel ≈ 2 : 1 (boceto)
    ladoMaximoVistaPrevia: 1600, // px; la vista previa se procesa reducida
  },
} as const;

export type Tema = typeof tema;
