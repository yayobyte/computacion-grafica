"""
Taller 1 - Física computacional en Python (de caída libre a proyectiles).

Menú interactivo que integra los 6 puntos del taller y una opción 7 para salir.
Cada punto tiene una función de CÁLCULO (no pide ni imprime nada) y una función
para MOSTRAR resultados, además de funciones de LECTURA que validan la entrada.

-------------------------------------------------------------------------------
FÓRMULAS
-------------------------------------------------------------------------------
1. Caída libre:            t = sqrt(2h / g)
2. Conversión velocidad:   v[m/s] = v[km/h] / 3.6     v[km/h] = v[m/s] * 3.6
                           (1 km/h = 1000 m / 3600 s = 1/3.6 m/s)
3. Desplazamiento MRUA:    s = u*t + (1/2)*a*t^2
4. Suma de vectores:       A + B = [Ax + Bx, Ay + By]
5. Producto escalar:       A . B = Ax*Bx + Ay*By
   Ángulo entre vectores:  cos(theta) = (A . B) / (|A| * |B|),  |A| = sqrt(Ax^2 + Ay^2)
6. Proyectil:              R = v0^2 * sin(2*theta) / g
                           H = v0^2 * sin^2(theta) / (2g)
                           t_vuelo = 2 * v0 * sin(theta) / g

-------------------------------------------------------------------------------
SUPUESTOS
-------------------------------------------------------------------------------
- g = 9.81 m/s^2 constante, sin resistencia del aire.
- Caída libre: el objeto parte del reposo.
- Proyectil: se lanza y aterriza a la misma altura (suelo plano), con
  0 <= theta <= 90 grados. Fuera de ese rango el proyectil iría hacia atrás o hacia abajo.
- MRUA: u y a pueden ser negativos (sentido contrario o frenado); el tiempo no.
- Vectores en 2D. Para calcular el ángulo ningún vector puede ser [0, 0],
  porque su magnitud es 0 y la división no está definida.
- Datos rechazados por ser físicamente inválidos: altura negativa, tiempo
  negativo, rapidez negativa, velocidad inicial negativa y ángulo fuera de [0, 90].

-------------------------------------------------------------------------------
COMPARACIÓN CON CÁLCULO MANUAL
-------------------------------------------------------------------------------
Caída libre, h = 20 m:
    t = sqrt(2 * 20 / 9.81) = sqrt(40 / 9.81) = sqrt(4.0775) = 2.0193 s
    Programa: 2.0193 s  -> coincide.
Proyectil, v0 = 20 m/s, theta = 45 grados (sin 90 = 1, sin 45 = 0.7071):
    R = 20^2 * 1 / 9.81 = 400 / 9.81 = 40.7747 m
    H = 400 * 0.7071^2 / (2 * 9.81) = 400 * 0.5 / 19.62 = 10.1937 m
    Programa: R = 40.7747 m, H = 10.1937 m  -> coincide.

-------------------------------------------------------------------------------
CONCLUSIÓN
-------------------------------------------------------------------------------
Los resultados del programa coinciden con el cálculo manual hasta la cuarta cifra
decimal en todos los casos probados. Separar cálculo, lectura y presentación permite
revisar cada fórmula por separado, sin mezclarla con el menú. Los casos límite
confirman el comportamiento físico esperado: h = 0 da t = 0, a 90 grados el alcance es
nulo y la altura máxima, y vectores perpendiculares tienen producto escalar 0. La
validación evita resultados sin sentido, como la raíz de una altura negativa o el
ángulo de un vector nulo.

Herramientas: Python 3 (solo biblioteca estándar: math).
Asistencia de IA: Claude OPUS 5.5 (Anthropic).
"""

import math

G = 9.81  # aceleración de la gravedad [m/s^2]


# =============================================================================
# Lectura y validación de datos
# =============================================================================

def leerNumero(mensaje, minimo=None, maximo=None):
    """Pide un número real hasta que sea válido y esté dentro de [minimo, maximo]."""
    while True:
        texto = input(mensaje).strip().replace(",", ".")  # acepta 9,81 o 9.81
        try:
            valor = float(texto)
        except ValueError:
            print("  ✗ Debe ser un número. Intenta de nuevo.")
            continue
        if not math.isfinite(valor):
            print("  ✗ El valor debe ser finito.")
        elif minimo is not None and valor < minimo:
            print(f"  ✗ El valor no puede ser menor que {minimo}.")
        elif maximo is not None and valor > maximo:
            print(f"  ✗ El valor no puede ser mayor que {maximo}.")
        else:
            return valor


def leerVector(nombre):
    """Pide las componentes x, y de un vector 2D y lo retorna como lista [x, y]."""
    print(f"Vector {nombre}:")
    x = leerNumero(f"  {nombre}x = ")
    y = leerNumero(f"  {nombre}y = ")
    return [x, y]


