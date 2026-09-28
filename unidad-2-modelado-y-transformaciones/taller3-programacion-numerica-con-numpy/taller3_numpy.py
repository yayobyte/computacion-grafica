"""
Taller 3 - Programación numérica con Python y NumPy.

Menú interactivo que integra los 7 ejercicios del taller y una opción 8 para salir.
Cada ejercicio es una función independiente que crea sus arreglos, opera sobre ellos
sin ciclos (operaciones vectorizadas) e informa forma (shape), dimensiones (ndim),
tipo de dato (dtype) y resultados.

-------------------------------------------------------------------------------
¿POR QUÉ ARREGLOS DE NUMPY?
-------------------------------------------------------------------------------
- Un ndarray guarda datos del MISMO tipo en memoria contigua, así que una operación
  como a + b se ejecuta en C sobre todos los elementos a la vez (vectorización), sin
  ciclos en Python. Es más rápido y el código se parece a la notación matemática.
- La forma (shape) permite ver los mismos datos como vector (1D) o matriz (2D) sin
  copiarlos, que es justo lo que se necesita para álgebra vectorial y matricial.
- np.nan permite representar datos faltantes sin romper el tipo float del arreglo.

-------------------------------------------------------------------------------
VERIFICACIONES (cálculo manual o propiedad matemática)
-------------------------------------------------------------------------------
El programa imprime cada verificación con ✓ o ✗ al ejecutar el ejercicio.
1. Ej. 1: la suma de 1..10 debe ser n(n+1)/2 = 10*11/2 = 55.
2. Ej. 2: suma total de a = 2 + 4 + 6 + 8 + 10 = 30; además (a + b) - b debe ser a.
3. Ej. 4: la raíz es la inversa del cuadrado: (sqrt(M + 10))^2 debe ser M + 10.
4. Ej. 5: A = [[1,2],[3,4],[5,6]]. A @ A^T es 3x3 y simétrica, con
   (A A^T)[0,0] = 1*1 + 2*2 = 5  y  (A A^T)[0,1] = 1*3 + 2*4 = 11.
5. Ej. 6: con los nan en 0: (4 + 0 + 6 + 0 + 10) / 5 = 20 / 5 = 4.0.
6. Ej. 7: el arreglo cargado debe ser igual al original en valores, forma y tipo.

Herramientas: Python 3, NumPy.
Asistencia de IA: Claude OPUS 5.5 (Anthropic).
"""

from pathlib import Path

import numpy as np

# datos.npy se guarda junto a este archivo, sin importar desde dónde se ejecute
RUTA_DATOS = Path(__file__).with_name("datos.npy")


# =============================================================================
# Utilidades de presentación
# =============================================================================

def mostrarArray(descripcion, arreglo):
    """Imprime un arreglo con su forma, número de dimensiones y tipo de dato."""
    print(f"\n  {descripcion}:")
    print("    " + str(arreglo).replace("\n", "\n    "))
    print(f"    shape = {arreglo.shape}, ndim = {arreglo.ndim}, dtype = {arreglo.dtype}")


def verificar(descripcion, condicion):
    """Muestra el resultado de una verificación (cálculo manual o propiedad)."""
    print(f"  {'✓' if condicion else '✗'} Verificación: {descripcion}")


# =============================================================================
# Ejercicios
# =============================================================================

