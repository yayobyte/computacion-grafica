# Taller 1 — Física Computacional en Python (de Caída Libre a Proyectiles)

Ruta sugerida: [← Unidad 1](../) | [Inicio](../../) | [Taller 2 →](../taller2-control-listas-funciones/)

## Objetivo

Aplicar variables, expresiones, entrada/salida, decisiones y funciones a problemas de caída libre, cinemática, vectores y movimiento de proyectiles. Todo se integra en un menú interactivo.

- **Valor:** 0,0 a 5,0 · trabajo individual · ~4 horas.
- **Evaluación (Moodle):** funcionamiento 40 %, corrección conceptual 25 %, organización y documentación 20 %, pruebas y verificación 15 %.

## Conceptos clave

| Opción | Tema | Fórmula |
| :---: | --- | --- |
| 1 | Caída libre | $t = \sqrt{2h/g}$ |
| 2 | Conversión de velocidad | $1\ \text{km/h} = \tfrac{1}{3.6}\ \text{m/s}$ |
| 3 | Desplazamiento MRUA | $s = ut + \tfrac{1}{2}at^2$ |
| 4 | Suma de vectores | $\vec{A} + \vec{B} = [A_x + B_x,\ A_y + B_y]$ |
| 5 | Producto escalar y ángulo | $\cos\theta = \dfrac{\vec{A} \cdot \vec{B}}{\lvert\vec{A}\rvert\,\lvert\vec{B}\rvert}$ |
| 6 | Proyectil | $R = \dfrac{v_0^2 \sin 2\theta}{g}$, $H = \dfrac{v_0^2 \sin^2\theta}{2g}$ |
| 7 | Salir | — |

**Organización del código:**
- **Lectura y validación:** `leerNumero`, `leerVector`, `leerOpcion`.
- **Cálculo:** `calcular...`, `convertir...`, `sumar...`. No leen ni imprimen nada.
- **Presentación:** `mostrar...`.

Gracias a esa separación, cada fórmula se puede revisar sin mezclarla con el menú.

## Estado

- [x] Menú con las 6 opciones + salir
- [x] Validación de datos físicamente inválidos
- [x] Funciones independientes de cálculo y de presentación
- [ ] Casos de prueba registrados en el encabezado (al menos 3 por opción)
- [x] Comparación con cálculo manual, supuestos y conclusión en el encabezado
- [ ] Revisado y entregado en Moodle

## Archivos de esta carpeta

| Archivo | Descripción |
| --- | --- |
| [`taller1_caida_libre.py`](./taller1_caida_libre.py) | **Entregable.** Menú interactivo con los 6 puntos. El encabezado incluye fórmulas, supuestos, cálculo manual y conclusión. |
| [`Taller1.md`](./Taller1.md) | Enunciado del taller, transcrito del PDF. |
| [`images/`](./images/) | Capturas del enunciado original (puntos 1 a 6). |

## Cómo ejecutar

Solo necesita Python 3; no requiere librerías externas.

```bash
python3 unidad-1-fundamentos-y-geometria/taller1-caida-libre/taller1_caida_libre.py
```

## Antes de entregar

- [ ] Ejecutar el archivo desde cero y comprobar que no hay errores.
- [ ] Probar el menú a mano con al menos 3 casos por opción.
- [ ] Poder explicar y modificar cualquier función.
- [ ] Revisar en Moodle la fecha y las condiciones de entrega.
