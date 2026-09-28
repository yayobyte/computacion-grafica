"""
Taller 2 - Programación en Python (subrutinas, estructuras de control, arreglos y listas).

Menú interactivo que integra los 10 ejercicios del taller y una opción 11 para salir.
El código se organiza en cuatro capas, cada función con una sola responsabilidad:
    1. LECTURA:  leer...()    pide datos al usuario y los valida (repite si son inválidos).
    2. LÓGICA:   funciones puras de cada ejercicio; no leen ni imprimen, solo retornan.
    3. OPCIONES: opcion...()  une lectura -> lógica -> impresión para cada punto del menú.
    4. MENÚ:     menuPrincipal() con un diccionario que asocia cada número a su opción.

-------------------------------------------------------------------------------
ANÁLISIS: ENTRADAS, PROCESOS Y SALIDAS
-------------------------------------------------------------------------------
Op. | Entradas                     | Proceso                                | Salida
----+------------------------------+----------------------------------------+---------------------
 1  | a, b (reales), operación     | if/elif elige sumar/restar/...         | resultado real
 2  | lista de enteros             | for + if (n % 2 == 0)                  | lista de pares
 3  | lista de temperaturas [°C]   | map + lambda: F = C * 9/5 + 32         | lista en °F
 4  | lista de notas (0 a 100)     | for + if/elif por rangos               | lista de letras
 5  | texto                        | minúsculas, quitar puntuación, for     | diccionario {palabra: conteo}
 6  | lista, elemento a buscar     | for con índice, sin .index()           | índice o -1
 7  | cadena de ( y )              | for + contador de abiertos             | True / False
 8  | lista de (nombre, edad)      | sorted con key = (edad, nombre)        | lista ordenada
 9  | longitud (entero >= 4)       | una de cada tipo + relleno + mezcla    | contraseña
10  | acciones sobre la agenda     | diccionario {nombre: teléfono}         | mensajes y listado

-------------------------------------------------------------------------------
DECISIONES Y SUPUESTOS
-------------------------------------------------------------------------------
- Calificaciones en escala 0 a 100: A >= 90, B >= 80, C >= 70, D >= 60, F < 60.
- Temperaturas: no se aceptan valores menores que el cero absoluto (-273.15 °C).
- Paridad: solo se define para enteros, así que la opción 2 no acepta decimales.
- Paréntesis: la cadena solo puede tener '(' y ')'. La cadena vacía se considera válida.
- Ordenamiento: los nombres se comparan sin distinguir mayúsculas ("ana" = "Ana").
- Contraseña: mínimo 4 caracteres, para garantizar al menos una mayúscula, una
  minúscula, un número y un símbolo. Se usa el módulo 'secrets' (aleatoriedad segura)
  en lugar de 'random', que no es apto para contraseñas.
- Agenda: vive en memoria mientras el programa está abierto. Los nombres no se repiten
  (sin distinguir mayúsculas). El teléfono debe tener entre 7 y 15 dígitos y puede
  incluir '+', espacios o guiones.

-------------------------------------------------------------------------------
FALLOS QUE DETECTAN LAS PRUEBAS Y CÓMO SE EVITAN
-------------------------------------------------------------------------------
- Conteo de palabras: string.punctuation no incluye los signos del español
  (¿ ¡ « »). Sin ellos, "¿Cómo" se contaría como palabra distinta de "cómo".
  Corrección: se agregaron esos signos a PUNTUACION.
- Paréntesis: comparar solo el total de abiertos y cerrados aceptaría "())(" como
  válido (2 y 2). Corrección: si el contador baja de 0 en algún momento, la
  secuencia es inválida de inmediato.

-------------------------------------------------------------------------------
CONCLUSIÓN
-------------------------------------------------------------------------------
Separar lectura, lógica y menú permitió probar cada ejercicio por separado y
encontrar errores que un caso normal no revela. Los casos límite, como la lista vacía, los bordes de las notas o "())(",
fueron los que más aportaron.

Herramientas: Python 3 (biblioteca estándar: secrets, string).
Asistencia de IA: Claude OPUS 5.5 (Anthropic).
"""

