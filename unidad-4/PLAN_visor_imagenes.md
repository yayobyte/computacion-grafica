# Plan del proyecto: Visor de Imágenes

Proyecto final de la Unidad 4 de Computación Gráfica (UTP). Este documento reúne los requisitos del enunciado, el diseño del boceto y la arquitectura de la aplicación, para usarlo como guía durante el desarrollo y la sustentación.

| Recurso | Ubicación |
| --- | --- |
| Enunciado | [`Proyecto Visor de Imagenes (2025)-2.pdf`](./Proyecto%20Visor%20de%20Imagenes%20(2025)-2.pdf) |
| Boceto anotado (HTML) | [`boceto_visor_imagenes.html`](./boceto_visor_imagenes.html) |
| Boceto editable (Excalidraw) | [`boceto_visor_imagenes.excalidraw`](./boceto_visor_imagenes.excalidraw) |
| Guía de wireframes | [`wireframe.txt`](./wireframe.txt) |
| Código | [`../web/`](../web/) (React + TypeScript + Vite) |

---

## 1. Decisión de plataforma

El enunciado pide una aplicación de escritorio en **Python con Tkinter o Qt**. Este proyecto se desarrolla como **aplicación web** (React + TypeScript + Vite, desplegada en Vercel), por decisión del estudiante.

> **Riesgo:** el "Producto a entregar" del enunciado dice "Aplicación funcional desarrollada en Python con interfaz gráfica (Tkinter o Qt)". Hay que **confirmar con el profesor** que una aplicación web es aceptable antes de la entrega. Si no lo es, la arquitectura de este documento se puede trasladar a Tkinter: el motor (`engine/`) ya es un puerto directo de `procesamiento_imagenes.py` y `taller9_transformaciones.py`, y la interfaz sigue el mismo boceto.

Equivalencias con lo que pide el enunciado:

| Enunciado | En la versión web |
| --- | --- |
| Tkinter / Qt | React (componentes) |
| `tkinter.Frame` para organizar | Componentes y rejillas CSS |
| NumPy | `Float32Array` con los mismos cálculos, píxel a píxel |
| Matplotlib para el histograma | SVG dibujado con rough.js (exportable a PNG) |
| Cuadro de diálogo de archivos | Selector de archivos del navegador |
| Guardar en otra ubicación | Descarga del navegador (el navegador elige la carpeta) |

---

## 2. Requisitos del enunciado

### 2.1 Interfaz de usuario

- [x] Ventana principal con título "Visor de Imágenes".
- [x] Campo de texto con la ruta del archivo cargado (en web, el nombre del archivo: el navegador no expone la ruta completa).
- [x] Botón **Explorar**: abre el selector de archivos.
- [x] Botón **Cargar**: carga la imagen seleccionada y la muestra.
- [x] Botón **Actualizar**: aplica los ajustes seleccionados.
- [x] Botón **Guardar**: guarda la imagen modificada con un nombre nuevo.
- [x] Botón **Fusionar imágenes**: segunda imagen con transparencia ajustable.
- [x] Deslizadores de **brillo**, **contraste**, **rotación (0°–360°)** y **transparencia de fusión (0 %–100 %)**.
- [x] Filtro de **zonas claras y zonas oscuras**.
- [x] Activar o desactivar los canales **RGB**.
- [x] Activar o desactivar los canales **CMY**.
- [x] **Zoom** desde un punto inicial (X, Y) con factor ajustable.
- [x] **Binarizar** con umbral ajustable.
- [x] **Histograma** con la distribución de cada canal.
- [x] **Negativo** de la imagen.

### 2.2 Funcionalidad

- [x] Cargar imágenes **JPG, PNG y BMP**; rechazar otros formatos con un mensaje.
- [x] Brillo y contraste con las fórmulas de clase.
- [x] Rotación de 0° a 360°.
- [x] Zoom desde (X, Y) con factor de escala.
- [x] Binarización con umbral.
- [x] Fusión: segunda imagen, transparencia de **0 (opaca) a 1 (transparente)**.
- [x] Histograma de **R, G, B y luminosidad**.
- [x] **Actualización dinámica** de la vista al mover los controles.

### 2.3 Detalles de implementación

- [x] Separar la lógica de la interfaz (`engine/` no importa React).
- [x] Código comentado y documentado.
- [x] Probar con distintos tipos y tamaños de imagen (ver sección 9).

### 2.4 Funcionalidades avanzadas (opcionales)

| Funcionalidad | Estado |
| --- | --- |
| Restaurar (volver a los valores por defecto) | Hecho: botón **Restaurar** y menú Editar |
| Deshacer cambios | Fase 2 (en el menú, deshabilitado) |
| Rotación libre con ratón o teclado | Fase 2 |
| Zoom seleccionando con el ratón | Fase 2 (casilla deshabilitada en la pestaña Zoom) |
| Modos de fusión (multiplicar, suma, diferencia) | Fase 2 (selector "Modo" deshabilitado) |

