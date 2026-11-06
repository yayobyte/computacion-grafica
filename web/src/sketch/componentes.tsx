import {
  useEffect,
  useId,
  useRef,
  useState,
  type ButtonHTMLAttributes,
  type InputHTMLAttributes,
  type ReactNode,
} from "react";
import { tema } from "../theme/theme";
import { Trazo, type PropsTrazo } from "./Trazo";
import "./sketch.css";

/* Componentes con aspecto de boceto de Excalidraw. Debajo de cada dibujo hay
   un control HTML real, así que funcionan con teclado y lectores de pantalla. */

// --- Caja genérica -------------------------------------------------------------

export function Caja({
  children,
  className = "",
  trazo,
  ...propsTrazo
}: { children?: ReactNode; className?: string; trazo?: string } & PropsTrazo) {
  return (
    <div className={`sk-caja ${className}`}>
      <Trazo trazo={trazo} {...propsTrazo} />
      {children}
    </div>
  );
}

export function Linea({ vertical = false, discontinua = false }: { vertical?: boolean; discontinua?: boolean }) {
  return (
    <div className={vertical ? "sk-linea-v" : "sk-linea"} aria-hidden="true">
      <Trazo forma={vertical ? "lineaDerecha" : "lineaInferior"} discontinuo={discontinua} margen={1} />
    </div>
  );
}

// --- Botón ---------------------------------------------------------------------

export function Boton({
  principal = false,
  children,
  className = "",
  ...props
}: { principal?: boolean } & ButtonHTMLAttributes<HTMLButtonElement>) {
  return (
    <button type="button" className={`sk-boton ${principal ? "principal" : ""} ${className}`} {...props}>
      <Trazo
        relleno={principal ? "var(--relleno-fuerte)" : "var(--relleno)"}
        estiloRelleno={principal ? "solid" : "hachure"}
        grosor={principal ? tema.trazo.strokeWidthPrincipal : tema.trazo.strokeWidth}
      />
      <span className="sk-boton-texto">{children}</span>
    </button>
  );
}

// --- Campos de texto y número ----------------------------------------------------

export function Campo({ className = "", ...props }: InputHTMLAttributes<HTMLInputElement>) {
  return (
    <span className={`sk-campo ${className} ${props.disabled ? "inactivo" : ""}`}>
      <Trazo relleno="var(--superficie)" estiloRelleno="solid" />
      <input {...props} />
    </span>
  );
}

// --- Deslizador ------------------------------------------------------------------

interface PropsDeslizador {
  id: string;
  etiqueta: string;
  valor: number;
  min: number;
  max: number;
  paso: number;
  onCambio: (valor: number) => void;
  etiquetaMin?: string;
  etiquetaMax?: string;
  sufijo?: string;
  decimales?: number;
  deshabilitado?: boolean;
}

/** Fila del boceto: etiqueta · deslizador · caja numérica. */
export function Deslizador({
  id,
  etiqueta,
  valor,
  min,
  max,
  paso,
  onCambio,
  etiquetaMin,
  etiquetaMax,
  sufijo = "",
  decimales = 0,
  deshabilitado = false,
}: PropsDeslizador) {
  const porcentaje = ((valor - min) / (max - min)) * 100;
  const [texto, setTexto] = useState(valor.toFixed(decimales));
  const [enFoco, setEnFoco] = useState(false);

  useEffect(() => setTexto(valor.toFixed(decimales)), [valor, decimales]);

  const confirmarTexto = () => {
    setEnFoco(false);
    const numero = Number(texto.replace(",", "."));
    if (Number.isFinite(numero)) {
      onCambio(Math.min(max, Math.max(min, numero)));
    } else {
      setTexto(valor.toFixed(decimales));
    }
  };

  return (
    <div className={`sk-control ${deshabilitado ? "inactivo" : ""}`}>
      <label htmlFor={id}>{etiqueta}</label>
      <div className="sk-deslizador">
        <div className="sk-pista">
          <Trazo forma="lineaInferior" margen={1} />
        </div>
        <div className="sk-perilla" style={{ left: `calc(${porcentaje}% - 9px)` }}>
          <Trazo relleno="var(--superficie)" estiloRelleno="solid" margen={1} />
        </div>
        <input
          id={id}
          type="range"
          min={min}
          max={max}
          step={paso}
          value={valor}
          disabled={deshabilitado}
          onChange={(e) => onCambio(Number(e.target.value))}
        />
        {etiquetaMin && <span className="sk-extremo izq">{etiquetaMin}</span>}
        {etiquetaMax && <span className="sk-extremo der">{etiquetaMax}</span>}
      </div>
      <Campo
        className="sk-numero"
        aria-label={`${etiqueta} (valor)`}
        value={enFoco ? texto : texto + sufijo}
        disabled={deshabilitado}
        inputMode="decimal"
        onFocus={() => {
          setEnFoco(true);
          setTexto(valor.toFixed(decimales));
        }}
        onChange={(e) => setTexto(e.target.value)}
        onBlur={confirmarTexto}
        onKeyDown={(e) => e.key === "Enter" && confirmarTexto()}
      />
    </div>
  );
}

