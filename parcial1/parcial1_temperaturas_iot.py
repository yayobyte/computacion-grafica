"""
Parcial 1 — Computación Gráfica (UTP)
Análisis de temperaturas en sensores IoT.

Propósito:
    Resolver, con NumPy y Matplotlib, el análisis de las temperaturas
    registradas por cuatro sensores de una planta industrial.

Datos:
    T[i][j] = temperatura del sensor i en el instante de tiempo j.
    T = [[32, 34, 33, 35],
         [28, 29, 30, 31],
         [40, 42, 41, 43],
         [25, 27, 26, 28]]

Herramientas / Asistencia de IA:
    Python 3 con NumPy y Matplotlib. Documentación y revisión asistidas por IA.
"""

import numpy as np
import matplotlib.pyplot as plt


def crearMatrizTemperaturas():
    """
    Crea y retorna la matriz de temperaturas del sistema de sensores.

    Cada fila representa un sensor (S1, S2, S3, S4) y cada columna un
    instante de tiempo (t1, t2, t3, t4).

    Retorna:
        np.ndarray: matriz de forma (4, 4) con las temperaturas en °C.
    """
    matriz_temperaturas = np.array([
        [32, 34, 33, 35],
        [28, 29, 30, 31],
        [40, 42, 41, 43],
        [25, 27, 26, 28],
    ])
    return matriz_temperaturas


def mostrarMatrizTemperaturas(matriz_temperaturas):
    """
    Imprime en pantalla la matriz de temperaturas.

    Parámetros:
        matriz_temperaturas (np.ndarray): matriz de temperaturas (4, 4).
    """
    print("Matriz de temperaturas (°C) — filas: sensores, columnas: instantes")
    print(matriz_temperaturas)


def calcularPromedioPorSensor(matriz_temperaturas):
    """
    Calcula la temperatura promedio registrada por cada sensor.

    Se promedia a lo largo de las columnas (axis=1), de modo que cada
    valor corresponde a un sensor (fila).

    Parámetros:
        matriz_temperaturas (np.ndarray): matriz de temperaturas (4, 4).

    Retorna:
        np.ndarray: vector con el promedio de cada sensor (4,).
    """
    promedio_sensor = np.mean(matriz_temperaturas, axis=1)
    return promedio_sensor


def calcularMaximoPorSensor(matriz_temperaturas):
    """
    Calcula la temperatura máxima registrada por cada sensor.

    Parámetros:
        matriz_temperaturas (np.ndarray): matriz de temperaturas (4, 4).

    Retorna:
        np.ndarray: vector con la temperatura máxima de cada sensor (4,).
    """
    temperatura_maxima = np.max(matriz_temperaturas, axis=1)
    return temperatura_maxima


def determinarSensorMayorPromedio(promedio_sensor):
    """
    Determina el índice del sensor con la mayor temperatura promedio.

    Parámetros:
        promedio_sensor (np.ndarray): promedio de temperatura de cada sensor.

    Retorna:
        int: índice (base 0) del sensor con mayor promedio.
    """
    indice_sensor = int(np.argmax(promedio_sensor))
    return indice_sensor


def mostrarAnalisisPorSensor(promedio_sensor, temperatura_maxima,
                             indice_sensor):
    """
    Imprime el promedio y el máximo por sensor y el sensor más caliente.

    Parámetros:
        promedio_sensor (np.ndarray): promedio de temperatura de cada sensor.
        temperatura_maxima (np.ndarray): máxima temperatura de cada sensor.
        indice_sensor (int): sensor con la mayor temperatura promedio.
    """
    print("Análisis de temperaturas por sensor:")
    for i in range(len(promedio_sensor)):
        print(f"  S{i + 1}: promedio = {promedio_sensor[i]:.2f} °C, "
              f"máxima = {temperatura_maxima[i]:.0f} °C")
    print()
    print(f"El sensor con mayor temperatura promedio es S{indice_sensor + 1} "
          f"({promedio_sensor[indice_sensor]:.2f} °C).")


def calcularMaximoGlobal(matriz_temperaturas):
    """
    Encuentra la temperatura máxima de toda la matriz.

    Parámetros:
        matriz_temperaturas (np.ndarray): matriz de temperaturas (4, 4).

    Retorna:
        float: temperatura máxima registrada en el sistema.
    """
    temperatura_maxima = float(np.max(matriz_temperaturas))
    return temperatura_maxima


def calcularMinimoGlobal(matriz_temperaturas):
    """
    Encuentra la temperatura mínima de toda la matriz.

    Parámetros:
        matriz_temperaturas (np.ndarray): matriz de temperaturas (4, 4).

    Retorna:
        float: temperatura mínima registrada en el sistema.
    """
    temperatura_minima = float(np.min(matriz_temperaturas))
    return temperatura_minima