### 2.5 Rúbrica

| Criterio | Peso | Dónde se cubre |
| --- | --- | --- |
| Interfaz gráfica funcional | 20 % | Boceto opción B, estilo Excalidraw, pantallas 1–4 |
| Transformaciones correctas | 20 % | `engine/ajustes.ts`, `color.ts`, `geometria.ts` |
| Fusión de imágenes | 15 % | `engine/fusion.ts`, pestaña Fusión, diálogo 4D |
| Visualización gráfica (histogramas) | 15 % | `engine/histograma.ts`, `DialogoHistograma.tsx` |
| Documentación del código | 10 % | Comentarios en el código, este plan, manual en Ayuda |
| Presentación y entrega | 20 % | Boceto, tabla de trazabilidad, despliegue en Vercel |

---

## 3. Pantallas (boceto, opción B)

Imagen a la izquierda (≈ 2/3 del ancho) y panel de controles en pestañas a la derecha. Los números entre paréntesis son las anotaciones del boceto.

| Pantalla | Contenido | Componente |
| --- | --- | --- |
| **1** Sin imagen | Título (1), menú (2), ruta + Explorar + Cargar (3), estado vacío (4), barra de estado (5); panel deshabilitado | `VisorPage.tsx` |
| **2A** Ajustes | Área de imagen (6), pestañas (7), brillo/contraste/rotación (8), zonas (9), Actualizar + "Actualizar al mover" (10), barra inferior (11) | `paneles/PanelAjustes.tsx` |
| **2B** Color | Casillas RGB y CMY (12), binarizar + umbral (13) | `paneles/PanelColor.tsx` |
| **2C** Zoom | X, Y con máximo visible (14), factor y miniatura con la región (15) | `paneles/PanelZoom.tsx` |
| **2D** Fusión | Segunda imagen + miniatura (16), transparencia 0–1 y modo "fase 2" (17) | `paneles/PanelFusion.tsx` |
| **3** Histograma | Separados / superpuestos (18), R, G, B y luminosidad con ejes (19) | `dialogos/DialogoHistograma.tsx` |
| **4A** Abrir | Selector de archivos con filtro JPG/PNG/BMP (20) | selector del navegador |
| **4B** Guardar como | Nombre y formato PNG/JPG/BMP (21) | `dialogos/Dialogos.tsx` |
| **4C** Error | Qué falló y cómo resolverlo (22) | `dialogos/Dialogos.tsx` |
| **4D** Tamaños distintos | Aviso antes de redimensionar la segunda imagen (23) | `dialogos/Dialogos.tsx` |

Menú: **Archivo** (Abrir Ctrl+O, Guardar como Ctrl+S) · **Editar** (Deshacer fase 2, Restaurar) · **Ver** (Histograma, Actualizar al mover) · **Ayuda** (Manual de usuario).

### Mapa de navegación

```
Pantalla 1 ──Explorar──▶ 4A Abrir ──Cargar──▶ Pantallas 2A–2D ──Actualizar──▶ 4B Guardar ──▶ "Guardado ✓"
                 │                                  │
                 └── formato no válido ──▶ 4C Error  ├──▶ 3 Histograma
                                                    ├──▶ 4D Aviso de tamaño (desde Fusión)
                                                    └──▶ Restaurar
```

---

## 4. Sistema de diseño (estilo Excalidraw)