// --- Casilla y opción --------------------------------------------------------------

export function Casilla({
  marcada,
  onCambio,
  children,
  deshabilitada = false,
}: {
  marcada: boolean;
  onCambio: (marcada: boolean) => void;
  children: ReactNode;
  deshabilitada?: boolean;
}) {
  return (
    <label className={`sk-casilla ${deshabilitada ? "inactivo" : ""}`}>
      <input
        type="checkbox"
        className="sk-oculto"
        checked={marcada}
        disabled={deshabilitada}
        onChange={(e) => onCambio(e.target.checked)}
      />
      <span className="sk-marco">
        <Trazo relleno="var(--superficie)" estiloRelleno="solid" margen={1} />
        {marcada && (
          <span className="sk-tilde">
            <Trazo forma="marca" trazo="var(--acento)" grosor={2.6} margen={0} />
          </span>
        )}
      </span>
      <span>{children}</span>
    </label>
  );
}

export function Opcion({
  nombre,
  marcada,
  onElegir,
  children,
  deshabilitada = false,
}: {
  nombre: string;
  marcada: boolean;
  onElegir: () => void;
  children: ReactNode;
  deshabilitada?: boolean;
}) {
  return (
    <label className={`sk-casilla ${deshabilitada ? "inactivo" : ""}`}>
      <input
        type="radio"
        name={nombre}
        className="sk-oculto"
        checked={marcada}
        disabled={deshabilitada}
        onChange={onElegir}
      />
      <span className="sk-marco redondo">
        <Trazo forma="elipse" relleno="var(--superficie)" estiloRelleno="solid" margen={1} />
        {marcada && (
          <span className="sk-punto">
            <Trazo forma="elipse" trazo="var(--acento)" relleno="var(--acento)" estiloRelleno="solid" margen={0} />
          </span>
        )}
      </span>
      <span>{children}</span>
    </label>
  );
}

// --- Grupo con título (línea punteada del boceto) ------------------------------------

export function Grupo({ titulo, children }: { titulo: string; children: ReactNode }) {
  return (
    <fieldset className="sk-grupo">
      <Trazo discontinuo margen={2} />
      <legend>{titulo}</legend>
      <div className="sk-grupo-contenido">{children}</div>
    </fieldset>
  );
}

// --- Pestañas ---------------------------------------------------------------------------

export function Pestanas<T extends string>({
  pestanas,
  activa,
  onElegir,
  deshabilitadas = false,
}: {
  pestanas: readonly { id: T; texto: string }[];
  activa: T;
  onElegir: (id: T) => void;
  deshabilitadas?: boolean;
}) {
  return (
    <div className="sk-pestanas" role="tablist">
      {pestanas.map((p) => {
        const esActiva = p.id === activa;
        return (
          <button
            key={p.id}
            type="button"
            role="tab"
            aria-selected={esActiva}
            disabled={deshabilitadas}
            className={`sk-pestana ${esActiva ? "activa" : ""}`}
            onClick={() => onElegir(p.id)}
          >
            <Trazo
              relleno={esActiva ? "var(--superficie)" : "var(--relleno)"}
              estiloRelleno={esActiva ? "solid" : "hachure"}
              grosor={esActiva ? tema.trazo.strokeWidthPrincipal : tema.trazo.strokeWidth}
              margen={1}
            />
            <span className="sk-boton-texto">{p.texto}</span>
          </button>
        );
      })}
    </div>
  );
}

