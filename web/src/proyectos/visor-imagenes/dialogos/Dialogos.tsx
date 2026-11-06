import { useState } from "react";
import { Boton, Campo, Dialogo, Opcion } from "../../../sketch/componentes";
import type { FormatoGuardado } from "../engine/archivos";
import type { Imagen } from "../engine/imagen";

/** Pantalla 4B: guardar con nombre y formato nuevos. */
export function DialogoGuardar({
  nombreSugerido,
  ocupado,
  onGuardar,
  onCerrar,
}: {
  nombreSugerido: string;
  ocupado: boolean;
  onGuardar: (nombre: string, formato: FormatoGuardado) => void;
  onCerrar: () => void;
}) {
  const [nombre, setNombre] = useState(nombreSugerido);
  const [formato, setFormato] = useState<FormatoGuardado>("png");
  return (
    <Dialogo
      titulo="Guardar como"
      onCerrar={onCerrar}
      pie={
        <>
          <Boton onClick={onCerrar}>Cancelar</Boton>
          <Boton principal disabled={ocupado} onClick={() => onGuardar(nombre, formato)}>
            {ocupado ? "Guardando…" : "Guardar"}
          </Boton>
        </>
      }
    >
      <div className="fila-formulario">
        <span>Carpeta:</span>
        <span className="suave">La elige el navegador (por lo general, Descargas).</span>
      </div>
      <label className="fila-formulario">
        <span>Nombre:</span>
        <Campo value={nombre} onChange={(e) => setNombre(e.target.value)} />
      </label>
      <div className="fila-formulario">
        <span>Formato:</span>
        <div className="sk-fila">
          {(["png", "jpg", "bmp"] as const).map((f) => (
            <Opcion key={f} nombre="formato" marcada={formato === f} onElegir={() => setFormato(f)}>
              {f.toUpperCase()}
            </Opcion>
          ))}
        </div>
      </div>
      <span className="suave nota">Se guarda en resolución completa con todos los ajustes aplicados.</span>
    </Dialogo>
  );
}

/** Pantalla 4C: error con qué falló y cómo resolverlo. */
export function DialogoError({ mensaje, onCerrar }: { mensaje: string; onCerrar: () => void }) {
  return (
    <Dialogo
      titulo="Error"
      onCerrar={onCerrar}
      pie={
        <Boton principal onClick={onCerrar}>
          Aceptar
        </Boton>
      }
    >
      <div className="aviso">
        <span className="icono-aviso" aria-hidden="true">
          ⚠
        </span>
        <p>{mensaje}</p>
      </div>
    </Dialogo>
  );
}

/** Pantalla 4D: la segunda imagen no mide lo mismo que la principal. */
export function DialogoTamano({
  segunda,
  original,
  onAceptar,
  onCerrar,
}: {
  segunda: Imagen;
  original: Imagen;
  onAceptar: () => void;
  onCerrar: () => void;
}) {
  return (
    <Dialogo
      titulo="Fusión: tamaños distintos"
      onCerrar={onCerrar}
      pie={
        <>
          <Boton onClick={onCerrar}>Cancelar</Boton>
          <Boton principal onClick={onAceptar}>
            Redimensionar y fusionar
          </Boton>
        </>
      }
    >
      <div className="aviso">
        <span className="icono-aviso info" aria-hidden="true">
          ⓘ
        </span>
        <p>
          La segunda imagen mide {segunda.ancho} × {segunda.alto} px y la principal {original.ancho} × {original.alto}{" "}
          px. Se redimensionará a {original.ancho} × {original.alto} px para fusionarlas.
        </p>
      </div>
    </Dialogo>
  );
}

/** Ayuda → Manual de usuario (resumen). */
export function DialogoAyuda({ onCerrar }: { onCerrar: () => void }) {
  return (
    <Dialogo
      titulo="Manual de usuario"
      onCerrar={onCerrar}
      ancho={560}
      pie={
        <Boton principal onClick={onCerrar}>
          Entendido
        </Boton>
      }
    >
      <ol className="manual">
        <li>
          <b>Explorar…</b> elige una imagen JPG, PNG o BMP; <b>Cargar</b> la muestra.
        </li>
        <li>
          <b>Ajustes:</b> brillo, contraste, rotación de 0° a 360° y filtro de zonas claras u oscuras.
        </li>
        <li>
          <b>Color:</b> activa o desactiva los canales RGB y las tintas CMY, o binariza con un umbral.
        </li>
        <li>
          <b>Zoom:</b> escribe la esquina (X, Y) y el factor; el recuadro azul muestra la región. Pulsa{" "}
          <b>Aplicar zoom</b>.
        </li>
        <li>
          <b>Fusión:</b> elige una segunda imagen y mueve la transparencia (0 = opaca, 1 = transparente).
        </li>
        <li>
          Con <b>Actualizar al mover</b> la imagen cambia con cada control; sin esa casilla, pulsa <b>Actualizar</b>.
          <b> Restaurar</b> vuelve a la imagen original.
        </li>
        <li>
          <b>Histograma</b> muestra la distribución de R, G, B y la luminosidad. <b>Guardar…</b> descarga la imagen
          editada.
        </li>
        <li>
          Atajos: <span className="mono">Ctrl+O</span> abrir, <span className="mono">Ctrl+S</span> guardar.
        </li>
      </ol>
    </Dialogo>
  );
}
