# Taller 1\Ejercicio4.py
# Ejercicio 4: Cálculo de trayectoria completa de un proyectil
# 
# Descripción: Este programa calcula y visualiza la trayectoria completa
# de un proyectil lanzado con una velocidad inicial, un ángulo determinado
# y desde una altura inicial dada.
# Utiliza NumPy para cálculos matriciales y matplotlib para visualización.

import numpy as np
import matplotlib.pyplot as plt

def calcular_trayectoria_proyectil(velocidad_inicial, angulo, altura_inicial):
    """
    Calcula y visualiza la trayectoria completa de un proyectil.
    
    Parámetros:
    velocidad_inicial : float
        Velocidad inicial del proyectil en m/s
    angulo : float
        Ángulo de lanzamiento en grados
    altura_inicial : float
        Altura inicial del proyectil en metros
    
    Retorna:
    None (Muestra un gráfico con la trayectoria)
    """
    g = 9.8  # Aceleración gravitatoria en m/s²
    
    # Convertir ángulo a radianes
    angulo_rad = np.radians(angulo)
    
    # Descomponemos la velocidad inicial en sus componentes
    v0_x = velocidad_inicial * np.cos(angulo_rad)
    v0_y = velocidad_inicial * np.sin(angulo_rad)
    
    # Estado inicial [x, y, vx, vy]
    x0 = np.array([0, altura_inicial, v0_x, v0_y])
    
    # Estimamos el tiempo de vuelo usando la fórmula cuadrática para calcular
    # cuándo y = 0, partiendo de y = y0 + v0_y*t - 0.5*g*t^2
    # Resolvemos la ecuación: 0 = altura_inicial + v0_y*t - 0.5*g*t^2
    a = -0.5 * g
    b = v0_y
    c = altura_inicial
    
    # Calculamos las raíces de la ecuación cuadrática
    discriminante = b**2 - 4*a*c
    
    if discriminante >= 0:
        t1 = (-b + np.sqrt(discriminante)) / (2*a)
        t2 = (-b - np.sqrt(discriminante)) / (2*a)
        # El tiempo de vuelo es la raíz positiva
        tiempo_vuelo = max(t1, t2) if t1 > 0 or t2 > 0 else 0
    else:
        # Si no hay solución real, estimamos un tiempo razonable
        tiempo_vuelo = 2 * v0_y / g
    
    # Aseguramos que el tiempo de vuelo sea positivo
    tiempo_vuelo = max(tiempo_vuelo, 2 * v0_y / g)
    
    # Creamos un vector de tiempo con suficientes puntos
    num_puntos = 100
    t = np.linspace(0, tiempo_vuelo, num_puntos)
    
    # Inicializamos matrices para almacenar resultados
    resultados = np.zeros((num_puntos, 4))
    
    # Para cada paso de tiempo, calculamos el estado del proyectil
    for i, tiempo in enumerate(t):
        # Matriz de transformación para este instante
        A = np.array([
            [1, 0, tiempo, 0],
            [0, 1, 0, tiempo],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
        
        # Vector de efecto gravitatorio [0, -0.5*g*t^2, 0, -g*t]
        b = np.array([0, -0.5 * g * tiempo**2, 0, -g * tiempo])
        
        # Calculamos el nuevo estado
        resultados[i] = A @ x0 + b
    
    # Extraemos las posiciones x e y
    x = resultados[:, 0]
    y = resultados[:, 1]
    
    # Encontramos el índice donde el proyectil toca el suelo (y ≤ 0)
    indices_impacto = np.where(y <= 0)[0]
    if len(indices_impacto) > 0:
        indice_impacto = indices_impacto[0]
        
        # Calculamos el alcance horizontal (punto de impacto)
        alcance = x[indice_impacto]
        tiempo_impacto = t[indice_impacto]
        
        # Interpolamos para obtener un valor más preciso del alcance
        if indice_impacto > 0:
            t_prev = t[indice_impacto - 1]
            y_prev = y[indice_impacto - 1]
            t_curr = t[indice_impacto]
            y_curr = y[indice_impacto]
            
            # Interpolación lineal para encontrar t_impacto exacto
            t_impacto = t_prev + (t_curr - t_prev) * (-y_prev) / (y_curr - y_prev)
            
            # Recalculamos el alcance con t_impacto
            A_impacto = np.array([
                [1, 0, t_impacto, 0],
                [0, 1, 0, t_impacto],
                [0, 0, 1, 0],
                [0, 0, 0, 1]
            ])
            b_impacto = np.array([0, -0.5 * g * t_impacto**2, 0, -g * t_impacto])
            estado_impacto = A_impacto @ x0 + b_impacto
            alcance = estado_impacto[0]
            tiempo_impacto = t_impacto
        
        # Truncamos los datos hasta el punto de impacto
        x = x[:indice_impacto+1]
        y = y[:indice_impacto+1]
        t = t[:indice_impacto+1]
        
        print(f"Alcance horizontal: {alcance:.2f} metros")
        print(f"Tiempo de vuelo: {tiempo_impacto:.2f} segundos")
    
    # Calculamos la altura máxima
    altura_maxima = np.max(y)
    indice_altura_max = np.argmax(y)
    tiempo_altura_max = t[indice_altura_max]
    
    print(f"Altura máxima: {altura_maxima:.2f} metros")
    print(f"Tiempo hasta altura máxima: {tiempo_altura_max:.2f} segundos")
    
    # Visualización de la trayectoria
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, 'b-', linewidth=2)
    plt.scatter([0], [altura_inicial], color='green', s=100, label='Punto de lanzamiento')
    plt.scatter([x[-1]], [y[-1]], color='red', s=100, label='Punto de impacto')
    plt.scatter([x[indice_altura_max]], [altura_maxima], color='purple', s=100, label='Altura máxima')
    
    plt.xlabel('Distancia horizontal (m)')
    plt.ylabel('Altura (m)')
    plt.title(f'Trayectoria de un proyectil (v₀={velocidad_inicial} m/s, θ={angulo}°)')
    plt.grid(True)
    plt.legend()
    plt.axis('equal')
    plt.show()

# Ejemplo de uso independiente
if __name__ == "__main__":
    calcular_trayectoria_proyectil(30, 45, 0)