// --- Etiqueta "fase 2" ----------------------------------------------------------------

export function Fase2() {
  return <span className="sk-fase2">fase 2</span>;
}

// --- Diálogo modal (pantallas 3 y 4) ------------------------------------------------------

export function Dialogo({
  titulo,
  children,
  pie,
  onCerrar,
  ancho = 460,
}: {
  titulo: string;
  children: ReactNode;
  pie?: ReactNode;
  onCerrar: () => void;
  ancho?: number;
}) {
  const idTitulo = useId();
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const anterior = document.activeElement as HTMLElement | null;
    ref.current?.querySelector<HTMLElement>("button.principal, input, button")?.focus();
    const alPulsar = (e: KeyboardEvent) => e.key === "Escape" && onCerrar();
    window.addEventListener("keydown", alPulsar);
    return () => {
      window.removeEventListener("keydown", alPulsar);
      anterior?.focus();
    };
  }, [onCerrar]);

  return (
    <div className="sk-fondo-modal" onMouseDown={(e) => e.target === e.currentTarget && onCerrar()}>
      <div
        ref={ref}
        className="sk-ventana sk-dialogo"
        role="dialog"
        aria-modal="true"
        aria-labelledby={idTitulo}
        style={{ width: `min(${ancho}px, 100%)` }}
      >
        <Trazo relleno="var(--superficie)" estiloRelleno="solid" />
        <div className="sk-barra-titulo">
          <Trazo forma="lineaInferior" margen={1} />
          <span id={idTitulo}>{titulo}</span>
          <button type="button" className="sk-cerrar" aria-label="Cerrar" onClick={onCerrar}>
            ×
          </button>
        </div>
        <div className="sk-dialogo-cuerpo">{children}</div>
        {pie && (
          <div className="sk-dialogo-pie">
            <Linea discontinua />
            <div className="sk-dialogo-botones">{pie}</div>
          </div>
        )}
      </div>
    </div>
  );
}

// --- Barra de menú ------------------------------------------------------------------------

export interface ItemMenu {
  texto: string;
  atajo?: string;
  accion?: () => void;
  deshabilitado?: boolean;
  marcado?: boolean;
  fase2?: boolean;
}

export function BarraMenu({ menus }: { menus: { titulo: string; items: ItemMenu[] }[] }) {
  const [abierto, setAbierto] = useState<number | null>(null);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (abierto === null) return;
    const cerrar = (e: MouseEvent | KeyboardEvent) => {
      if (e instanceof KeyboardEvent ? e.key === "Escape" : !ref.current?.contains(e.target as Node)) {
        setAbierto(null);
      }
    };
    window.addEventListener("mousedown", cerrar);
    window.addEventListener("keydown", cerrar);
    return () => {
      window.removeEventListener("mousedown", cerrar);
      window.removeEventListener("keydown", cerrar);
    };
  }, [abierto]);

  return (
    <div className="sk-barra-menu" ref={ref} role="menubar">
      {menus.map((menu, i) => (
        <div key={menu.titulo} className="sk-menu">
          <button
            type="button"
            role="menuitem"
            aria-haspopup="true"
            aria-expanded={abierto === i}
            className={`sk-menu-titulo ${abierto === i ? "abierto" : ""}`}
            onClick={() => setAbierto(abierto === i ? null : i)}
            onMouseEnter={() => abierto !== null && setAbierto(i)}
          >
            {menu.titulo}
          </button>
          {abierto === i && (
            <div className="sk-desplegable" role="menu">
              <Trazo relleno="var(--superficie)" estiloRelleno="solid" />
              {menu.items.map((item) => (
                <button
                  key={item.texto}
                  type="button"
                  role="menuitem"
                  disabled={item.deshabilitado}
                  className="sk-menu-item"
                  onClick={() => {
                    setAbierto(null);
                    item.accion?.();
                  }}
                >
                  <span className="sk-menu-marca">{item.marcado ? "✓" : ""}</span>
                  <span>{item.texto}</span>
                  {item.fase2 && <Fase2 />}
                  <span className="sk-menu-atajo suave">{item.atajo}</span>
                </button>
              ))}
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