import secrets
import string

CERO_ABSOLUTO_C = -273.15  # temperatura mínima posible [°C]
PUNTUACION = string.punctuation + "¿¡«»“”‘’…"  # signos a ignorar al contar palabras
SIMBOLOS_CONTRASENA = "!@#$%&*?-_+="


# =============================================================================
# 1. LECTURA Y VALIDACIÓN DE DATOS
# =============================================================================

def convertirNumero(texto, soloEnteros=False):
    """Convierte texto a int o float (acepta coma decimal). Lanza ValueError si no es válido."""
    texto = texto.strip().replace(",", ".")
    if soloEnteros:
        return int(texto)
    return float(texto)


def leerNumero(mensaje, soloEnteros=False, minimo=None, maximo=None):
    """Pide un número hasta que sea válido y esté dentro de [minimo, maximo]."""
    while True:
        try:
            valor = convertirNumero(input(mensaje), soloEnteros)
        except ValueError:
            print("  ✗ Debe ser un número" + (" entero." if soloEnteros else "."))
            continue
        if minimo is not None and valor < minimo:
            print(f"  ✗ El valor no puede ser menor que {minimo}.")
        elif maximo is not None and valor > maximo:
            print(f"  ✗ El valor no puede ser mayor que {maximo}.")
        else:
            return valor


def leerListaNumeros(mensaje, soloEnteros=False, minimo=None, maximo=None):
    """Pide números separados por espacios o ';' y retorna la lista. Vacío = lista vacía."""
    while True:
        texto = input(mensaje + "\n  (separados por espacios; Enter vacío = lista vacía): ")
        partes = texto.replace(";", " ").split()
        try:
            lista = [convertirNumero(parte, soloEnteros) for parte in partes]
        except ValueError:
            print("  ✗ Todos los valores deben ser números" + (" enteros." if soloEnteros else "."))
            continue
        fueraDeRango = [n for n in lista
                        if (minimo is not None and n < minimo) or (maximo is not None and n > maximo)]
        if fueraDeRango:
            rango = f"por debajo del mínimo {minimo}" if maximo is None else f"fuera del rango [{minimo}, {maximo}]"
            print(f"  ✗ Valores {rango}: {fueraDeRango}")
            continue
        return lista


def leerTexto(mensaje, permitirVacio=False):
    """Pide un texto; si permitirVacio es False, insiste hasta que no esté vacío."""
    while True:
        texto = input(mensaje).strip()
        if texto or permitirVacio:
            return texto
        print("  ✗ El texto no puede estar vacío.")


def leerOpcion(mensaje, opcionesValidas):
    """Pide una opción hasta que el usuario escriba una de opcionesValidas."""
    while True:
        opcion = input(mensaje).strip().lower()
        if opcion in opcionesValidas:
            return opcion
        print(f"  ✗ Opción no válida. Elige entre: {', '.join(opcionesValidas)}.")


# =============================================================================
# 2. LÓGICA DE CADA EJERCICIO (funciones puras: no leen ni imprimen)
# =============================================================================

# --- Punto 1: calculadora ---------------------------------------------------

def sumar(a, b):
    return a + b


def restar(a, b):
    return a - b


def multiplicar(a, b):
    return a * b


def dividir(a, b):
    if b == 0:
        raise ValueError("No se puede dividir por cero.")
    return a / b


OPERACIONES = {"+": sumar, "-": restar, "*": multiplicar, "/": dividir}


def calcular(a, b, operador):
    """Aplica la operación indicada por el operador (+, -, *, /) a los números a y b."""
    if operador not in OPERACIONES:
        raise ValueError(f"Operación desconocida: {operador}")
    return OPERACIONES[operador](a, b)


# --- Punto 2: filtrado de pares ---------------------------------------------

def filtrarPares(numeros):
    """Retorna una lista nueva con los números pares de 'numeros' (bucle + condicional)."""
    pares = []
    for numero in numeros:
        if numero % 2 == 0:
            pares.append(numero)
    return pares


# --- Punto 3: Celsius a Fahrenheit con map y lambda -------------------------

