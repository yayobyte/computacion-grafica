import { useCallback, useDeferredValue, useMemo, useState } from "react";
import { tema } from "../../theme/theme";
import { type Imagen } from "./engine/imagen";
import { redimensionar } from "./engine/geometria";
import { AJUSTES_INICIALES, aplicarAjustes, type Ajustes } from "./engine/pipeline";
import { codificar, descargar, esFormatoValido, leerArchivo, type FormatoGuardado } from "./engine/archivos";

export type Dialogo =
  | { tipo: "histograma" }
  | { tipo: "guardar" }
  | { tipo: "error"; mensaje: string }
  | { tipo: "tamano"; segunda: Imagen; nombre: string }
  | { tipo: "ayuda" };

interface SegundaImagen {
  nombre: string;
  completa: Imagen; // del tamaño de la imagen principal
  vista: Imagen; // del tamaño de la vista previa
}

/** Reduce una imagen para la vista previa (≤ ladoMaximoVistaPrevia en su lado mayor). */
function reducirParaVista(imagen: Imagen): { vista: Imagen; escala: number } {
  const lado = Math.max(imagen.ancho, imagen.alto);
  const escala = Math.min(1, tema.ventana.ladoMaximoVistaPrevia / lado);
  if (escala === 1) return { vista: imagen, escala };
  const ancho = Math.max(1, Math.round(imagen.ancho * escala));
  const alto = Math.max(1, Math.round(imagen.alto * escala));
  return { vista: redimensionar(imagen, ancho, alto), escala: ancho / imagen.ancho };
}

function nombreSinExtension(nombre: string): string {
  return nombre.replace(/\.[^.]+$/, "");
}

/**
 * Estado y acciones del visor. La interfaz (VisorPage y sus paneles) solo lee
 * este estado y llama a las acciones; la lógica de imagen está en engine/.
 */
