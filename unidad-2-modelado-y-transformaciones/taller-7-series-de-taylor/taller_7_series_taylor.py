"""
===============================================================================
UNIVERSIDAD TECNOLÓGICA DE PEREIRA (UTP)
Facultad de Ingenierías - Departamento de Sistemas
Curso: Computación Gráfica
Unidad 2: Modelado Numérico, Curvas y Transformaciones

Taller 7: Series de Taylor y Comparación Visual de Aproximaciones
Alineación: RAA1 (Modelación numérica), RAA5 (Análisis técnico), RAA6 (Autonomía)
Herramientas: Python 3, NumPy y Matplotlib
===============================================================================
"""

import math
import numpy as np
import matplotlib.pyplot as plt


# =============================================================================
# 1. FUNCIONES MATEMÁTICAS REUTILIZABLES
# =============================================================================

def mi_factorial(n: int) -> int:
    """
    Calcula el factorial de un número entero n no negativo de forma recursiva,
    conservando la estructura algorítmica vista en clase con validación.
    
    Parámetros:
        n (int): Entero no negativo.
        
    Retorna:
        int: n! (factorial de n).
    """
    if not isinstance(n, (int, np.integer)):
        raise TypeError("El factorial solo está definido para números enteros.")
    if n < 0:
        raise ValueError("El factorial no está definido para números negativos.")
    if n == 0 or n == 1:
        return 1
    return n * mi_factorial(n - 1)


def aproximacion_taylor_seno(x: np.ndarray, num_terminos: int) -> np.ndarray:
    """
    Calcula la aproximación por Serie de Taylor (Maclaurin, a=0) de la función seno:
        sen(x) ≈ sum_{k=0}^{num_terminos - 1} [ ((-1)^k / (2k + 1)!) * x^(2k + 1) ]
        
    Parámetros:
        x (np.ndarray o float): Valores de entrada en radianes.
        num_terminos (int): Número de términos acumulados en la serie polinómica (N >= 1).
        
    Retorna:
        np.ndarray: Valores evaluados del polinomio de Taylor de grado 2*(num_terminos) - 1.
    """
    if num_terminos < 1:
        raise ValueError("El número de términos debe ser al menos 1.")
    
    # Asegurar que la entrada sea tratada como un arreglo flotante de NumPy
    x_arr = np.asarray(x, dtype=np.float64)
    suma = np.zeros_like(x_arr)
    
    for k in range(num_terminos):
        potencia = 2 * k + 1
        coeficiente = ((-1) ** k) / mi_factorial(potencia)
        termino = coeficiente * (x_arr ** potencia)
        suma += termino
        
    return suma


def calcular_error_absoluto(y_real: np.ndarray, y_aprox: np.ndarray) -> np.ndarray:
    """
    Calcula el error absoluto punto a punto entre la función analítica y la aproximación:
        Error_Absoluto(x) = | y_real(x) - y_aprox(x) |
    """
    return np.abs(y_real - y_aprox)


# =============================================================================
# 2. DEFINICIÓN Y JUSTIFICACIÓN DEL DOMINIO
# =============================================================================
# JUSTIFICACIÓN TÉCNICA DEL DOMINIO:
# La función seno es periódica con período T = 2π rad (~6.2832 rad). Al expandir
# la serie alrededor de a = 0 (Maclaurin), la aproximación es asintóticamente
# exacta en el origen. Seleccionar el dominio simétrico [-2π, 2π] cubre dos
# oscilaciones completas. Esto permite evaluar no solo la precisión local
# cerca de x = 0, sino también la rápida divergencia polinómica a medida
# que |x| crece, permitiendo comparar el comportamiento entre aproximaciones
# de orden bajo y orden alto. Se generan 600 puntos uniformes con np.linspace
# para garantizar resolución continua y evitar sesgos de discretización.

x_inicio = -2 * np.pi
x_fin = 2 * np.pi
num_puntos = 600

x = np.linspace(x_inicio, x_fin, num_puntos)
y_real = np.sin(x)

# Lista configurable de número de términos a comparar (N >= 3)
terminos_a_evaluar = [1, 2, 3, 5, 7]
colores = ['#E63946', '#F4A261', '#2A9D8F', '#457B9D', '#9B5DE5']
estilos = ['--', '-.', ':', (0, (3, 1, 1, 1)), '-']


# =============================================================================
# 3. GENERACIÓN DE VISUALIZACIONES ROTULADAS Y ANÁLISIS DE ERROR
# =============================================================================

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 9), sharex=True)
fig.suptitle(
    "Taller 7: Series de Taylor para sen(x) y Evaluación del Error Absoluto",
    fontsize=14,
    fontweight='bold',
    y=0.96
)

