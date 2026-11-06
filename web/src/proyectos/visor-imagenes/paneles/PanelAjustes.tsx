import { Deslizador, Grupo, Opcion } from "../../../sketch/componentes";
import type { Zonas } from "../engine/ajustes";
import type { Visor } from "../estado";

const ZONAS: { id: Zonas; texto: string }[] = [
  { id: "ninguno", texto: "Ninguno" },
  { id: "claras", texto: "Zonas claras" },
  { id: "oscuras", texto: "Zonas oscuras" },
];

/** Pantalla 2A: brillo, contraste, rotación y filtro de zonas. */
export function PanelAjustes({ visor, deshabilitado }: { visor: Visor; deshabilitado: boolean }) {
  const { ajustes, cambiar } = visor;
  return (
    <>
      <Deslizador
        id="brillo"
        etiqueta="Brillo"
        valor={ajustes.brillo}
        min={-100}
        max={100}
        paso={1}
        etiquetaMin="-100"
        etiquetaMax="100"
        onCambio={(brillo) => cambiar({ brillo })}
        deshabilitado={deshabilitado}
      />
      <Deslizador
        id="contraste"
        etiqueta="Contraste"
        valor={ajustes.contraste}
        min={0.2}
        max={3}
        paso={0.05}
        decimales={2}
        etiquetaMin="0.2"
        etiquetaMax="3.0"
        onCambio={(contraste) => cambiar({ contraste })}
        deshabilitado={deshabilitado}
      />
      <Deslizador
        id="rotacion"
        etiqueta="Rotación"
        valor={ajustes.rotacion}
        min={0}
        max={360}
        paso={1}
        sufijo="°"
        etiquetaMin="0°"
        etiquetaMax="360°"
        onCambio={(rotacion) => cambiar({ rotacion })}
        deshabilitado={deshabilitado}
      />
      <Grupo titulo="Filtro de zonas">
        <div className="sk-fila">
          {ZONAS.map((z) => (
            <Opcion
              key={z.id}
              nombre="zonas"
              marcada={ajustes.zonas === z.id}
              onElegir={() => cambiar({ zonas: z.id })}
              deshabilitada={deshabilitado}
            >
              {z.texto}
            </Opcion>
          ))}
        </div>
      </Grupo>
    </>
  );
}
