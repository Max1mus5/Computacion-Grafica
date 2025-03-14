# Taller 1\Ejercicio6.py
# Ejercicio 6: Cálculo del ángulo óptimo para máximo alcance
# 
# Descripción: Este programa determina el ángulo óptimo de lanzamiento que
# maximiza el alcance horizontal de un proyectil para una velocidad inicial dada
# y una altura inicial determinada.
# Utiliza métodos numéricos y álgebra lineal para encontrar la solución.

import numpy as np
from Ejercicio5 import calcular_alcance_horizontal

def calcular_angulo_optimo(velocidad_inicial, altura_inicial):
    """
    Calcula el ángulo óptimo que maximiza el alcance horizontal de un proyectil.
    
    Parámetros:
    velocidad_inicial : float
        Velocidad inicial del proyectil en m/s
    altura_inicial : float
        Altura inicial del proyectil en metros
    
    Retorna:
    float : Ángulo óptimo en grados
    """
    # Para encontrar el ángulo óptimo, evaluamos el alcance en un rango de ángulos
    # y seleccionamos el que proporciona el mayor alcance
    
    # Creamos un vector de ángulos a evaluar
    angulos = np.linspace(1, 89, 89)  # Evitamos 0° y 90° para prevenir singularidades
    
    # Calculamos el alcance para cada ángulo
    alcances = np.zeros_like(angulos, dtype=float)
    
    for i, angulo in enumerate(angulos):
        alcances[i] = calcular_alcance_horizontal(velocidad_inicial, angulo, altura_inicial)
    
    # Encontramos el índice del ángulo que maximiza el alcance
    indice_maximo = np.argmax(alcances)
    angulo_optimo_aproximado = angulos[indice_maximo]
    
    # Para mayor precisión, podemos refinar la búsqueda alrededor del ángulo óptimo aproximado
    # utilizando métodos numéricos más avanzados
    
    # Definimos un rango más estrecho alrededor del ángulo óptimo aproximado
    delta = 1.0  # Rango de +/- 1 grado
    angulos_refinados = np.linspace(
        max(1, angulo_optimo_aproximado - delta), 
        min(89, angulo_optimo_aproximado + delta), 
        20
    )
    
    # Calculamos el alcance para cada ángulo refinado
    alcances_refinados = np.zeros_like(angulos_refinados, dtype=float)
    
    for i, angulo in enumerate(angulos_refinados):
        alcances_refinados[i] = calcular_alcance_horizontal(velocidad_inicial, angulo, altura_inicial)
    
    # Encontramos el índice del ángulo refinado que maximiza el alcance
    indice_maximo_refinado = np.argmax(alcances_refinados)
    angulo_optimo = angulos_refinados[indice_maximo_refinado]
    
    # Calculamos el alcance máximo con el ángulo óptimo
    alcance_maximo = alcances_refinados[indice_maximo_refinado]
    
    print(f"Alcance máximo: {alcance_maximo:.2f} metros")
    
    # Si la altura inicial es 0, sabemos teóricamente que el ángulo óptimo es 45°
    # (sin resistencia del aire)
    if abs(altura_inicial) < 1e-6:  # Consideramos altura ≈ 0
        teoria = "Teóricamente, para un lanzamiento desde el suelo sin resistencia del aire, el ángulo óptimo es 45°."
        print(teoria)
    
    return angulo_optimo

# Ejemplo de uso independiente
if __name__ == "__main__":
    velocidad = 30  # m/s
    altura = 0      # metros
    angulo = calcular_angulo_optimo(velocidad, altura)
    print(f"El ángulo óptimo para un lanzamiento con velocidad inicial {velocidad} m/s desde una altura de {altura} m es {angulo:.2f}°")