# --- Subgráfica 1: Comparación de Aproximaciones vs Función Real ---
ax1.plot(
    x, y_real,
    label="sen(x) analítica (referencia)",
    color="#1D3557",
    linewidth=2.5,
    zorder=5
)

# Almacenar cálculos de error para resumen impreso
metricas_error = {}

for n_terms, color, estilo in zip(terminos_a_evaluar, colores, estilos):
    y_aprox = aproximacion_taylor_seno(x, n_terms)
    error_abs = calcular_error_absoluto(y_real, y_aprox)
    metricas_error[n_terms] = {
        'max': np.max(error_abs),
        'mean': np.mean(error_abs)
    }
    
    grado = 2 * n_terms - 1
    ax1.plot(
        x, y_aprox,
        label=f"Taylor N = {n_terms} térm. (grado {grado})",
        color=color,
        linestyle=estilo,
        linewidth=1.8,
        alpha=0.9
    )
    
    # --- Subgráfica 2: Representación del Error Absoluto ---
    ax2.plot(
        x, error_abs,
        label=f"Error N = {n_terms} térm. (máx: {metricas_error[n_terms]['max']:.2e})",
        color=color,
        linestyle=estilo,
        linewidth=1.8
    )

# Configuración estética y rotulación de la Subgráfica 1
ax1.set_ylabel("f(x)", fontsize=11, fontweight='semibold')
ax1.set_title("Aproximación Polinómica de Taylor vs. sen(x) Real", fontsize=12)
ax1.set_ylim(-2.5, 2.5)  # Trunca visualmente el escape al infinito para comparar el ajuste
ax1.axhline(0, color="gray", linestyle="--", linewidth=0.8, alpha=0.7)
ax1.axvline(0, color="gray", linestyle="--", linewidth=0.8, alpha=0.7)
ax1.grid(True, linestyle=":", alpha=0.6)
ax1.legend(loc="upper center", bbox_to_anchor=(0.5, -0.05), ncol=3, frameon=True)

# Configuración estética y rotulación de la Subgráfica 2
ax2.set_xlabel("x (radianes)", fontsize=11, fontweight='semibold')
ax2.set_ylabel("Error Absoluto |sen(x) - P_N(x)|", fontsize=11, fontweight='semibold')
ax2.set_title("Evolución del Error Absoluto a lo Largo del Dominio (Escala Logarítmica)", fontsize=12)
ax2.set_yscale('log')
ax2.set_ylim(1e-15, 1e4)
ax2.axvline(0, color="gray", linestyle="--", linewidth=0.8, alpha=0.7)
ax2.grid(True, which="both", linestyle=":", alpha=0.6)
ax2.legend(loc="lower left", fontsize=9, frameon=True)

plt.subplots_adjust(top=0.90, bottom=0.10, hspace=0.35)

# Reporte en consola de verificación numérica
print("=" * 68)
print("RESUMEN DE PRUEBAS NUMÉRICAS Y ERROR EN EL DOMINIO [-2π, 2π]:")
print("=" * 68)
print(f"{'Términos (N)':<15} {'Grado Polinomio':<18} {'Error Máximo':<18} {'Error Promedio':<18}")
print("-" * 68)
for n_terms in terminos_a_evaluar:
    grado = 2 * n_terms - 1
    emax = metricas_error[n_terms]['max']
    emean = metricas_error[n_terms]['mean']
    print(f"{n_terms:<15} {grado:<18} {emax:<18.4e} {emean:<18.4e}")
print("=" * 68)


if __name__ == "__main__":
    plt.show()


# =============================================================================
# CONCLUSIÓN TÉCNICA (Requisito: entre 5 y 8 líneas de análisis técnico)
# =============================================================================
"""
La serie de Taylor centrada en el origen exhibe convergencia uniforme y asintótica hacia sen(x).
Al incrementar el número de términos N, el polinomio extiende progresivamente el intervalo de
validez donde el error absoluto se aproxima a la precisión de máquina (~10^-16), reduciendo
drásticamente la discrepancia en el centro. Sin embargo, para cualquier N finito, al alejarse de
x = 0 el término dominante de mayor grado provoca una divergencia polinómica exponencial, lo que
hace crecer el error en los extremos del dominio [-2π, 2π]. Por consiguiente, la precisión en
computación gráfica no solo depende de la cantidad de términos evaluados, sino críticamente de la
cercanía al punto de expansión y del costo computacional de evaluar factoriales de alto orden.
"""
