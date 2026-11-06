import { lazy, type ComponentType, type LazyExoticComponent } from "react";

/**
 * Registro de proyectos del curso. Para agregar uno nuevo:
 *   1. crea su carpeta en src/proyectos/<id>/ con una página que exporte un componente;
 *   2. agrega una entrada aquí. La ruta y la tarjeta del inicio se crean solas.
 */
export interface Proyecto {
  id: string; // también es la ruta: /<id>
  titulo: string;
  unidad: string;
  descripcion: string;
  temas: string[];
  pagina: LazyExoticComponent<ComponentType>;
}

export const PROYECTOS: Proyecto[] = [
  {
    id: "visor-imagenes",
    titulo: "Visor de Imágenes",
    unidad: "Unidad 4",
    descripcion:
      "Carga una imagen y ajusta brillo, contraste, rotación, canales RGB/CMY, zoom, binarización y fusión. Incluye histograma y guardado.",
    temas: ["procesamiento de imágenes", "transformaciones", "interfaces gráficas"],
    pagina: lazy(() => import("./visor-imagenes/VisorPage").then((m) => ({ default: m.VisorPage }))),
  },
];
