# Taller 1\Ejercicio2.py
# Ejercicio 2: Cálculo del tiempo de caída desde una altura
# 
# Descripción: Este programa calcula el tiempo que tarda un objeto
# en caer desde una altura determinada hasta el suelo, considerando
# únicamente la aceleración gravitatoria.
# Utiliza la fórmula derivada de la ecuación de caída libre.

import numpy as np

def calcular_tiempo_caida(altura):
    """
    Calcula el tiempo que tarda un objeto en caer desde una altura determinada.
    
    Parámetros:
    altura : float
        Altura inicial del objeto en metros
    
    Retorna:
    float : Tiempo de caída en segundos
    """
    g = 9.8  # Aceleración gravitatoria en m/s²
    
    # Utilizamos la ecuación de caída libre: h = h0 + v0*t - 0.5*g*t^2
    # Para calcular cuando h = 0, resolvemos: 0 = h0 - 0.5*g*t^2
    # Lo que nos da: t = sqrt(2*h0/g)
    
    # Representamos el problema como un sistema de ecuaciones lineales
    # Aunque es un problema sencillo, lo planteamos matricialmente para
    # mantener la consistencia con el enfoque de álgebra lineal
    
    # Matriz de coeficientes para la ecuación -0.5*g*t^2 + altura = 0
    A = np.array([[-0.5 * g]])
    b = np.array([altura])
    
    # Resolvemos para t^2
    t_squared = b / A[0]
    
    # Calculamos el tiempo de caída
    tiempo = np.sqrt(abs(t_squared))[0]
    
    return tiempo

# Ejemplo de uso independiente
if __name__ == "__main__":
    altura = 100  # metros
    tiempo = calcular_tiempo_caida(altura)
    print(f"Un objeto que cae desde {altura} metros tarda {tiempo:.2f} segundos en llegar al suelo.")