- **Trazo a mano** con [rough.js](https://roughjs.com/), la misma librería que usa Excalidraw, con **descuido 2 = "Caricaturista"** (la tercera opción de Excalidraw).
- **Fuente manuscrita:** Excalifont (la fuente de Excalidraw, licencia OFL), con Kalam de Google Fonts como respaldo.
- **Paleta:** papel cálido, tinta casi negra, acento azul de Excalidraw (`#1971c2`), rellenos con rayado (*hachure*).
- **Modo oscuro** automático según el sistema operativo.

Todo sale de un solo archivo, [`web/src/theme/theme.ts`](../web/src/theme/theme.ts):

| Token | Para qué sirve |
| --- | --- |
| `colores.claro` / `colores.oscuro` | Paleta; se convierte en variables CSS (`--papel`, `--tinta`, `--acento`…) |
| `fuentes` | Fuente manuscrita y monoespaciada |
| `trazo.roughness` | Descuido del trazo: 0 Arquitecto, 1 Artista, **2 Caricaturista** |
| `trazo.bowing`, `strokeWidth`, `fillStyle`, `hachureGap` | Curvatura, grosor y relleno de los dibujos |
| `trazoDatos` | Trazo más sereno para las gráficas |
| `ventana.columnas` | Proporción imagen : panel |
| `ventana.ladoMaximoVistaPrevia` | Tamaño máximo de la vista previa (rendimiento) |

**Componentes de boceto** ([`web/src/sketch/`](../web/src/sketch/)): `Trazo` (dibujo de rough.js que se ajusta a su contenedor), `Boton`, `Campo`, `Deslizador`, `Casilla`, `Opcion`, `Grupo`, `Pestanas`, `Dialogo`, `BarraMenu`, `Linea`, `Fase2`. Cada uno envuelve un control HTML real, así que funcionan con teclado y lectores de pantalla.

---

## 5. Arquitectura

```
tema (theme.ts) ─▶ componentes de boceto (sketch/) ─▶ pantallas (VisorPage, paneles, diálogos)
                                                             │
                                                             ▼
                                         estado (estado.ts: useVisor)
                                                             │
                                                             ▼
                                motor puro (engine/: sin React, sin DOM salvo archivos.ts)
```

| Capa | Responsabilidad | Regla |
| --- | --- | --- |
| `engine/` | Cálculos sobre la imagen | Funciones puras: reciben una `Imagen` y retornan otra |
| `estado.ts` | Imagen original, vista previa, segunda imagen, ajustes, diálogos, mensajes | Único lugar que llama al motor |
| `paneles/`, `dialogos/`, `VisorPage.tsx` | Interfaz | Solo leen el estado y llaman acciones |
| `sketch/`, `theme/` | Apariencia | No saben nada de imágenes |

### 5.1 Representación de la imagen

Igual que en los talleres de Python con NumPy normalizado: cada píxel guarda R, G y B como reales en **[0, 1]**, en un `Float32Array` entrelazado. El píxel (fila, columna) empieza en `(fila · ancho + columna) · 3`.

### 5.2 Vista previa y resolución completa

Para que los deslizadores respondan con fluidez, la vista previa se procesa con la imagen reducida a 1600 px en su lado mayor. Al **guardar**, el mismo pipeline se ejecuta sobre la imagen original en resolución completa.

---

## 6. Motor de procesamiento

Fórmulas tomadas de los talleres 8 y 9 y de los apuntes de la unidad 3. Notación: `I` es el valor de un canal en [0, 1].

| Operación | Fórmula | Archivo | Origen |
| --- | --- | --- | --- |
| Brillo | `clip(I + b)`, b = brillo/100 ∈ [−1, 1] | `ajustes.ts` | `ajustarBrillo` (Taller 9) |
| Contraste | `clip((I − 0.5)·k + 0.5)`, k ∈ [0.2, 3] | `ajustes.ts` | `ajustarContraste` (Taller 9) |
| Zonas oscuras | `log₁₀(1 + I) / log₁₀(2)` | `ajustes.ts` | Apuntes 3.6 (forma normalizada) |
| Zonas claras | `(eᴵ − 1) / (e − 1)` | `ajustes.ts` | Apuntes 3.6 (forma normalizada) |
| Canales RGB | canal desactivado → 0 | `color.ts` | `extraerCapa` (Taller 8) |
| Tintas CMY | R = R si cian activa, si no 1; G con magenta; B con amarillo | `color.ts` | `capaTinta` (Taller 8) |
| Negativo | `1 − I` | `color.ts` | `invertirColores` (Taller 8) |
| Binarizar | `0.299R + 0.587G + 0.114B ≥ umbral` | `color.ts` | `binarizar` (Taller 9) |
| Zoom | región de (X, Y) de tamaño ancho/f × alto/f, ampliada por vecino más cercano | `geometria.ts` | `ampliarRegion` / `np.kron` (Taller 9) |
| Rotación | mapeo inverso con lienzo ampliado | `geometria.ts` | `rotarImagen` (Taller 9) |
| Fusión | `(1 − t)·B + t·A`, t = transparencia de la segunda | `fusion.ts` | `fusionarConFactor` (Taller 8) |
| Histograma | conteo de niveles 0–255 por canal y luminosidad | `histograma.ts` | `calcularHistograma` (Taller 9) |
| Redimensionar | interpolación bilineal | `geometria.ts` | — |

**Decisiones:**

- **Tintas CMY.** Cada tinta marcada aplica su capa y las capas marcadas se multiplican, como filtros superpuestos. Con las tres marcadas, o con ninguna, se ve la imagen completa.
- **Fusión.** El enunciado define la transparencia de la **segunda** imagen: 0 = opaca (solo se ve la segunda), 1 = transparente (solo la principal). Si las imágenes no miden lo mismo, el diálogo 4D avisa y la segunda se redimensiona al tamaño de la principal.
- **Zoom antes de la rotación**, para que (X, Y) siempre se refieran a los píxeles de la imagen original. Si la región se saldría de la imagen, se desplaza hacia adentro.
- **Rotación.** El código de la Diapositiva 30 deja la imagen negra entre 90° y 180°; se usa el mapeo inverso centrado del Taller 9, que funciona en cualquier ángulo.

### 6.1 Orden del pipeline (`pipeline.ts`)

```
fusión → brillo → contraste → zonas → canales RGB → tintas CMY → negativo → binarizar → zoom → rotación
```

---

## 7. Estructura de carpetas

```
web/
├── index.html · vite.config.ts · tsconfig.json · package.json
├── vercel.json                     # reescritura SPA → /index.html
├── public/fonts/Excalifont-Regular.woff2
└── src/
    ├── main.tsx · App.tsx          # rutas: "/" y una por proyecto
    ├── theme/                      # theme.ts (tokens), ThemeProvider.tsx, global.css
    ├── sketch/                     # Trazo.tsx, componentes.tsx, sketch.css
    ├── home/                       # HomePage.tsx: menú de proyectos
    └── proyectos/
        ├── registro.ts             # lista de proyectos del curso
        └── visor-imagenes/
            ├── VisorPage.tsx       # pantallas 1 y 2
            ├── estado.ts           # useVisor()
            ├── visor.css
            ├── engine/             # imagen, ajustes, color, geometria, fusion,
            │                       # histograma, pipeline, archivos (cargar, guardar, BMP)
            ├── paneles/            # PanelAjustes, PanelColor, PanelZoom, PanelFusion
            └── dialogos/           # DialogoHistograma, Dialogos (guardar, error, tamaño, ayuda)
```

### 7.1 Agregar los próximos proyectos

1. Crear `src/proyectos/<id>/` con una página que exporte un componente.
2. Agregar una entrada en `src/proyectos/registro.ts` (id, título, unidad, descripción, temas y página).
3. La ruta `/<id>` y la tarjeta del inicio se crean solas. Reutilizar `sketch/` y `theme/` para mantener el estilo.

---

## 8. Hitos

| # | Hito | Estado |
| --- | --- | --- |
| 1 | Boceto (HTML + Excalidraw) con trazabilidad | Hecho |
| 2 | Proyecto Vite + tema + componentes de boceto + inicio | Hecho |
| 3 | Motor de procesamiento con las fórmulas de clase | Hecho |
| 4 | Pantallas 1, 2A–2D, 3 y 4B–4D funcionando | Hecho |
| 5 | Despliegue en Vercel | Pendiente (pasos en la sección 10) |
| 6 | Manual de usuario y presentación | Manual breve en Ayuda; falta la presentación |
| 7 | Funcionalidades de fase 2 | Opcional |

---

## 9. Verificación

**Motor** (comprobaciones con imágenes aleatorias): negativo dos veces = original; brillo +2 satura en 1; capas RGB sumadas = original; tintas CMY multiplicadas = original; rotar 0° y 360° = original; rotar 90° intercambia ancho y alto; rotar 120° conserva la imagen; fusión con t = 1 da la principal y con t = 0 la segunda; el histograma suma el total de píxeles.

**Aplicación** (en Chrome, de punta a punta):

| Caso | Resultado esperado |
| --- | --- |
| Abrir un `.gif` | Diálogo 4C "El visor acepta JPG, PNG y BMP" |
| Cargar JPG, PNG y BMP | Se muestran con su tamaño real en la barra de estado |
| Mover brillo y contraste | La vista cambia al instante |
| Desmarcar "Actualizar al mover" | La vista espera hasta pulsar Actualizar |
| Restaurar | Vuelve a la imagen original |
| Binarizar | Solo píxeles blancos y negros |
| Rotar 120° | El lienzo se amplía y la imagen no se corta |
| Zoom (300, 500) × 4 | Se amplía esa región |
| Fusionar con una imagen de otro tamaño | Diálogo 4D con los dos tamaños |
| Transparencia 1 | Solo se ve la imagen principal |
| Histograma separados / superpuestos | 4 gráficas o una con las 4 curvas; "Guardar gráfica" descarga un PNG |
| Guardar PNG, JPG y BMP | Se descargan y se pueden volver a abrir |
| Pantalla de 400 px | El panel pasa debajo de la imagen, sin desplazamiento horizontal |

---

## 10. Ejecución y despliegue

```bash
cd web
npm install
npm run dev        # desarrollo en http://localhost:5173
npm run build      # verificación de tipos + compilación en dist/
npm run preview    # prueba local de la versión compilada
```

**Vercel:** importar el repositorio y configurar:

| Ajuste | Valor |
| --- | --- |
| Root Directory | `web` |
| Framework Preset | Vite |
| Build Command | `npm run build` |
| Output Directory | `dist` |

`vercel.json` redirige todas las rutas a `index.html`, así que un enlace directo a `/visor-imagenes` también funciona.
