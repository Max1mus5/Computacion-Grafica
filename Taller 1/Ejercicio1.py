# Taller 1\Ejercicio1.py
# Ejercicio 1: Cálculo de posición y velocidad en caída libre
# 
# Descripción: Este programa calcula y visualiza la posición y velocidad
# de un objeto en caída libre a partir de una altura inicial, durante
# un intervalo de tiempo específico.
# Utiliza NumPy para realizar cálculos matriciales y matplotlib para
# visualizar los resultados.

import numpy as np
import matplotlib.pyplot as plt

def calcular_caida_libre(altura_inicial, tiempo_total, pasos):
    """
    Calcula la posición y velocidad de un objeto en caída libre.
    
    Parámetros:
    altura_inicial : float
        Altura inicial del objeto en metros
    tiempo_total : float
        Tiempo total de caída en segundos
    pasos : int
        Número de pasos para discretizar el tiempo
    
    Retorna:
    None (Muestra gráficos con los resultados)
    """
    g = 9.8  # Aceleración gravitatoria en m/s²
    
    # Crear vector de tiempo
    t = np.linspace(0, tiempo_total, pasos)
    
    # Crear matriz de transformación para el sistema de ecuaciones
    # Para cada tiempo t, calculamos [y, v] = [y0, v0] + [v0*t - 0.5*g*t^2, -g*t]
    y0 = np.array([altura_inicial, 0])  # Estado inicial [posición, velocidad]
    
    # Creamos matrices para almacenar resultados
    resultados = np.zeros((pasos, 2))
    
    # Aplicamos las ecuaciones de caída libre usando álgebra matricial
    for i, tiempo in enumerate(t):
        # Matriz de transformación para este paso de tiempo
        A = np.array([
            [1, tiempo],
            [0, 1]
        ])
        
        # Vector de efecto gravitatorio
        b = np.array([-0.5 * g * tiempo**2, -g * tiempo])
        
        # Calculamos el nuevo estado
        nuevo_estado = A @ y0 + b
        resultados[i] = nuevo_estado
    
    # Detectar cuándo el objeto toca el suelo (y ≤ 0)
    impacto_idx = np.where(resultados[:, 0] <= 0)[0]
    if len(impacto_idx) > 0:
        primer_impacto = impacto_idx[0]
        tiempo_impacto = t[primer_impacto]
        velocidad_impacto = resultados[primer_impacto, 1]
        
        # Truncar resultados en el punto de impacto
        t = t[:primer_impacto+1]
        resultados = resultados[:primer_impacto+1]
        
        print(f"¡Impacto con el suelo!")
        print(f"Tiempo de impacto: {tiempo_impacto:.2f} segundos")
        print(f"Velocidad de impacto: {abs(velocidad_impacto):.2f} m/s")
    
    # Visualizar resultados
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    # Gráfico de posición vs tiempo
    ax1.plot(t, resultados[:, 0], 'b-', linewidth=2)
    ax1.set_xlabel('Tiempo (s)')
    ax1.set_ylabel('Altura (m)')
    ax1.set_title('Posición vs Tiempo en Caída Libre')
    ax1.grid(True)
    
    # Gráfico de velocidad vs tiempo
    ax2.plot(t, resultados[:, 1], 'r-', linewidth=2)
    ax2.set_xlabel('Tiempo (s)')
    ax2.set_ylabel('Velocidad (m/s)')
    ax2.set_title('Velocidad vs Tiempo en Caída Libre')
    ax2.grid(True)
    
    plt.tight_layout()
    plt.show()

# Ejemplo de uso independiente
if __name__ == "__main__":
    calcular_caida_libre(100, 5, 100)