def leerOpcion(mensaje, opcionesValidas):
    """Pide una opción hasta que el usuario escriba una de opcionesValidas."""
    while True:
        opcion = input(mensaje).strip()
        if opcion in opcionesValidas:
            return opcion
        print(f"  ✗ Opción no válida. Elige entre: {', '.join(opcionesValidas)}.")


# =============================================================================
# Funciones de cálculo (independientes: no leen ni imprimen)
# =============================================================================

def calcularTiempoCaida(altura, g=G):
    """Tiempo [s] que tarda en caer un objeto desde 'altura' [m], partiendo del reposo."""
    if altura < 0:
        raise ValueError("La altura no puede ser negativa.")
    return math.sqrt(2 * altura / g)


def convertirVelocidad(velocidad, tipoConversion):
    """Convierte velocidad. tipoConversion: 'kmh_a_ms' o 'ms_a_kmh'."""
    if velocidad < 0:
        raise ValueError("La rapidez no puede ser negativa.")
    if tipoConversion == "kmh_a_ms":
        return velocidad / 3.6
    elif tipoConversion == "ms_a_kmh":
        return velocidad * 3.6
    else:
        raise ValueError(f"Tipo de conversión desconocido: {tipoConversion}")


def calcularDesplazamiento(velocidadInicial, aceleracion, tiempo):
    """Desplazamiento [m] en MRUA: s = u*t + (1/2)*a*t^2."""
    if tiempo < 0:
        raise ValueError("El tiempo no puede ser negativo.")
    return velocidadInicial * tiempo + 0.5 * aceleracion * tiempo**2


def sumarVectores(vectorA, vectorB):
    """Suma componente a componente de dos vectores 2D representados como listas."""
    return [vectorA[0] + vectorB[0], vectorA[1] + vectorB[1]]


def calcularMagnitud(vector):
    """Magnitud (norma euclidiana) de un vector 2D."""
    return math.sqrt(vector[0]**2 + vector[1]**2)


def calcularProductoEscalar(vectorA, vectorB):
    """Producto escalar A . B = Ax*Bx + Ay*By."""
    return vectorA[0] * vectorB[0] + vectorA[1] * vectorB[1]


def calcularAnguloEntreVectores(vectorA, vectorB):
    """Ángulo [grados] entre A y B usando cos(theta) = (A . B) / (|A| |B|)."""
    magnitudA = calcularMagnitud(vectorA)
    magnitudB = calcularMagnitud(vectorB)
    if magnitudA == 0 or magnitudB == 0:
        raise ValueError("El ángulo no está definido si un vector es [0, 0].")
    cosTheta = calcularProductoEscalar(vectorA, vectorB) / (magnitudA * magnitudB)
    # Por redondeo, cosTheta puede quedar en 1.0000000002 y acos fallaría: se recorta a [-1, 1]
    cosTheta = max(-1.0, min(1.0, cosTheta))
    return math.degrees(math.acos(cosTheta))


def calcularProyectil(velocidadInicial, anguloGrados, g=G):
    """Retorna (alcance R [m], altura máxima H [m], tiempo de vuelo [s])."""
    if velocidadInicial < 0:
        raise ValueError("La velocidad inicial no puede ser negativa.")
    if not 0 <= anguloGrados <= 90:
        raise ValueError("El ángulo debe estar entre 0 y 90 grados.")
    theta = math.radians(anguloGrados)  # math.sin trabaja en radianes
    alcance = velocidadInicial**2 * math.sin(2 * theta) / g
    alturaMaxima = velocidadInicial**2 * math.sin(theta)**2 / (2 * g)
    tiempoVuelo = 2 * velocidadInicial * math.sin(theta) / g
    # sin(180°) da 1.2e-16 en lugar de 0 por redondeo; se limpia para no mostrar "-0.0000"
    if abs(alcance) < 1e-9:
        alcance = 0.0
    return alcance, alturaMaxima, tiempoVuelo


# =============================================================================
# Funciones para mostrar resultados (con unidades)
# =============================================================================

def formatearVector(vector):
    return f"[{vector[0]:.4f}, {vector[1]:.4f}]"


def mostrarCaidaLibre(altura, tiempo):
    print(f"\n  Altura:           h = {altura:.4f} m")
    print(f"  Tiempo de caída:  t = {tiempo:.4f} s")


def mostrarConversion(valorEntrada, valorSalida, tipoConversion):
    unidadEntrada, unidadSalida = ("km/h", "m/s") if tipoConversion == "kmh_a_ms" else ("m/s", "km/h")
    print(f"\n  {valorEntrada:.4f} {unidadEntrada} = {valorSalida:.4f} {unidadSalida}")


def mostrarDesplazamiento(velocidadInicial, aceleracion, tiempo, desplazamiento):
    print(f"\n  u = {velocidadInicial:.4f} m/s,  a = {aceleracion:.4f} m/s^2,  t = {tiempo:.4f} s")
    print(f"  Desplazamiento:   s = {desplazamiento:.4f} m")


