import { Casilla, Deslizador, Grupo } from "../../../sketch/componentes";
import type { TresCanales } from "../engine/color";
import type { Visor } from "../estado";

function cambiarUno(canales: TresCanales, i: number, valor: boolean): TresCanales {
  const copia = [...canales] as TresCanales;
  copia[i] = valor;
  return copia;
}

/** Pantalla 2B: canales RGB, tintas CMY y binarización. */
export function PanelColor({ visor, deshabilitado }: { visor: Visor; deshabilitado: boolean }) {
  const { ajustes, cambiar } = visor;
  return (
    <>
      <Grupo titulo="Canales RGB">
        <div className="sk-fila">
          {["Rojo", "Verde", "Azul"].map((nombre, i) => (
            <Casilla
              key={nombre}
              marcada={ajustes.canalesRGB[i]}
              onCambio={(v) => cambiar({ canalesRGB: cambiarUno(ajustes.canalesRGB, i, v) })}
              deshabilitada={deshabilitado}
            >
              {nombre}
            </Casilla>
          ))}
        </div>
      </Grupo>
      <Grupo titulo="Canales CMY">
        <div className="sk-fila">
          {["Cian", "Magenta", "Amarillo"].map((nombre, i) => (
            <Casilla
              key={nombre}
              marcada={ajustes.tintasCMY[i]}
              onCambio={(v) => cambiar({ tintasCMY: cambiarUno(ajustes.tintasCMY, i, v) })}
              deshabilitada={deshabilitado}
            >
              {nombre}
            </Casilla>
          ))}
        </div>
        <span className="suave nota">Sin ninguna o con las tres marcadas se ve la imagen completa.</span>
      </Grupo>
      <Grupo titulo="Binarizar">
        <Casilla
          marcada={ajustes.binarizar}
          onCambio={(binarizar) => cambiar({ binarizar })}
          deshabilitada={deshabilitado}
        >
          Convertir a blanco y negro
        </Casilla>
        <Deslizador
          id="umbral"
          etiqueta="Umbral"
          valor={ajustes.umbral}
          min={0}
          max={1}
          paso={0.01}
          decimales={2}
          etiquetaMin="0"
          etiquetaMax="1"
          onCambio={(umbral) => cambiar({ umbral })}
          deshabilitado={deshabilitado || !ajustes.binarizar}
        />
      </Grupo>
    </>
  );
}