export function useVisor() {
  const [archivoElegido, setArchivoElegido] = useState<File | null>(null);
  const [nombreCargado, setNombreCargado] = useState("");
  const [original, setOriginal] = useState<Imagen | null>(null);
  const [vista, setVista] = useState<{ vista: Imagen; escala: number } | null>(null);
  const [segunda, setSegunda] = useState<SegundaImagen | null>(null);
  const [ajustes, setAjustes] = useState<Ajustes>(AJUSTES_INICIALES);
  const [ajustesAplicados, setAjustesAplicados] = useState<Ajustes>(AJUSTES_INICIALES);
  const [autoActualizar, setAutoActualizarEstado] = useState(true);
  const [dialogo, setDialogo] = useState<Dialogo | null>(null);
  const [mensaje, setMensaje] = useState("Listo. Selecciona una imagen para empezar.");
  const [ocupado, setOcupado] = useState(false);

  // Con "Actualizar al mover" la vista sigue a los controles; sin él, solo cambia al pulsar Actualizar
  const vigentes = autoActualizar ? ajustes : ajustesAplicados;
  const diferidos = useDeferredValue(vigentes);

  const resultado = useMemo(() => {
    if (!vista) return null;
    return aplicarAjustes(vista.vista, segunda?.vista ?? null, diferidos, vista.escala);
  }, [vista, segunda, diferidos]);

  const pendientes = !autoActualizar && ajustes !== ajustesAplicados;

  const cambiar = useCallback((parcial: Partial<Ajustes>) => {
    setAjustes((a) => ({ ...a, ...parcial }));
  }, []);

  const elegirArchivo = useCallback((archivo: File) => {
    if (!esFormatoValido(archivo.name)) {
      setDialogo({
        tipo: "error",
        mensaje: `No se pudo abrir "${archivo.name}". El visor acepta JPG, PNG y BMP. Elige otro archivo.`,
      });
      return;
    }
    setArchivoElegido(archivo);
    setMensaje(`Archivo elegido: ${archivo.name}. Pulsa Cargar para mostrarlo.`);
  }, []);

  const cargar = useCallback(async () => {
    if (!archivoElegido) return;
    setOcupado(true);
    try {
      const imagen = await leerArchivo(archivoElegido);
      setOriginal(imagen);
      setVista(reducirParaVista(imagen));
      setSegunda(null);
      setAjustes(AJUSTES_INICIALES);
      setAjustesAplicados(AJUSTES_INICIALES);
      setNombreCargado(archivoElegido.name);
      setMensaje(`${archivoElegido.name} cargada. Usa las pestañas para editarla.`);
    } catch {
      setDialogo({
        tipo: "error",
        mensaje: `No se pudo leer "${archivoElegido.name}". El archivo puede estar dañado. Prueba con otra imagen.`,
      });
    } finally {
      setOcupado(false);
    }
  }, [archivoElegido]);

  const actualizar = useCallback(() => {
    setAjustesAplicados(ajustes);
    setMensaje("Ajustes aplicados ✓");
  }, [ajustes]);

  const restaurar = useCallback(() => {
    setAjustes(AJUSTES_INICIALES);
    setAjustesAplicados(AJUSTES_INICIALES);
    setMensaje("Imagen restaurada a sus valores originales.");
  }, []);

  const setAutoActualizar = useCallback(
    (activo: boolean) => {
      setAutoActualizarEstado(activo);
      if (!activo) setAjustesAplicados(ajustes);
    },
    [ajustes],
  );

  const instalarSegunda = useCallback(
    (imagen: Imagen, nombre: string) => {
      if (!original || !vista) return;
      const completa = redimensionar(imagen, original.ancho, original.alto);
      setSegunda({ nombre, completa, vista: redimensionar(completa, vista.vista.ancho, vista.vista.alto) });
      setAjustes((a) => ({ ...a, fusion: { ...a.fusion, activa: true } }));
      setMensaje(`Fusión con ${nombre}. Ajusta la transparencia.`);
    },
    [original, vista],
  );

  const elegirSegunda = useCallback(
    async (archivo: File) => {
      if (!original) return;
      if (!esFormatoValido(archivo.name)) {
        setDialogo({
          tipo: "error",
          mensaje: `No se pudo abrir "${archivo.name}". El visor acepta JPG, PNG y BMP. Elige otro archivo.`,
        });
        return;
      }
      try {
        const imagen = await leerArchivo(archivo);
        if (imagen.ancho !== original.ancho || imagen.alto !== original.alto) {
          setDialogo({ tipo: "tamano", segunda: imagen, nombre: archivo.name });
        } else {
          instalarSegunda(imagen, archivo.name);
        }
      } catch {
        setDialogo({ tipo: "error", mensaje: `No se pudo leer "${archivo.name}". Prueba con otra imagen.` });
      }
    },
    [original, instalarSegunda],
  );

  const quitarSegunda = useCallback(() => {
    setSegunda(null);
    setAjustes((a) => ({ ...a, fusion: { ...a.fusion, activa: false } }));
    setMensaje("Fusión quitada.");
  }, []);

  const guardar = useCallback(
    async (nombre: string, formato: FormatoGuardado) => {
      if (!original) return;
      setOcupado(true);
      try {
        const final = aplicarAjustes(original, segunda?.completa ?? null, vigentes, 1);
        const blob = await codificar(final, formato);
        const nombreFinal = `${nombre.trim() || "imagen_editada"}.${formato}`;
        descargar(blob, nombreFinal);
        setMensaje(`Guardado como ${nombreFinal} (${final.ancho} × ${final.alto} px) ✓`);
        setDialogo(null);
      } catch {
        setDialogo({ tipo: "error", mensaje: "No se pudo guardar la imagen. Inténtalo de nuevo." });
      } finally {
        setOcupado(false);
      }
    },
    [original, segunda, vigentes],
  );

  return {
    archivoElegido,
    nombreCargado,
    nombreSugerido: nombreSinExtension(nombreCargado) + "_editado",
    original,
    vistaBase: vista?.vista ?? null,
    resultado,
    segunda,
    ajustes,
    autoActualizar,
    pendientes,
    dialogo,
    mensaje,
    ocupado,
    cambiar,
    elegirArchivo,
    cargar,
    actualizar,
    restaurar,
    setAutoActualizar,
    elegirSegunda,
    instalarSegunda,
    quitarSegunda,
    guardar,
    abrirDialogo: setDialogo,
    cerrarDialogo: () => setDialogo(null),
  };
}

export type Visor = ReturnType<typeof useVisor>;
