# Taller 1\Ejercicio5.py
# Ejercicio 5: Cálculo del alcance horizontal de un proyectil
# 
# Descripción: Este programa calcula el alcance horizontal máximo de un proyectil
# lanzado con una velocidad inicial, un ángulo determinado y desde una altura inicial.
# Utiliza ecuaciones de movimiento parabólico y técnicas de álgebra lineal.

import numpy as np

def calcular_alcance_horizontal(velocidad_inicial, angulo, altura_inicial):
    """
    Calcula el alcance horizontal de un proyectil.
    
    Parámetros:
    velocidad_inicial : float
        Velocidad inicial del proyectil en m/s
    angulo : float
        Ángulo de lanzamiento en grados
    altura_inicial : float
        Altura inicial del proyectil en metros
    
    Retorna:
    float : Alcance horizontal en metros
    """
    g = 9.8  # Aceleración gravitatoria en m/s²
    
    # Convertir ángulo a radianes
    angulo_rad = np.radians(angulo)
    
    # Descomponemos la velocidad inicial en sus componentes
    v0_x = velocidad_inicial * np.cos(angulo_rad)
    v0_y = velocidad_inicial * np.sin(angulo_rad)
    
    # Para calcular el alcance horizontal, necesitamos encontrar el tiempo t
    # en que el proyectil toca el suelo (y = 0)
    # La ecuación es: 0 = altura_inicial + v0_y*t - 0.5*g*t^2
    
    # Coeficientes de la ecuación cuadrática a*t^2 + b*t + c = 0
    a = -0.5 * g
    b = v0_y
    c = altura_inicial
    
    # Resolvemos usando la forma matricial de una ecuación cuadrática
    # [a b c] @ [t^2 t 1]^T = 0
    coef = np.array([a, b, c])
    
    # Calculamos el discriminante
    discriminante = b**2 - 4*a*c
    
    if discriminante < 0:
        # No hay solución real, el proyectil nunca toca el suelo
        return float('inf')
    
    # Calculamos las raíces
    t1 = (-b + np.sqrt(discriminante)) / (2*a)
    t2 = (-b - np.sqrt(discriminante)) / (2*a)
    
    # El tiempo de vuelo es la raíz positiva más grande
    tiempo_vuelo = max(t for t in [t1, t2] if t > 0) if any(t > 0 for t in [t1, t2]) else 0
    
    # Calculamos el alcance horizontal usando x = v0_x * t
    alcance = v0_x * tiempo_vuelo
    
    return alcance

# Ejemplo de uso independiente
if __name__ == "__main__":
    velocidad = 30  # m/s
    angulo = 45     # grados
    altura = 0      # metros
    alcance = calcular_alcance_horizontal(velocidad, angulo, altura)
    print(f"Un proyectil lanzado a {velocidad} m/s con un ángulo de {angulo}° desde una altura de {altura} m alcanza un alcance horizontal de {alcance:.2f} metros.")