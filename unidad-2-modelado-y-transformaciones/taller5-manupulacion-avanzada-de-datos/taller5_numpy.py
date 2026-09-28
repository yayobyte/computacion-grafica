"""
Taller 5 - Manipulación avanzada de arrays con NumPy.

Resuelve los 18 puntos del taller sobre los vectores A, B y C, organizados en un menú
por grupos: creación y concatenación (1-3), estadísticas (4-10), filtrado con máscaras
booleanas (11-12) y modificaciones de C (13-18). Cada resultado se identifica con su
número de punto y se acompaña de pruebas de dimensiones y valores (✓ / ✗).

-------------------------------------------------------------------------------
DECISIONES DE IMPLEMENTACIÓN
-------------------------------------------------------------------------------
1. Posiciones contadas desde 1: "los elementos 5 y 15" son el 5.º y el 15.º elemento,
   es decir, los índices NumPy 4 y 14. "Del 6 al 8" es el segmento C[5:8]. Se eligió
   así porque el enunciado habla de posiciones como las contaría una persona, y
   "respectivamente" indica una asignación posición por posición.
2. Las modificaciones se acumulan: 13 cambia C, 15 ordena ese C, 16 lo multiplica por
   10, y 17 y 18 trabajan sobre el resultado. Para que el menú dé siempre lo mismo sin
   importar el orden en que se elijan las opciones, el grupo 13-18 parte de un C nuevo
   (el de los puntos 1-3) y aplica los seis pasos en orden.
3. Filtros con '&' y no con 'and': 'and' de Python espera UN booleano, mientras que
   (C > 5) & (C < 15) combina las máscaras elemento a elemento. Los paréntesis son
   obligatorios porque '&' tiene más precedencia que '>' y '<'.
4. Moda con np.unique(..., return_counts=True): NumPy no tiene una función de moda.
   np.unique entrega los valores distintos y cuántas veces aparece cada uno, y se
   retornan TODOS los valores con el conteo máximo por si hay empate.

-------------------------------------------------------------------------------
COMPARACIÓN DE RESULTADOS (puntos 7, 8 y 9)
-------------------------------------------------------------------------------
Suma de C = (2+3+5+1+4+7+9+8+6+10) + (11+...+20) = 55 + 155 = 210, con 20 elementos:
    7. suma / división:  210 / 20 = 10.5
    8. np.average(C):    10.5  (promedio; admite pesos, aquí todos valen 1)
    9. np.mean(C):       10.5  (media aritmética)
Los tres coinciden porque, sin pesos, promedio y media aritmética son la misma operación.

Herramientas: Python 3, NumPy.
Asistencia de IA: Claude OPUS 5.5 (Anthropic).
"""

import numpy as np

VALORES_A = [2, 3, 5, 1, 4, 7, 9, 8, 6, 10]


# =============================================================================
# Utilidades
# =============================================================================

def mostrar(punto, descripcion, valor):
    """Imprime un resultado identificado con su número de punto."""
    texto = str(valor).replace("\n", "\n      ")
    print(f"\n  [{punto:>2}] {descripcion}:\n      {texto}")
    if isinstance(valor, np.ndarray):
        print(f"      shape = {valor.shape}, size = {valor.size}, dtype = {valor.dtype}")


def verificar(descripcion, condicion):
    """Muestra el resultado de una prueba de dimensiones o valores."""
    print(f"       {'✓' if condicion else '✗'} Prueba: {descripcion}")


def asignarEnPosiciones(vector, posicionInicial, valores):
    """Asigna 'valores' desde la posición 'posicionInicial' (contando desde 1).
    Valida que el segmento exista y tenga la misma cantidad de elementos que 'valores'."""
    valores = np.asarray(valores)
    inicio = posicionInicial - 1  # posición humana -> índice NumPy
    fin = inicio + valores.size
    if inicio < 0 or fin > vector.size:
        raise ValueError(f"Las posiciones {posicionInicial}..{posicionInicial + valores.size - 1} "
                         f"no existen en un vector de {vector.size} elementos.")
    segmento = vector[inicio:fin]
    if segmento.shape != valores.shape:
        raise ValueError(f"Dimensiones incompatibles: segmento {segmento.shape} vs valores {valores.shape}.")
    vector[inicio:fin] = valores


