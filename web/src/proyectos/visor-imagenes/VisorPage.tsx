import { useEffect, useRef, useState } from "react";
import { Link } from "react-router-dom";
import { BarraMenu, Boton, Campo, Casilla, Linea, Pestanas } from "../../sketch/componentes";
import { Trazo } from "../../sketch/Trazo";
import { aImageData } from "./engine/imagen";
import { EXTENSIONES_VALIDAS } from "./engine/archivos";
import { useVisor } from "./estado";
import { PanelAjustes } from "./paneles/PanelAjustes";
import { PanelColor } from "./paneles/PanelColor";
import { PanelZoom } from "./paneles/PanelZoom";
import { PanelFusion } from "./paneles/PanelFusion";
import { DialogoHistograma } from "./dialogos/DialogoHistograma";
import { DialogoAyuda, DialogoError, DialogoGuardar, DialogoTamano } from "./dialogos/Dialogos";
import "./visor.css";

const PESTANAS = [
  { id: "ajustes", texto: "Ajustes" },
  { id: "color", texto: "Color" },
  { id: "zoom", texto: "Zoom" },
  { id: "fusion", texto: "Fusión" },
] as const;
type IdPestana = (typeof PESTANAS)[number]["id"];

/**
 * Ventana principal del visor (pantallas 1 y 2A–2D del boceto, opción B):
 * área de imagen a la izquierda y panel de controles en pestañas a la derecha.
 */