def celsiusAFahrenheit(temperaturasC):
    """Convierte una lista de temperaturas [°C] a [°F] con map + lambda: F = C * 9/5 + 32."""
    for temperatura in temperaturasC:
        if temperatura < CERO_ABSOLUTO_C:
            raise ValueError(f"{temperatura} °C está por debajo del cero absoluto.")
    return list(map(lambda c: round(c * 9 / 5 + 32, 2), temperaturasC))


# --- Punto 4: calificaciones a letras ---------------------------------------

def notaALetra(nota):
    """Convierte una nota de 0 a 100 a letra: A >= 90, B >= 80, C >= 70, D >= 60, F < 60."""
    if not 0 <= nota <= 100:
        raise ValueError(f"La nota {nota} está fuera del rango 0 a 100.")
    if nota >= 90:
        return "A"
    elif nota >= 80:
        return "B"
    elif nota >= 70:
        return "C"
    elif nota >= 60:
        return "D"
    else:
        return "F"


def calificacionesALetras(notas):
    """Retorna la lista de letras correspondiente a la lista de notas."""
    return [notaALetra(nota) for nota in notas]


# --- Punto 5: conteo de palabras --------------------------------------------

def contarPalabras(texto):
    """Retorna {palabra: veces}, ignorando mayúsculas y signos de puntuación."""
    textoLimpio = texto.lower()
    for signo in PUNTUACION:
        textoLimpio = textoLimpio.replace(signo, " ")
    conteo = {}
    for palabra in textoLimpio.split():
        conteo[palabra] = conteo.get(palabra, 0) + 1
    return conteo


# --- Punto 6: búsqueda sin .index() -----------------------------------------

def buscarElemento(lista, elemento):
    """Retorna el índice de la primera aparición de 'elemento' en 'lista', o -1."""
    for indice in range(len(lista)):
        if lista[indice] == elemento:
            return indice
    return -1


# --- Punto 7: validación de paréntesis --------------------------------------

def validarParentesis(cadena):
    """True si cada '(' tiene su ')' correspondiente y en el orden correcto."""
    abiertos = 0
    for caracter in cadena:
        if caracter == "(":
            abiertos += 1
        elif caracter == ")":
            abiertos -= 1
            if abiertos < 0:  # se cerró uno que nunca se abrió, ej. "())("
                return False
        else:
            raise ValueError(f"Carácter no permitido: '{caracter}'. Solo se aceptan ( y ).")
    return abiertos == 0


# --- Punto 8: ordenamiento personalizado ------------------------------------

def ordenarPorEdadYNombre(personas):
    """Ordena tuplas (nombre, edad) por edad y luego por nombre, ambos ascendentes."""
    return sorted(personas, key=lambda persona: (persona[1], persona[0].lower()))


# --- Punto 9: generador de contraseñas --------------------------------------

def generarContrasena(longitud):
    """Contraseña aleatoria con al menos una mayúscula, una minúscula, un número y un símbolo."""
    grupos = [string.ascii_uppercase, string.ascii_lowercase, string.digits, SIMBOLOS_CONTRASENA]
    if longitud < len(grupos):
        raise ValueError(f"La longitud mínima es {len(grupos)} (uno de cada tipo).")
    caracteres = [secrets.choice(grupo) for grupo in grupos]  # garantiza cada tipo
    todos = "".join(grupos)
    while len(caracteres) < longitud:
        caracteres.append(secrets.choice(todos))
    secrets.SystemRandom().shuffle(caracteres)  # que los 4 garantizados no queden al inicio
    return "".join(caracteres)


# --- Punto 10: agenda telefónica --------------------------------------------

def validarTelefono(telefono):
    """True si el teléfono tiene de 7 a 15 dígitos y solo usa dígitos, '+', espacios o '-'."""
    permitidos = set(string.digits + "+- ")
    cantidadDigitos = sum(1 for c in telefono if c.isdigit())
    return set(telefono) <= permitidos and 7 <= cantidadDigitos <= 15


def buscarClave(agenda, nombre):
    """Retorna la clave real de 'nombre' en la agenda (sin distinguir mayúsculas), o None."""
    for clave in agenda:
        if clave.lower() == nombre.lower():
            return clave
    return None


