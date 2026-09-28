"""
Taller 4 - Manejo de arrays y operaciones básicas usando NumPy.

Menú interactivo que integra los 10 ejercicios del taller y una opción 11 para salir.
Cada ejercicio es una función independiente que crea sus arreglos, los opera sin
ciclos (operaciones vectorizadas) e informa forma (shape), tamaño (size) y tipo (dtype).

-------------------------------------------------------------------------------
VERIFICACIONES (resultado esperado)
-------------------------------------------------------------------------------
El programa imprime cada verificación con ✓ o ✗ al ejecutar el ejercicio.
Ej. | Verificación                                   | Esperado
----+------------------------------------------------+------------------------------
 1  | suma de 1..10 = n(n+1)/2                       | 10 * 11 / 2 = 55
 2  | elemento central de la matriz 3x3              | matriz[1, 1] = 5
 3  | [1..5] + [1..5] = 2 * [1..5]                   | [2, 4, 6, 8, 10]
 4  | el primer elemento es e^1 = e                  | exp[0] = 2.718281828...
 4  | el logaritmo deshace la exponencial            | log(exp(x)) = x
 5  | pares de 1..10                                 | [2, 4, 6, 8, 10]
 5  | la máscara coincide con el slicing [1::2]      | mismos elementos
 6  | todos los aleatorios en el intervalo [0, 1)    | 0 <= x < 1, shape (10,)
 7  | media de 1..5 = (1 + 2 + 3 + 4 + 5) / 5        | 15 / 5 = 3.0
 8  | todos los elementos valen 7                    | [7, 7, 7, 7, 7]
 9  | [1, 2, 3] + [4, 5, 6]                          | [5, 7, 9]
10  | reshape conserva los 6 datos en 2x3            | shape (2, 3), matriz[1, 0] = 4

Herramientas: Python 3, NumPy.
Asistencia de IA: Claude OPUS 5.5 (Anthropic).
"""

import numpy as np


# =============================================================================
# Utilidades de presentación
# =============================================================================

def mostrarArray(descripcion, arreglo):
    """Imprime un arreglo con su forma, tamaño y tipo de dato."""
    print(f"\n  {descripcion}:")
    print("    " + str(arreglo).replace("\n", "\n    "))
    print(f"    shape = {arreglo.shape}, size = {arreglo.size}, dtype = {arreglo.dtype}")


def verificar(descripcion, condicion):
    """Muestra el resultado de una verificación contra su valor esperado."""
    print(f"  {'✓' if condicion else '✗'} Verificación: {descripcion}")


# =============================================================================
# Ejercicios
# =============================================================================

def ejercicio1ArrayUnidimensional():
    print("\n=== 1) Array unidimensional ===")
    # np.arange(inicio, fin) genera de 'inicio' a 'fin - 1': para llegar a 10, fin = 11
    numeros = np.arange(1, 11)
    mostrarArray("Array del 1 al 10", numeros)
    verificar("suma = 10 * 11 / 2 = 55", numeros.sum() == 55)


def ejercicio2ArrayMultidimensional():
    print("\n=== 2) Array multidimensional ===")
    # Se generan los 9 números en 1D y se reorganizan en 3 filas x 3 columnas
    matriz = np.arange(1, 10).reshape(3, 3)
    mostrarArray("Matriz 3x3 del 1 al 9", matriz)
    verificar("elemento central matriz[1, 1] = 5", matriz[1, 1] == 5)


def ejercicio3OperacionesBasicas():
    print("\n=== 3) Operaciones básicas con arrays ===")
    arregloA = np.arange(1, 6)
    arregloB = np.arange(1, 6)
    # La suma es elemento a elemento: suma[i] = arregloA[i] + arregloB[i], sin ciclos
    suma = arregloA + arregloB
    mostrarArray("Array A", arregloA)
    mostrarArray("Array B", arregloB)
    mostrarArray("A + B", suma)
    verificar("A + B = [2, 4, 6, 8, 10]", np.array_equal(suma, [2, 4, 6, 8, 10]))


def ejercicio4FuncionesMatematicas():
    print("\n=== 4) Funciones matemáticas ===")
    numeros = np.arange(1, 6)
    # np.exp es una función universal (ufunc): calcula e^x para cada elemento.
    # El resultado es float64 aunque la entrada sea entera, porque e^x no es entero.
    exponenciales = np.exp(numeros)
    mostrarArray("Array del 1 al 5", numeros)
    mostrarArray("Exponencial de cada elemento (e^x)", exponenciales)
    verificar("exp(1) = e = 2.718281828...", np.isclose(exponenciales[0], np.e))
    verificar("log(exp(x)) = x (el logaritmo deshace la exponencial)",
              np.allclose(np.log(exponenciales), numeros))


def ejercicio5IndexacionYSegmentacion():
    print("\n=== 5) Indexación y segmentación ===")
    numeros = np.arange(1, 11)
    # Indexación booleana: numeros % 2 == 0 produce una máscara [False, True, ...]
    # y numeros[mascara] conserva solo las posiciones donde la máscara es True.
    mascaraPares = numeros % 2 == 0
    pares = numeros[mascaraPares]
    mostrarArray("Array del 1 al 10", numeros)
    print(f"\n  Máscara (numeros % 2 == 0): {mascaraPares}")
    mostrarArray("Elementos pares", pares)
    verificar("pares = [2, 4, 6, 8, 10]", np.array_equal(pares, [2, 4, 6, 8, 10]))
    # Segmentación equivalente: desde el índice 1 (valor 2) hasta el final, de 2 en 2.
    # Solo funciona porque el arreglo es consecutivo; la máscara sirve para cualquier arreglo.
    verificar("la máscara coincide con el slicing numeros[1::2]",
              np.array_equal(pares, numeros[1::2]))


