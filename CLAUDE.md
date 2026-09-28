# CLAUDE.md — Contexto para la IA en este repositorio

Repositorio de la asignatura **Computación Gráfica (UTP)**. El estudiante resuelve talleres en Python y la IA lo acompaña: implementa lo pedido, explica el porqué y lo deja listo para sustentar.

## Reglas de trabajo

1. **Hacer solo lo que se pide.** No agregar funcionalidades, archivos ni cambios en otros archivos (por ejemplo, los README) si el estudiante no lo solicita. Si algo extra parece útil, se propone en la respuesta, no se implementa.
2. **Sin código de pruebas automáticas** (`verificar`, `ejecutarPruebas`, modo `--pruebas`) salvo que el enunciado lo exija. Si el enunciado pide *casos de prueba*, van como tabla en el encabezado del `.py`. Si pide *verificaciones* dentro del programa, se imprimen en el propio ejercicio.
3. **No reescribir la voz del estudiante.** Si edita un archivo (por ejemplo, borra una sección), se respeta. Si eso deja incumplido un requisito del enunciado, se le avisa en lugar de revertirlo.
4. **Ejecutar antes de entregar.** Cada `.py` se corre de principio a fin, con entradas simuladas para los menús (`printf '...' | python ...`). Se hace en el scratchpad cuando genera archivos (por ejemplo, `datos.npy`), para no ensuciar el repo.
5. **Honestidad académica.** Nunca inventar un historial de pruebas o de fallos "encontrados" que el estudiante no vivió. Todo `.py` declara en su encabezado las herramientas y la asistencia de IA usada.

## Cómo son los enunciados

Cada taller llega con **dos fuentes**, y ambas deben cumplirse:

- **El PDF del profesor** (se transcribe a `TallerN.md` en la carpeta del taller): los ejercicios concretos y el **menú integrador** (una opción por ejercicio + "Salir").
- **El encabezado de Moodle**: propósito, procedimiento y producto. Siempre exige un `.py` ejecutable y documentado. La evaluación suele ser: funcionamiento 40 %, corrección conceptual 25 %, organización y documentación 20 %, pruebas y verificación 15 %.

Antes de escribir código, se leen ambos y se identifica qué pide cada uno. Por ejemplo, el número mínimo de casos de prueba o las verificaciones manuales.

## Estructura del repositorio

```
unidad-N-<tema>/
└── tallerN-<tema>/
    ├── TallerN.md / TallerN.pdf   ← enunciado (no modificar)
    └── tallerN_<tema>.py          ← entregable
```

- Unidad 1: talleres 1 (caída libre), 2 (control, listas y funciones) y 3 (NumPy).
- Unidad 2: taller 7 (series de Taylor).
- Entorno virtual en `.venv/` con `requirements.txt` (numpy, matplotlib). Se ejecuta con `.venv/bin/python`.

## Convenciones del código

- **Idioma:** comentarios, mensajes y documentación en **español**. Los nombres de funciones y variables van en español, en camelCase, siguiendo el estilo de clase (`miFactorial`, `calcularTiempoCaida`, `leerNumero`).
- **Encabezado (docstring)** del `.py`, según lo que pida el enunciado: propósito, fórmulas, supuestos, casos de prueba, comparación con cálculo manual, conclusión y "Herramientas / Asistencia de IA".
- **Organización por capas:** lectura y validación (`leer...`), lógica pura que no lee ni imprime, presentación (`mostrar...`), opciones del menú y `menuPrincipal()` con un diccionario `OPCIONES`.
- **Menú:** valida la opción (repite si es inválida), tiene "Salir" como última opción y captura `KeyboardInterrupt`/`EOFError` en `if __name__ == "__main__":`.
- **Validación de entradas:** rechazar datos física o matemáticamente inválidos (alturas o tiempos negativos, división por cero, etc.) y volver a pedirlos.
- **Resultados con unidades** y mensajes descriptivos, nunca solo el valor.
- **Taller 7 (gráficas):** se sigue el estilo del código de clase (`np.frompyfunc`, `plt.subplot`), con dominios justificados y el error en escala log.