def agregarContacto(agenda, nombre, telefono):
    """Agrega el contacto. Lanza ValueError si ya existe o si el teléfono es inválido."""
    if buscarClave(agenda, nombre) is not None:
        raise ValueError(f"Ya existe un contacto llamado '{nombre}'.")
    if not validarTelefono(telefono):
        raise ValueError("Teléfono inválido: usa de 7 a 15 dígitos (se permiten +, espacios y -).")
    agenda[nombre] = telefono


def buscarContacto(agenda, nombre):
    """Retorna (nombre, teléfono) si existe, o None."""
    clave = buscarClave(agenda, nombre)
    return None if clave is None else (clave, agenda[clave])


def eliminarContacto(agenda, nombre):
    """Elimina el contacto y retorna True; retorna False si no existía."""
    clave = buscarClave(agenda, nombre)
    if clave is None:
        return False
    del agenda[clave]
    return True


def listarContactos(agenda):
    """Retorna la lista de (nombre, teléfono) ordenada alfabéticamente."""
    return sorted(agenda.items(), key=lambda contacto: contacto[0].lower())


# =============================================================================
# 3. OPCIONES DEL MENÚ: leer -> procesar -> mostrar
# =============================================================================

def opcionCalculadora():
    print("\n--- 1. Calculadora básica ---")
    a = leerNumero("Primer número: ")
    b = leerNumero("Segundo número: ")
    operador = leerOpcion("Operación (+, -, *, /): ", list(OPERACIONES))
    try:
        print(f"\n  {a} {operador} {b} = {calcular(a, b, operador)}")
    except ValueError as error:
        print(f"\n  ✗ {error}")


def opcionFiltrarPares():
    print("\n--- 2. Filtrado de números pares ---")
    numeros = leerListaNumeros("Lista de enteros", soloEnteros=True)
    print(f"\n  Lista original: {numeros}")
    print(f"  Números pares:  {filtrarPares(numeros)}")


def opcionTemperaturas():
    print("\n--- 3. Celsius a Fahrenheit (map + lambda) ---")
    temperaturas = leerListaNumeros("Temperaturas en °C", minimo=CERO_ABSOLUTO_C)
    for celsius, fahrenheit in zip(temperaturas, celsiusAFahrenheit(temperaturas)):
        print(f"  {celsius:>8.2f} °C = {fahrenheit:>8.2f} °F")


def opcionCalificaciones():
    print("\n--- 4. Calificaciones a letras (escala 0 a 100) ---")
    notas = leerListaNumeros("Notas", minimo=0, maximo=100)
    for nota, letra in zip(notas, calificacionesALetras(notas)):
        print(f"  {nota:>6.1f} -> {letra}")


def opcionContarPalabras():
    print("\n--- 5. Conteo de palabras ---")
    conteo = contarPalabras(leerTexto("Texto: ", permitirVacio=True))
    if not conteo:
        print("\n  El texto no contiene palabras.")
    for palabra, veces in sorted(conteo.items(), key=lambda par: (-par[1], par[0])):
        print(f"  {palabra:<15} {veces}")


def opcionBuscar():
    print("\n--- 6. Búsqueda de elemento en lista ---")
    texto = input("Elementos de la lista (separados por espacios): ")
    lista = texto.split()
    elemento = leerTexto("Elemento a buscar: ")
    indice = buscarElemento(lista, elemento)
    if indice == -1:
        print(f"\n  '{elemento}' no está en la lista -> -1")
    else:
        print(f"\n  '{elemento}' está en el índice {indice}")


def opcionParentesis():
    print("\n--- 7. Validación de paréntesis ---")
    while True:
        cadena = input("Secuencia de paréntesis (solo ( y )): ").replace(" ", "")
        try:
            valida = validarParentesis(cadena)
            break
        except ValueError as error:
            print(f"  ✗ {error}")
    print(f"\n  '{cadena}' es {'VÁLIDA' if valida else 'INVÁLIDA'}")