def mostrarSumaVectores(vectorA, vectorB, suma):
    print(f"\n  A + B = {formatearVector(vectorA)} + {formatearVector(vectorB)} = {formatearVector(suma)}")


def mostrarProductoEscalar(vectorA, vectorB, producto, angulo):
    print(f"\n  A . B = {producto:.4f}")
    if angulo is None:
        print("  Ángulo: no definido (uno de los vectores es [0, 0]).")
    else:
        print(f"  Ángulo entre A y B: theta = {angulo:.4f} grados")


def mostrarProyectil(velocidadInicial, anguloGrados, alcance, alturaMaxima, tiempoVuelo):
    print(f"\n  v0 = {velocidadInicial:.4f} m/s,  theta = {anguloGrados:.4f} grados")
    print(f"  Alcance máximo:   R = {alcance:.4f} m")
    print(f"  Altura máxima:    H = {alturaMaxima:.4f} m")
    print(f"  Tiempo de vuelo:  t = {tiempoVuelo:.4f} s")


# =============================================================================
# Opciones del menú: leer -> calcular -> mostrar
# =============================================================================

def opcionCaidaLibre():
    print("\n--- 1. Caída libre ---")
    altura = leerNumero("Altura h [m] (>= 0): ", minimo=0)
    mostrarCaidaLibre(altura, calcularTiempoCaida(altura))


def opcionConversion():
    print("\n--- 2. Conversión de velocidad ---")
    print("  a) km/h -> m/s")
    print("  b) m/s  -> km/h")
    tipo = "kmh_a_ms" if leerOpcion("Tipo de conversión (a/b): ", ["a", "b"]) == "a" else "ms_a_kmh"
    velocidad = leerNumero("Rapidez (>= 0): ", minimo=0)
    mostrarConversion(velocidad, convertirVelocidad(velocidad, tipo), tipo)


def opcionDesplazamiento():
    print("\n--- 3. Desplazamiento en MRUA ---")
    velocidadInicial = leerNumero("Velocidad inicial u [m/s]: ")
    aceleracion = leerNumero("Aceleración a [m/s^2]: ")
    tiempo = leerNumero("Tiempo t [s] (>= 0): ", minimo=0)
    desplazamiento = calcularDesplazamiento(velocidadInicial, aceleracion, tiempo)
    mostrarDesplazamiento(velocidadInicial, aceleracion, tiempo, desplazamiento)


def opcionSumaVectores():
    print("\n--- 4. Suma de vectores ---")
    vectorA = leerVector("A")
    vectorB = leerVector("B")
    mostrarSumaVectores(vectorA, vectorB, sumarVectores(vectorA, vectorB))


def opcionProductoEscalar():
    print("\n--- 5. Producto escalar y ángulo ---")
    vectorA = leerVector("A")
    vectorB = leerVector("B")
    producto = calcularProductoEscalar(vectorA, vectorB)
    try:
        angulo = calcularAnguloEntreVectores(vectorA, vectorB)
    except ValueError:
        angulo = None  # el producto sí existe, pero el ángulo no está definido
    mostrarProductoEscalar(vectorA, vectorB, producto, angulo)


def opcionProyectil():
    print("\n--- 6. Lanzamiento de proyectil ---")
    velocidadInicial = leerNumero("Velocidad inicial v0 [m/s] (>= 0): ", minimo=0)
    anguloGrados = leerNumero("Ángulo theta [grados] (0 a 90): ", minimo=0, maximo=90)
    alcance, alturaMaxima, tiempoVuelo = calcularProyectil(velocidadInicial, anguloGrados)
    mostrarProyectil(velocidadInicial, anguloGrados, alcance, alturaMaxima, tiempoVuelo)


# =============================================================================
# Menú principal
# =============================================================================

OPCIONES = {
    "1": ("Caída libre", opcionCaidaLibre),
    "2": ("Conversión de velocidad (km/h <-> m/s)", opcionConversion),
    "3": ("Desplazamiento en MRUA", opcionDesplazamiento),
    "4": ("Suma de vectores", opcionSumaVectores),
    "5": ("Producto escalar y ángulo entre vectores", opcionProductoEscalar),
    "6": ("Lanzamiento de proyectil", opcionProyectil),
    "7": ("Salir", None),
}


def mostrarMenu():
    print("\n" + "=" * 50)
    print("  TALLER 1 · FÍSICA COMPUTACIONAL EN PYTHON")
    print("=" * 50)
    for clave, (descripcion, _) in OPCIONES.items():
        print(f"  {clave}. {descripcion}")


def menuPrincipal():
    while True:
        mostrarMenu()
        opcion = leerOpcion("Elige una opción (1-7): ", list(OPCIONES))
        if opcion == "7":
            print("\n¡Hasta luego!")
            break
        OPCIONES[opcion][1]()  # ejecuta la función asociada a la opción


if __name__ == "__main__":
    try:
        menuPrincipal()
    except (KeyboardInterrupt, EOFError):
        print("\n\nPrograma interrumpido. ¡Hasta luego!")
