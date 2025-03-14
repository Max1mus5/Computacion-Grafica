# Taller 1\Ejercicio3.py
# Ejercicio 3: Cálculo de altura máxima de un proyectil
# 
# Descripción: Este programa calcula la altura máxima que alcanza un proyectil
# lanzado con una velocidad inicial y un ángulo determinado.
# Utiliza las ecuaciones de movimiento parabólico y álgebra lineal para
# resolver el problema.

import numpy as np

def calcular_altura_maxima(velocidad_inicial, angulo):
    """
    Calcula la altura máxima alcanzada por un proyectil.
    
    Parámetros:
    velocidad_inicial : float
        Velocidad inicial del proyectil en m/s
    angulo : float
        Ángulo de lanzamiento en grados
    
    Retorna:
    float : Altura máxima en metros
    """
    g = 9.8  # Aceleración gravitatoria en m/s²
    
    # Convertir ángulo a radianes
    angulo_rad = np.radians(angulo)
    
    # Descomponemos la velocidad inicial en sus componentes
    v0 = np.array([
        velocidad_inicial * np.cos(angulo_rad),  # Componente horizontal
        velocidad_inicial * np.sin(angulo_rad)   # Componente vertical
    ])
    
    # La altura máxima se alcanza cuando la velocidad vertical es cero
    # Planteamos el problema usando álgebra lineal
    
    # Matriz de transformación para el sistema de ecuaciones
    # Dado que la velocidad vertical en la altura máxima es cero:
    # 0 = v0_y - g*t
    # Despejamos t: t = v0_y / g
    
    # Calculamos el tiempo hasta la altura máxima
    t_max = v0[1] / g
    
    # Calculamos la altura máxima usando la ecuación de movimiento vertical
    # y = v0_y*t - 0.5*g*t^2
    
    # Matriz de transformación para la posición
    A = np.array([
        [t_max],          # Coeficiente para v0_y
        [-0.5 * t_max**2] # Coeficiente para g
    ])
    
    # Vector de parámetros
    b = np.array([v0[1], g])
    
    # Calculamos la altura máxima
    altura_maxima = A.T @ b
    
    return float(altura_maxima)

# Ejemplo de uso independiente
if __name__ == "__main__":
    velocidad = 50  # m/s
    angulo = 45     # grados
    altura = calcular_altura_maxima(velocidad, angulo)
    print(f"Un proyectil lanzado a {velocidad} m/s con un ángulo de {angulo}° alcanza una altura máxima de {altura:.2f} metros.")