def calcularModa(vector):
    """Retorna un arreglo con el valor o los valores más frecuentes y su frecuencia."""
    valores, conteos = np.unique(vector, return_counts=True)
    frecuenciaMaxima = conteos.max()
    return valores[conteos == frecuenciaMaxima], frecuenciaMaxima


# =============================================================================
# Puntos 1-3: creación y concatenación
# =============================================================================

def crearVectores():
    """Retorna (A, B, C) según los puntos 1 a 3. C es una copia nueva en cada llamada."""
    vectorA = np.array(VALORES_A)
    vectorB = np.arange(11, 21)  # arange excluye el final: 11..20
    # Concatenar une A y B en una sola fila (1D). Ambos deben ser 1D para que el
    # resultado sea un vector de A.size + B.size elementos.
    vectorC = np.concatenate((vectorA, vectorB))
    return vectorA, vectorB, vectorC


def grupoCreacion():
    print("\n=== Puntos 1-3: creación y concatenación ===")
    vectorA, vectorB, vectorC = crearVectores()
    mostrar(1, "Vector A", vectorA)
    mostrar(2, "Vector B (11 al 20)", vectorB)
    mostrar(3, "Vector C = [A, B] en la misma fila", vectorC)
    verificar("A y B son 1D (ndim = 1), requisito para concatenar en una fila",
              vectorA.ndim == 1 and vectorB.ndim == 1)
    verificar("C tiene 10 + 10 = 20 elementos y es 1D", vectorC.shape == (20,))
    verificar("C empieza con A y termina con B",
              np.array_equal(vectorC[:10], vectorA) and np.array_equal(vectorC[10:], vectorB))


# =============================================================================
# Puntos 4-10: estadísticas
# =============================================================================

def grupoEstadisticas():
    print("\n=== Puntos 4-10: estadísticas de C ===")
    _, _, vectorC = crearVectores()
    minimo = np.min(vectorC)
    maximo = np.max(vectorC)
    longitud = np.size(vectorC)  # función de NumPy (len() sería la de Python)
    suma = np.sum(vectorC)
    promedioManual = suma / longitud  # operaciones elementales: suma y división
    promedio = np.average(vectorC)
    media = np.mean(vectorC)

    mostrar(4, "Mínimo (np.min)", minimo)
    mostrar(5, "Máximo (np.max)", maximo)
    mostrar(6, "Longitud (np.size)", longitud)
    mostrar(7, "Promedio con suma / división", promedioManual)
    mostrar(8, "Promedio (np.average)", promedio)
    mostrar(9, "Media (np.mean)", media)
    mostrar(10, "Suma (np.sum)", suma)

    verificar("mínimo = 1 y máximo = 20", minimo == 1 and maximo == 20)
    verificar("suma = 55 + 155 = 210 y longitud = 20", suma == 210 and longitud == 20)
    verificar("puntos 7, 8 y 9 coinciden en 10.5", promedioManual == promedio == media == 10.5)


# =============================================================================
# Puntos 11-12: filtrado con máscaras booleanas
# =============================================================================

def grupoFiltrado():
    print("\n=== Puntos 11-12: filtrado con máscaras booleanas ===")
    _, _, vectorC = crearVectores()
    # La máscara es un arreglo de True/False del mismo tamaño que C;
    # C[mascara] conserva solo los elementos donde la máscara es True.
    vectorD = vectorC[vectorC > 5]
    vectorE = vectorC[(vectorC > 5) & (vectorC < 15)]

    mostrar(11, "D = elementos de C mayores que 5", vectorD)
    mostrar(12, "E = elementos de C mayores que 5 y menores que 15", vectorE)

    verificar("todos los elementos de D son > 5", np.all(vectorD > 5))
    verificar("D tiene 20 - 5 = 15 elementos (se excluyen 1, 2, 3, 4, 5)", vectorD.size == 15)
    verificar("E = [7, 9, 8, 6, 10, 11, 12, 13, 14] (conserva el orden de C)",
              np.array_equal(vectorE, [7, 9, 8, 6, 10, 11, 12, 13, 14]))


