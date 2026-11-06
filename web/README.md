# Computación Gráfica · UTP — proyectos web

Aplicación React + TypeScript + Vite con los proyectos del curso. El inicio lista los proyectos y cada uno tiene su propia ruta.

| Proyecto | Ruta | Plan |
| --- | --- | --- |
| Visor de Imágenes (Unidad 4) | `/visor-imagenes` | [`unidad-4/PLAN_visor_imagenes.md`](../unidad-4/PLAN_visor_imagenes.md) |

## Comandos

```bash
npm install
npm run dev       # http://localhost:5173
npm run build     # tipos + compilación en dist/
npm run preview   # prueba de la versión compilada
```

## Despliegue en Vercel

Root Directory `web`, preset Vite, build `npm run build`, salida `dist`. `vercel.json` hace que las rutas directas (por ejemplo `/visor-imagenes`) carguen la aplicación.

## Tema y estilo

- Colores, fuentes, espaciados y el trazo a mano están en [`src/theme/theme.ts`](./src/theme/theme.ts).
- `trazo.roughness` controla el descuido: 0 Arquitecto, 1 Artista, 2 Caricaturista (el actual).
- Los componentes de boceto están en [`src/sketch/`](./src/sketch/).

## Agregar un proyecto

1. Crea `src/proyectos/<id>/` con una página que exporte un componente.
2. Agrega su entrada en [`src/proyectos/registro.ts`](./src/proyectos/registro.ts).

## Créditos

- Trazo a mano: [rough.js](https://github.com/rough-stuff/rough) (MIT).
- Fuente: Excalifont, de [Excalidraw](https://github.com/excalidraw/excalidraw), con licencia SIL Open Font License 1.1. Se incluye solo el subconjunto latino (`public/fonts/`).
- Herramientas / asistencia de IA: Claude Opus 5.5 (Anthropic).