def opcionOrdenar():
    print("\n--- 8. Ordenamiento por edad y nombre ---")
    cantidad = leerNumero("¿Cuántas personas? ", soloEnteros=True, minimo=1, maximo=50)
    personas = []
    for i in range(cantidad):
        nombre = leerTexto(f"  Nombre {i + 1}: ")
        edad = leerNumero(f"  Edad de {nombre} [años]: ", soloEnteros=True, minimo=0, maximo=150)
        personas.append((nombre, edad))
    print("\n  Ordenado (edad, luego nombre):")
    for nombre, edad in ordenarPorEdadYNombre(personas):
        print(f"    {edad:>3} años  {nombre}")


def opcionContrasena():
    print("\n--- 9. Generador de contraseñas ---")
    longitud = leerNumero("Longitud (4 a 64): ", soloEnteros=True, minimo=4, maximo=64)
    print(f"\n  Contraseña: {generarContrasena(longitud)}")


def opcionAgenda(agenda):
    """Submenú de la agenda. Recibe el diccionario para que los contactos se conserven."""
    while True:
        print("\n--- 10. Agenda telefónica ---")
        print("  a) Agregar   b) Buscar   c) Eliminar   d) Mostrar todos   e) Volver")
        accion = leerOpcion("Acción: ", ["a", "b", "c", "d", "e"])
        if accion == "a":
            nombre = leerTexto("  Nombre: ")
            telefono = leerTexto("  Teléfono: ")
            try:
                agregarContacto(agenda, nombre, telefono)
                print(f"  ✓ '{nombre}' agregado.")
            except ValueError as error:
                print(f"  ✗ {error}")
        elif accion == "b":
            encontrado = buscarContacto(agenda, leerTexto("  Nombre a buscar: "))
            print(f"  ✓ {encontrado[0]}: {encontrado[1]}" if encontrado else "  ✗ No encontrado.")
        elif accion == "c":
            nombre = leerTexto("  Nombre a eliminar: ")
            print("  ✓ Eliminado." if eliminarContacto(agenda, nombre) else "  ✗ No encontrado.")
        elif accion == "d":
            contactos = listarContactos(agenda)
            if not contactos:
                print("  (La agenda está vacía)")
            for nombre, telefono in contactos:
                print(f"  {nombre:<20} {telefono}")
        else:
            return


# =============================================================================
# 4. MENÚ PRINCIPAL
# =============================================================================

OPCIONES = {
    "1": "Operaciones básicas (calculadora)",
    "2": "Filtrado de lista por números pares",
    "3": "Conversión de temperaturas de Celsius a Fahrenheit",
    "4": "Sistema de calificaciones a letras",
    "5": "Conteo de palabras en una cadena",
    "6": "Búsqueda de elemento en lista",
    "7": "Validación de secuencia de paréntesis",
    "8": "Ordenamiento personalizado de lista de tuplas",
    "9": "Generador de contraseñas aleatorias",
    "10": "Gestión de agenda telefónica",
    "11": "Salir del programa",
}


def mostrarMenu():
    print("\n" + "=" * 55)
    print("  TALLER 2 · CONTROL, LISTAS Y FUNCIONES EN PYTHON")
    print("=" * 55)
    for clave, descripcion in OPCIONES.items():
        print(f"  {clave:>2}. {descripcion}")


def menuPrincipal():
    agenda = {}  # se crea una vez para que los contactos duren toda la sesión
    acciones = {
        "1": opcionCalculadora, "2": opcionFiltrarPares, "3": opcionTemperaturas,
        "4": opcionCalificaciones, "5": opcionContarPalabras, "6": opcionBuscar,
        "7": opcionParentesis, "8": opcionOrdenar, "9": opcionContrasena,
        "10": lambda: opcionAgenda(agenda),
    }
    while True:
        mostrarMenu()
        opcion = leerOpcion("Elige una opción (1-11): ", list(OPCIONES))
        if opcion == "11":
            print("\n¡Hasta luego!")
            break
        acciones[opcion]()


if __name__ == "__main__":
    try:
        menuPrincipal()
    except (KeyboardInterrupt, EOFError):
        print("\n\nPrograma interrumpido. ¡Hasta luego!")
