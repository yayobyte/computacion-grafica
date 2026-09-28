# Taller número 2. Programación en Python (Subrutinas, Estructuras de Control, Arreglos y Listas).

## Objetivos:

- Practicar la definición y uso de funciones y procedimientos en Python.
- Aplicar estructuras de control para resolver problemas variados.
- Manejar arreglos y listas para el procesamiento de datos.
- Integrar diversos conceptos de programación en un solo sistema.

## Metodología:

- Cada ejercicio se desarrollará individualmente, seguido de una sesión de revisión grupal para discutir las soluciones y posibles mejoras.
- Se fomentará el uso de buenas prácticas de programación, incluyendo la documentación adecuada de cada función y procedimiento.

## Recursos Necesarios:

- Computadora con Python instalado.
- Editor de texto o IDE para desarrollo en Python (por ejemplo, Visual Studio Code, PyCharm, Jupyter Notebook).

## Evaluación:

- Cada ejercicio será revisado y evaluado basándose en la corrección, eficiencia, y legibilidad del código.
- Se realizará una demostración a través del menu para evaluar la integración efectiva de las subrutinas en un sistema funcional.

## Feedback y Reflexión:

- Al final del taller, se realizará una sesión de feedback donde los participantes podrán compartir sus experiencias, dificultades encontradas y cómo las superaron.
- Se discutirán las lecciones aprendidas y la importancia de cada concepto abordado en el taller para el desarrollo de software en Python.

## Puntos del taller:

1. **Calculadora Básica:**
   Crea una función para cada operación básica (suma, resta, multiplicación, división) que acepte dos argumentos y devuelva el resultado. Implementa una función principal que solicite al usuario números y la operación a realizar, utilizando las funciones creadas.

2. **Filtrado de Lista:**
   Desarrolla una función que reciba una lista de números y devuelva solo aquellos que sean pares. Utiliza un bucle y condicionales dentro de la función.

3. **Transformación de Listas con Map y Lambda:**
   Escribe un script que utilice `map` y una función `lambda` para convertir todas las temperaturas de una lista de grados Celsius a Fahrenheit.

4. **Sistema de Calificaciones:**
   Implementa una función que reciba una lista de calificaciones numéricas y devuelva una lista con las calificaciones convertidas a letras (A, B, C, D, F) según el rango en el que se encuentren.

5. **Conteo de Palabras:**
   Crea una función que reciba una cadena de texto y retorne un diccionario con el conteo de cuántas veces aparece cada palabra. Considera ignorar mayúsculas y signos de puntuación.

6. **Función de Búsqueda:**
   Desarrolla una función que busque un elemento dado dentro de una lista y devuelva su índice si lo encuentra o -1 si no está presente. No utilices métodos predefinidos como `.index()`.

7. **Validación de Paréntesis:**
   Escribe una función que tome una cadena de solo paréntesis `(` y `)` y determine si la secuencia es válida (cada paréntesis abierto tiene un correspondiente paréntesis cerrado).

8. **Ordenamiento Personalizado:**
   Implementa una función que ordene una lista de tuplas (nombre, edad) primero por edad y luego por nombre (ambos en orden ascendente). Puedes usar la función `sort` o `sorted` con parámetros personalizados.

9. **Generador de Contraseñas:**
   Crea una función que genere una contraseña aleatoria que consista en una combinación de letras mayúsculas, minúsculas, números y símbolos. La longitud de la contraseña debe ser un parámetro de la función.

10. **Gestión de Agenda Telefónica:**
    Desarrolla un programa que utilice funciones para permitir al usuario agregar, buscar, eliminar y mostrar todos los contactos de una agenda telefónica almacenada en un diccionario.

## Programa Integrador con Menú de Opciones:

Desarrollar un programa en Python que integre todas las funcionalidades de los ejercicios anteriores en un menú interactivo, permitiendo al usuario elegir qué tarea realizar. El programa debe comenzar mostrando al usuario un menú de opciones que incluya las siguientes funcionalidades:

1. Operaciones Básicas (Calculadora)
2. Filtrado de Lista por Números Pares
3. Conversión de Temperaturas de Celsius a Fahrenheit
4. Sistema de Calificaciones a Letras
5. Conteo de Palabras en una Cadena
6. Búsqueda de Elemento en Lista
7. Validación de Secuencia de Paréntesis
8. Ordenamiento Personalizado de Lista de Tuplas
9. Generador de Contraseñas Aleatorias
10. Gestión de Agenda Telefónica
11. Salir del Programa

Cada opción del menú debe corresponder a una función específica implementada en los ejercicios del 1 al 10. La opción de "Salir del Programa" debe terminar la ejecución del mismo.