def ejercicio6DatosAleatorios():
    print("\n=== 6) Generación de datos aleatorios ===")
    # Generator.random() devuelve valores uniformes en [0, 1): incluye 0, excluye 1.
    # Sin semilla, cada ejecución produce números distintos.
    generador = np.random.default_rng()
    aleatorios = generador.random(10)
    mostrarArray("10 números aleatorios en [0, 1)", aleatorios)
    verificar("10 valores, todos con 0 <= x < 1",
              aleatorios.shape == (10,) and np.all((aleatorios >= 0) & (aleatorios < 1)))


def ejercicio7FuncionesAgregacion():
    print("\n=== 7) Funciones de agregación ===")
    numeros = np.arange(1, 6)
    # Una función de agregación resume todo el arreglo en un solo valor
    media = np.mean(numeros)
    mostrarArray("Array del 1 al 5", numeros)
    print(f"\n  Media de los elementos: {media}")
    verificar("media = (1 + 2 + 3 + 4 + 5) / 5 = 3.0", media == 3.0)


def ejercicio8FuncionesFabrica():
    print("\n=== 8) Creación de arrays con funciones de fábrica ===")
    # np.full(forma, valor) crea el arreglo ya lleno, sin crear uno vacío y recorrerlo
    sietes = np.full(5, 7)
    mostrarArray("Array de 5 elementos con valor 7 (np.full)", sietes)
    verificar("todos los elementos valen 7", np.all(sietes == 7) and sietes.size == 5)


def ejercicio9Broadcasting():
    print("\n=== 9) Operaciones de alineación y broadcasting ===")
    primeros = np.array([1, 2, 3])
    siguientes = np.array([4, 5, 6])
    # Broadcasting compara las formas desde la última dimensión: son compatibles si
    # son iguales o si una vale 1. Aquí ambas son (3,), así que se alinean posición a
    # posición sin estirar ninguna. Si una fuera escalar o de forma (1,), NumPy la
    # "estiraría" a (3,) sin copiarla en memoria.
    suma = primeros + siguientes
    mostrarArray("Array [1, 2, 3]", primeros)
    mostrarArray("Array [4, 5, 6]", siguientes)
    mostrarArray("Suma", suma)
    verificar("[1, 2, 3] + [4, 5, 6] = [5, 7, 9]", np.array_equal(suma, [5, 7, 9]))


def ejercicio10Redimensionamiento():
    print("\n=== 10) Transformación y redimensionamiento ===")
    numeros = np.arange(1, 7)
    # reshape(2, 3) reorganiza los mismos 6 datos en 2 filas x 3 columnas, llenando
    # fila por fila. Solo es válido si 2 * 3 = size (6).
    matriz = numeros.reshape(2, 3)
    mostrarArray("Array del 1 al 6", numeros)
    mostrarArray("Matriz 2x3", matriz)
    verificar("shape (2, 3) y matriz[1, 0] = 4 (inicio de la segunda fila)",
              matriz.shape == (2, 3) and matriz[1, 0] == 4)


# =============================================================================
# Menú principal
# =============================================================================

OPCIONES = {
    "1": ("Crear un array unidimensional", ejercicio1ArrayUnidimensional),
    "2": ("Crear un array multidimensional", ejercicio2ArrayMultidimensional),
    "3": ("Operaciones básicas con arrays", ejercicio3OperacionesBasicas),
    "4": ("Funciones matemáticas", ejercicio4FuncionesMatematicas),
    "5": ("Indexación y segmentación", ejercicio5IndexacionYSegmentacion),
    "6": ("Generación de datos aleatorios", ejercicio6DatosAleatorios),
    "7": ("Funciones de agregación", ejercicio7FuncionesAgregacion),
    "8": ("Creación de arrays con funciones de fábrica", ejercicio8FuncionesFabrica),
    "9": ("Operaciones de alineación y broadcasting", ejercicio9Broadcasting),
    "10": ("Funciones de transformación y redimensionamiento", ejercicio10Redimensionamiento),
    "11": ("Salir", None),
}


def mostrarMenu():
    print("\n" + "=" * 55)
    print("  TALLER 4 · ARRAYS Y OPERACIONES BÁSICAS CON NUMPY")
    print("=" * 55)
    for clave, (descripcion, _) in OPCIONES.items():
        print(f"  {clave:>2}. {descripcion}")


def leerOpcion():
    """Pide una opción del menú hasta que sea válida."""
    while True:
        opcion = input("Elige una opción (1-11): ").strip()
        if opcion in OPCIONES:
            return opcion
        print("  ✗ Opción no válida. Escribe un número del 1 al 11.")


def menuPrincipal():
    while True:
        mostrarMenu()
        opcion = leerOpcion()
        if opcion == "11":
            print("\n¡Hasta luego!")
            break
        OPCIONES[opcion][1]()  # ejecuta el ejercicio elegido


if __name__ == "__main__":
    try:
        menuPrincipal()
    except (KeyboardInterrupt, EOFError):
        print("\n\nPrograma interrumpido. ¡Hasta luego!")