# =============================================================================
# Puntos 13-18: modificaciones de C (se acumulan en orden)
# =============================================================================

def grupoModificaciones():
    print("\n=== Puntos 13-18: modificaciones de C (acumulativas) ===")
    _, _, vectorC = crearVectores()
    print(f"\n  C inicial: {vectorC}")

    # 13. Elementos 5 y 15 (índices 4 y 14) por 7, con indexación por lista de índices
    vectorC[[4, 14]] = 7
    mostrar(13, "C con los elementos 5 y 15 cambiados por 7", vectorC)
    verificar("C[4] = C[14] = 7 (antes valían 4 y 15)", vectorC[4] == 7 and vectorC[14] == 7)

    # 14. Moda: el 7 ya existía una vez y ahora aparece tres veces
    moda, frecuencia = calcularModa(vectorC)
    mostrar(14, f"Moda de C (aparece {frecuencia} veces)", moda)
    verificar("moda = 7 con frecuencia 3", np.array_equal(moda, [7]) and frecuencia == 3)

    # 15. Orden ascendente: np.sort retorna una copia ordenada que reemplaza a C
    vectorC = np.sort(vectorC)
    mostrar(15, "C ordenado de menor a mayor", vectorC)
    verificar("cada elemento es <= al siguiente", np.all(vectorC[:-1] <= vectorC[1:]))

    # 16. Multiplicar por 10: broadcasting del escalar sobre los 20 elementos
    vectorC = vectorC * 10
    mostrar(16, "C multiplicado por 10", vectorC)
    # Tras el punto 13 la suma es 210 - 4 - 15 + 7 + 7 = 205; ordenar no la cambia
    verificar("suma = 205 * 10 = 2050", vectorC.sum() == 2050)

    # 17 y 18. Asignación por segmento con validación de dimensiones (3 posiciones = 3 valores)
    asignarEnPosiciones(vectorC, 6, [60, 70, 80])
    mostrar(17, "C con los elementos 6 al 8 cambiados por 60, 70, 80", vectorC)
    verificar("C[5:8] = [60, 70, 80]", np.array_equal(vectorC[5:8], [60, 70, 80]))

    asignarEnPosiciones(vectorC, 14, [140, 150, 160])
    mostrar(18, "C con los elementos 14 al 16 cambiados por 140, 150, 160", vectorC)
    verificar("C[13:16] = [140, 150, 160]", np.array_equal(vectorC[13:16], [140, 150, 160]))
    verificar("C conserva su forma (20,) tras todas las modificaciones", vectorC.shape == (20,))


def ejecutarTodo():
    grupoCreacion()
    grupoEstadisticas()
    grupoFiltrado()
    grupoModificaciones()


# =============================================================================
# Menú principal
# =============================================================================

OPCIONES = {
    "1": ("Puntos 1-3: crear A, B y C", grupoCreacion),
    "2": ("Puntos 4-10: estadísticas de C", grupoEstadisticas),
    "3": ("Puntos 11-12: filtrado con máscaras", grupoFiltrado),
    "4": ("Puntos 13-18: modificaciones de C", grupoModificaciones),
    "5": ("Ejecutar todos los puntos (1-18)", ejecutarTodo),
    "6": ("Salir", None),
}


def mostrarMenu():
    print("\n" + "=" * 50)
    print("  TALLER 5 · MANIPULACIÓN AVANZADA CON NUMPY")
    print("=" * 50)
    for clave, (descripcion, _) in OPCIONES.items():
        print(f"  {clave}. {descripcion}")


def leerOpcion():
    """Pide una opción del menú hasta que sea válida."""
    while True:
        opcion = input("Elige una opción (1-6): ").strip()
        if opcion in OPCIONES:
            return opcion
        print("  ✗ Opción no válida. Escribe un número del 1 al 6.")


def menuPrincipal():
    while True:
        mostrarMenu()
        opcion = leerOpcion()
        if opcion == "6":
            print("\n¡Hasta luego!")
            break
        OPCIONES[opcion][1]()  # ejecuta el grupo elegido


if __name__ == "__main__":
    try:
        menuPrincipal()
    except (KeyboardInterrupt, EOFError):
        print("\n\nPrograma interrumpido. ¡Hasta luego!")
