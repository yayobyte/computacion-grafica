# Taller 2 — Control, Listas y Funciones en Python

Ruta sugerida: [← Taller 1](../taller1-caida-libre/) | [Unidad 1](../) | [Inicio](../../)

## Objetivo

Integrar estructuras condicionales, ciclos, listas, diccionarios y funciones en un sistema con menú. El sistema resuelve 10 ejercicios: calculadora, filtros, `map` + `lambda`, calificaciones, conteo de palabras, búsqueda, paréntesis, ordenamiento, contraseñas y agenda.

- **Valor:** 0,0 a 5,0 · trabajo individual · ~4 horas.
- **Evaluación (Moodle):** funcionamiento 40 %, corrección conceptual 25 %, organización y documentación 20 %, pruebas y verificación 15 %.

## Conceptos clave

| Concepto | Dónde se practica |
| --- | --- |
| Condicionales `if/elif/else` | Calificaciones (4), paréntesis (7), submenú de agenda (10) |
| Ciclos `for` / `while` | Filtrado (2), conteo (5), búsqueda sin `.index()` (6), validación de entradas |
| Listas | Filtrado, temperaturas, notas, búsqueda, ordenamiento |
| Diccionarios | Conteo de palabras (5), agenda (10), tabla de operaciones de la calculadora (1) |
| `map` + `lambda` | Celsius → Fahrenheit (3), `key=` de `sorted` (8) |
| Funciones con una responsabilidad | Capas: lectura → lógica pura → opción de menú → menú |

## Estado

- [x] Menú con las 10 opciones + salir, con validación de cada opción
- [x] Análisis de entradas, procesos y salidas en el encabezado
- [ ] Casos de prueba registrados en el encabezado (al menos 5)
- [ ] Revisado y entregado en Moodle

## Archivos de esta carpeta

| Archivo | Descripción |
| --- | --- |
| [`taller2_control_listas_funciones.py`](./taller2_control_listas_funciones.py) | **Entregable.** Menú con los 10 ejercicios. El encabezado incluye el análisis de entradas, procesos y salidas, los supuestos, los fallos que detectan las pruebas y la conclusión. |
| [`Taller2.md`](./Taller2.md) | Enunciado del taller, transcrito del PDF. |
| [`Taller2.pdf`](./Taller2.pdf) | Enunciado original. |

## Cómo ejecutar

Solo necesita Python 3; no requiere librerías externas.

```bash
python3 unidad-1-fundamentos-y-geometria/taller2-control-listas-funciones/taller2_control_listas_funciones.py
```

## Antes de entregar

- [ ] Ejecutar el archivo desde cero y comprobar que no hay errores.
- [ ] Probar el menú a mano y, si encuentras un fallo propio, registrarlo en el encabezado.
- [ ] Poder explicar y modificar cualquier función.
- [ ] Revisar en Moodle la fecha y las condiciones de entrega.