export function VisorPage() {
  const visor = useVisor();
  const { original, resultado, ajustes, dialogo } = visor;
  const [pestana, setPestana] = useState<IdPestana>("ajustes");
  const entrada = useRef<HTMLInputElement>(null);
  const lienzo = useRef<HTMLCanvasElement>(null);
  const sinImagen = !original;

  useEffect(() => {
    document.title = visor.nombreCargado ? `Visor de Imágenes — ${visor.nombreCargado}` : "Visor de Imágenes";
  }, [visor.nombreCargado]);

  // Dibuja el resultado en el lienzo cada vez que cambia
  useEffect(() => {
    if (!resultado || !lienzo.current) return;
    lienzo.current.width = resultado.ancho;
    lienzo.current.height = resultado.alto;
    lienzo.current.getContext("2d")!.putImageData(aImageData(resultado), 0, 0);
  }, [resultado]);

  // Atajos de teclado: Ctrl+O abrir, Ctrl+S guardar
  useEffect(() => {
    const alPulsar = (e: KeyboardEvent) => {
      if (!(e.ctrlKey || e.metaKey) || dialogo) return;
      const tecla = e.key.toLowerCase();
      if (tecla === "o") {
        e.preventDefault();
        entrada.current?.click();
      } else if (tecla === "s" && original) {
        e.preventDefault();
        visor.abrirDialogo({ tipo: "guardar" });
      }
    };
    window.addEventListener("keydown", alPulsar);
    return () => window.removeEventListener("keydown", alPulsar);
  }, [dialogo, original, visor]);

  const explorar = () => entrada.current?.click();
  const abrirHistograma = () => visor.abrirDialogo({ tipo: "histograma" });

  const menus = [
    {
      titulo: "Archivo",
      items: [
        { texto: "Abrir…", atajo: "Ctrl+O", accion: explorar },
        {
          texto: "Guardar como…",
          atajo: "Ctrl+S",
          accion: () => visor.abrirDialogo({ tipo: "guardar" }),
          deshabilitado: sinImagen,
        },
      ],
    },
    {
      titulo: "Editar",
      items: [
        { texto: "Deshacer", atajo: "Ctrl+Z", deshabilitado: true, fase2: true },
        { texto: "Restaurar", accion: visor.restaurar, deshabilitado: sinImagen },
      ],
    },
    {
      titulo: "Ver",
      items: [
        { texto: "Histograma", accion: abrirHistograma, deshabilitado: sinImagen },
        {
          texto: "Actualizar al mover",
          marcado: visor.autoActualizar,
          accion: () => visor.setAutoActualizar(!visor.autoActualizar),
        },
      ],
    },
    {
      titulo: "Ayuda",
      items: [{ texto: "Manual de usuario", accion: () => visor.abrirDialogo({ tipo: "ayuda" }) }],
    },
  ];

  const panel = {
    ajustes: <PanelAjustes visor={visor} deshabilitado={sinImagen} />,
    color: <PanelColor visor={visor} deshabilitado={sinImagen} />,
    zoom: <PanelZoom visor={visor} deshabilitado={sinImagen} />,
    fusion: <PanelFusion visor={visor} deshabilitado={sinImagen} />,
  }[pestana];

  return (
    <div className="visor-pagina">
      <Link to="/" className="volver">
        ← Proyectos
      </Link>

      <div className="sk-ventana visor-ventana">
        <Trazo relleno="var(--superficie)" estiloRelleno="solid" />

        {/* Barra de título */}
        <div className="sk-barra-titulo visor-titulo">
          <Trazo forma="rect" relleno="var(--relleno)" estiloRelleno="solid" margen={1} />
          <h1>Visor de Imágenes{visor.nombreCargado && ` — ${visor.nombreCargado}`}</h1>
          <span className="decoracion-so suave" aria-hidden="true">
            _ □ ×
          </span>
        </div>

        {/* Barra de menú */}
        <div className="visor-menu">
          <BarraMenu menus={menus} />
        </div>
        <Linea discontinua />

        {/* Fila de ruta */}
        <div className="visor-ruta">
          <label htmlFor="ruta-archivo">Archivo de imagen:</label>
          <Campo
            id="ruta-archivo"
            className="campo-ruta"
            readOnly
            value={visor.archivoElegido?.name ?? ""}
            placeholder="Ninguna imagen seleccionada"
          />
          <Boton onClick={explorar}>Explorar…</Boton>
          <Boton disabled={!visor.archivoElegido || visor.ocupado} onClick={() => void visor.cargar()}>
            {visor.ocupado ? "Cargando…" : "Cargar"}
          </Boton>
          <input
            ref={entrada}
            type="file"
            accept={EXTENSIONES_VALIDAS.join(",")}
            hidden
            onChange={(e) => {
              const archivo = e.target.files?.[0];
              if (archivo) visor.elegirArchivo(archivo);
              e.target.value = "";
            }}
          />
        </div>
        <Linea />

        {/* Cuerpo: imagen | panel */}
        <div className="visor-cuerpo">
          <div className="visor-area">
            <Trazo forma="lineaDerecha" margen={1} />
            {resultado ? (
              <div className="visor-lienzo">
                <canvas ref={lienzo} aria-label={`Imagen ${visor.nombreCargado} con los ajustes aplicados`} />
              </div>
            ) : (
              <button type="button" className="visor-vacio" onClick={explorar}>
                <Trazo discontinuo />
                <span className="icono-vacio" aria-hidden="true">
                  ⇪
                </span>
                <span className="texto-vacio">Explora y carga una imagen</span>
                <span className="suave">Formatos: JPG, PNG y BMP</span>
              </button>
            )}
          </div>

          <div className="visor-panel">
            <Pestanas pestanas={PESTANAS} activa={pestana} onElegir={setPestana} deshabilitadas={sinImagen} />
            <div className={`visor-panel-contenido ${sinImagen ? "inactivo" : ""}`} role="tabpanel">
              {panel}
            </div>
            <div className={`visor-acciones ${sinImagen ? "inactivo" : ""}`}>
              <Linea discontinua />
              <Casilla marcada={visor.autoActualizar} onCambio={visor.setAutoActualizar} deshabilitada={sinImagen}>
                Actualizar al mover
              </Casilla>
              <div className="botones-panel">
                <Boton onClick={visor.restaurar} disabled={sinImagen}>
                  Restaurar
                </Boton>
                <Boton principal onClick={visor.actualizar} disabled={sinImagen || visor.autoActualizar}>
                  Actualizar{visor.pendientes ? " •" : ""}
                </Boton>
              </div>
            </div>
          </div>
        </div>

        {/* Barra inferior y de estado */}
        <div className="visor-estado">
          <Trazo forma="rect" relleno="var(--relleno)" estiloRelleno="solid" margen={1} />
          <div className="botones-estado">
            <Boton onClick={abrirHistograma} disabled={sinImagen}>
              Histograma
            </Boton>
            <Boton
              onClick={() => visor.cambiar({ negativo: !ajustes.negativo })}
              disabled={sinImagen}
              aria-pressed={ajustes.negativo}
            >
              Negativo{ajustes.negativo ? " ✓" : ""}
            </Boton>
            <Boton onClick={() => visor.abrirDialogo({ tipo: "guardar" })} disabled={sinImagen}>
              Guardar…
            </Boton>
          </div>
          <span className="mensaje-estado" role="status">
            {original && (
              <span className="suave">
                {original.ancho} × {original.alto} px ·{" "}
              </span>
            )}
            {visor.mensaje}
          </span>
        </div>
      </div>

      {/* Pantallas 3 y 4 */}
      {dialogo?.tipo === "histograma" && resultado && (
        <DialogoHistograma imagen={resultado} nombre={visor.nombreCargado} onCerrar={visor.cerrarDialogo} />
      )}
      {dialogo?.tipo === "guardar" && (
        <DialogoGuardar
          nombreSugerido={visor.nombreSugerido}
          ocupado={visor.ocupado}
          onGuardar={(nombre, formato) => void visor.guardar(nombre, formato)}
          onCerrar={visor.cerrarDialogo}
        />
      )}
      {dialogo?.tipo === "error" && <DialogoError mensaje={dialogo.mensaje} onCerrar={visor.cerrarDialogo} />}
      {dialogo?.tipo === "tamano" && original && (
        <DialogoTamano
          segunda={dialogo.segunda}
          original={original}
          onCerrar={visor.cerrarDialogo}
          onAceptar={() => {
            visor.instalarSegunda(dialogo.segunda, dialogo.nombre);
            visor.cerrarDialogo();
          }}
        />
      )}
      {dialogo?.tipo === "ayuda" && <DialogoAyuda onCerrar={visor.cerrarDialogo} />}
    </div>
  );
}