def calcularPromedioGlobal(matriz_temperaturas):
    """
    Calcula la temperatura promedio general del sistema.

    Parámetros:
        matriz_temperaturas (np.ndarray): matriz de temperaturas (4, 4).

    Retorna:
        float: promedio de todas las temperaturas registradas.
    """
    promedio_general = float(np.mean(matriz_temperaturas))
    return promedio_general


def mostrarEstadisticasGlobales(temperatura_maxima, temperatura_minima,
                                promedio_general):
    """
    Imprime las estadísticas globales del sistema de sensores.

    Parámetros:
        temperatura_maxima (float): máxima temperatura del sistema.
        temperatura_minima (float): mínima temperatura del sistema.
        promedio_general (float): promedio general del sistema.
    """
    print("Estadísticas globales del sistema:")
    print(f"  Temperatura máxima: {temperatura_maxima:.2f} °C")
    print(f"  Temperatura mínima: {temperatura_minima:.2f} °C")
    print(f"  Temperatura promedio general: {promedio_general:.2f} °C")


def graficarPromedioPorSensor(promedio_sensor):
    """
    Genera un gráfico de barras con la temperatura promedio de cada sensor.

    Parámetros:
        promedio_sensor (np.ndarray): promedio de temperatura de cada sensor.
    """
    etiquetas_sensores = ["S1", "S2", "S3", "S4"]
    plt.figure(figsize=(7, 4.5))
    plt.bar(etiquetas_sensores, promedio_sensor, color="steelblue")
    plt.title("Temperatura promedio por sensor")
    plt.xlabel("Sensor")
    plt.ylabel("Temperatura promedio (°C)")
    plt.grid(axis="y", linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.show()


def graficarTemperaturaSensor3(temperaturas_sensor_3, instantes_tiempo):
    """
    Genera un gráfico de líneas con la evolución térmica del sensor 3.

    Parámetros:
        temperaturas_sensor_3 (list): temperaturas del sensor 3 por instante.
        instantes_tiempo (list): etiquetas de los instantes de tiempo.
    """
    plt.figure(figsize=(7, 4.5))
    plt.plot(instantes_tiempo, temperaturas_sensor_3, marker="o",
             color="darkorange", linewidth=2)
    plt.title("Evolución de la temperatura del sensor 3")
    plt.xlabel("Instante de tiempo")
    plt.ylabel("Temperatura (°C)")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.show()


def main():
    matriz_temperaturas = crearMatrizTemperaturas()
    mostrarMatrizTemperaturas(matriz_temperaturas)
    print()
    print("Interpretación:")
    print("  - Cada fila es un sensor: S1, S2, S3 y S4.")
    print("  - Cada columna es un instante de tiempo: t1, t2, t3 y t4.")
    print("  - T[i][j] es la temperatura del sensor i en el instante j.")
    print()

    promedio_sensor = calcularPromedioPorSensor(matriz_temperaturas)
    temperatura_maxima = calcularMaximoPorSensor(matriz_temperaturas)
    indice_sensor = determinarSensorMayorPromedio(promedio_sensor)
    mostrarAnalisisPorSensor(promedio_sensor, temperatura_maxima,
                             indice_sensor)
    print()
    print("Interpretación:")
    print("  El sensor S3 opera a la temperatura promedio más alta, por")
    print("  lo que su zona de producción es la más crítica y debe")
    print("  priorizarse en el monitoreo para evitar sobrecalentamientos.")
    print()

    temperatura_maxima = calcularMaximoGlobal(matriz_temperaturas)
    temperatura_minima = calcularMinimoGlobal(matriz_temperaturas)
    promedio_general = calcularPromedioGlobal(matriz_temperaturas)
    mostrarEstadisticasGlobales(temperatura_maxima, temperatura_minima,
                                promedio_general)
    print()
    print("Interpretación:")
    print("  El máximo (43 °C) marca el pico térmico alcanzado por algún")
    print("  sensor; el mínimo (25 °C) indica la zona más fría. El promedio")
    print("  general (32.75 °C) resume el comportamiento térmico del sistema.")
    print()

    graficarPromedioPorSensor(promedio_sensor)

    temperaturas_sensor_3 = [40, 42, 41, 43]
    instantes_tiempo = ["t1", "t2", "t3", "t4"]
    graficarTemperaturaSensor3(temperaturas_sensor_3, instantes_tiempo)
    print("Interpretación:")
    print("  El gráfico muestra que el sensor 3 se mantiene entre 40 y 43 °C")
    print("  con una tendencia leve al aumento, lo que permite al ingeniero")
    print("  detectar si la zona se está calentando y anticipar acciones de")
    print("  control antes de que se superen los límites operativos.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nEjecución interrumpida por el usuario.")