def ejercicio1CreacionYPropiedades():
    print("\n=== Ejercicio 1: Creación y propiedades de arrays ===")
    # Vector 1D: los datos son una secuencia simple, una sola dimensión basta
    original = np.array(range(1, 11))
    # reshape reorganiza los mismos 10 datos en 2 filas x 5 columnas (2 * 5 = 10)
    reestructurado = original.reshape(2, 5)

    mostrarArray("Array original (1 al 10)", original)
    mostrarArray("Array reestructurado (2x5)", reestructurado)
    print(f"\n  Forma (shape) del reestructurado:      {reestructurado.shape}")
    print(f"  Tamaño total (size), cantidad de datos: {reestructurado.size}")
    print(f"  Número de dimensiones (ndim):           {reestructurado.ndim}")

    verificar("size = 2 * 5 = 10 (reshape no pierde ni agrega datos)", reestructurado.size == 10)
    verificar("suma 1..10 = n(n+1)/2 = 55", reestructurado.sum() == 10 * 11 // 2)


def ejercicio2OperacionesBasicas():
    print("\n=== Ejercicio 2: Operaciones básicas entre arrays ===")
    a = np.array([2, 4, 6, 8, 10])
    b = np.array([1, 3, 5, 7, 9])
    mostrarArray("a", a)
    mostrarArray("b", b)

    # "Elemento a elemento" significa que la operación se aplica a cada pareja de
    # elementos en la misma posición: (a + b)[i] = a[i] + b[i]. Por eso a y b deben
    # tener la misma forma. NumPy lo hace en una sola instrucción, sin ciclos for.
    mostrarArray("Suma elemento a elemento (a + b)", a + b)
    mostrarArray("Resta elemento a elemento (a - b)", a - b)
    mostrarArray("Producto elemento a elemento (a * b)", a * b)
    sumaTotal = np.sum(a)
    print(f"\n  Suma total de los elementos de a: {sumaTotal}")

    verificar("suma total de a = 2 + 4 + 6 + 8 + 10 = 30", sumaTotal == 30)
    verificar("(a + b) - b = a (la resta deshace la suma)", np.array_equal((a + b) - b, a))


def ejercicio3IndexacionYSlicing():
    print("\n=== Ejercicio 3: Indexación y slicing ===")
    numeros = np.arange(20)  # 0, 1, ..., 19
    mostrarArray("Array del 0 al 19", numeros)

    # Indexación directa: los índices empiezan en 0, así que el quinto es numeros[4]
    print(f"\n  Quinto elemento (índice 4):          {numeros[4]}")
    # Slicing inicio:fin toma desde 'inicio' hasta 'fin - 1' (el fin NO se incluye).
    # Para ir de la posición 2 a la 6 inclusive, el fin debe ser 7.
    print(f"  Posiciones 2 a 6 (numeros[2:7]):     {numeros[2:7]}")
    # Un índice negativo cuenta desde el final: -3: significa "los últimos tres"
    print(f"  Últimos tres elementos (numeros[-3:]): {numeros[-3:]}")

    numeros[0] = 100  # modificación directa por índice
    mostrarArray("Array actualizado (posición 0 = 100)", numeros)


def ejercicio4BroadcastingYUfunc():
    print("\n=== Ejercicio 4: Broadcasting y funciones universales ===")
    matriz = np.arange(1, 10).reshape(3, 3)  # matriz 3x3 con los valores 1..9
    mostrarArray("Matriz 3x3", matriz)

    # Broadcasting: NumPy "estira" el escalar 10 hasta la forma 3x3 de la matriz, sin
    # copiarlo en memoria, y luego suma elemento a elemento. Es como sumar una matriz
    # 3x3 llena de dieces, pero sin crearla.
    masDiez = matriz + 10
    mostrarArray("Matriz + 10 (broadcasting)", masDiez)

    # np.sqrt es una función universal (ufunc): se aplica a cada elemento sin ciclos.
    # El dtype cambia de int64 a float64 porque las raíces no son enteras.
    raices = np.sqrt(masDiez)
    mostrarArray("Raíz cuadrada de cada elemento (np.sqrt)", np.round(raices, 4))

    verificar("(sqrt(M + 10))^2 = M + 10", np.allclose(raices ** 2, masDiez))
    verificar("sqrt(16) = 4 en la posición [1, 2] (6 + 10 = 16)", raices[1, 2] == 4.0)


def ejercicio5FormasYAlgebraLineal():
    print("\n=== Ejercicio 5: Manipulación de formas y álgebra lineal ===")
    datos = np.array([1, 2, 3, 4, 5, 6])
    matrizA = datos.reshape(3, 2)
    mostrarArray("Array de 6 números", datos)
    mostrarArray("Matriz A (3x2)", matrizA)
    mostrarArray("Transpuesta A^T (2x3)", matrizA.T)

    # Producto punto de matrices: cada elemento [i, j] del resultado es el producto
    # escalar entre la fila i de A y la columna j de A^T (es decir, la fila j de A).
    # Mide qué tanto "se parecen" las filas entre sí. Con (3x2) @ (2x3) las
    # dimensiones internas coinciden (2 = 2) y el resultado toma las externas: 3x3.
    producto = matrizA @ matrizA.T  # equivalente a np.dot(matrizA, matrizA.T)
    mostrarArray("Producto A @ A^T", producto)
    filas, columnas = producto.shape
    print(f"\n  Dimensiones de la matriz final: {filas}x{columnas}")

    verificar("(A A^T)[0,0] = 1*1 + 2*2 = 5", producto[0, 0] == 5)
    verificar("(A A^T)[0,1] = 1*3 + 2*4 = 11", producto[0, 1] == 11)
    verificar("A A^T es simétrica (igual a su transpuesta)", np.array_equal(producto, producto.T))


def ejercicio6DatosFaltantes():
    print("\n=== Ejercicio 6: Manejo de datos faltantes ===")
    # np.nan solo existe en tipo float, por eso el arreglo es float64
    original = np.array([4.0, np.nan, 6.0, np.nan, 10.0])
    corregido = np.nan_to_num(original, nan=0.0)  # reemplaza cada nan por 0
    mostrarArray("Array original (con nan)", original)
    mostrarArray("Array corregido (nan -> 0)", corregido)

    mediaOriginal = np.mean(original)
    mediaIgnorandoNan = np.nanmean(original)
    mediaCorregida = np.mean(corregido)
    print(f"\n  Media del array original (np.mean):          {mediaOriginal}")
    print(f"  Media del original ignorando nan (np.nanmean): {mediaIgnorandoNan:.4f}")
    print(f"  Media del array corregido:                   {mediaCorregida}")

    # Comparación:
    # - La media del original es nan porque cualquier operación con nan da nan:
    #   un dato desconocido hace desconocido el resultado.
    # - Al reemplazar nan por 0 la media sí se puede calcular (4.0), pero baja, porque
    #   los 0 cuentan como datos reales: se divide por 5 en lugar de 3.
    # - np.nanmean ignora los faltantes y promedia solo los 3 datos conocidos
    #   (20 / 3 = 6.6667). Reemplazar por 0 solo es correcto si el faltante
    #   realmente significa cero.

    verificar("media corregida = (4 + 0 + 6 + 0 + 10) / 5 = 4.0", mediaCorregida == 4.0)
    verificar("media del original es nan", np.isnan(mediaOriginal))


def ejercicio7GuardarYCargar():
    print("\n=== Ejercicio 7: Guardar y cargar arrays ===")
    original = np.array([[1.5, 2.5, 3.5], [4.5, 5.5, 6.5]])
    mostrarArray("Array original", original)

    np.save(RUTA_DATOS, original)  # formato binario .npy: guarda valores, forma y dtype
    print(f"\n  Guardado en: {RUTA_DATOS}")
    cargado = np.load(RUTA_DATOS)
    mostrarArray("Array cargado desde datos.npy", cargado)

    iguales = (np.array_equal(original, cargado)
               and original.shape == cargado.shape and original.dtype == cargado.dtype)
    verificar("el array cargado es igual al original (valores, forma y dtype)", iguales)


# =============================================================================
# Menú principal
# =============================================================================

OPCIONES = {
    "1": ("Creación y propiedades de arrays", ejercicio1CreacionYPropiedades),
    "2": ("Operaciones básicas entre arrays", ejercicio2OperacionesBasicas),
    "3": ("Indexación y slicing", ejercicio3IndexacionYSlicing),
    "4": ("Broadcasting y funciones universales", ejercicio4BroadcastingYUfunc),
    "5": ("Manipulación de formas y álgebra lineal", ejercicio5FormasYAlgebraLineal),
    "6": ("Manejo de datos faltantes", ejercicio6DatosFaltantes),
    "7": ("Guardar y cargar arrays", ejercicio7GuardarYCargar),
    "8": ("Salir", None),
}


def mostrarMenu():
    print("\n" + "=" * 50)
    print("  TALLER 3 · PROGRAMACIÓN NUMÉRICA CON NUMPY")
    print("=" * 50)
    for clave, (descripcion, _) in OPCIONES.items():
        print(f"  {clave}. {descripcion}")


def leerOpcion():
    """Pide una opción del menú hasta que sea válida."""
    while True:
        opcion = input("Elige una opción (1-8): ").strip()
        if opcion in OPCIONES:
            return opcion
        print("  ✗ Opción no válida. Escribe un número del 1 al 8.")


def menuPrincipal():
    while True:
        mostrarMenu()
        opcion = leerOpcion()
        if opcion == "8":
            print("\n¡Hasta luego!")
            break
        OPCIONES[opcion][1]()  # ejecuta el ejercicio elegido


if __name__ == "__main__":
    try:
        menuPrincipal()
    except (KeyboardInterrupt, EOFError):
        print("\n\nPrograma interrumpido. ¡Hasta luego!")
