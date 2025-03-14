# Ejercicio 6: Generación de Datos Aleatorios
# a. Genera un array de 10 números aleatorios entre 0 y 1.
# b. Imprime el array.

import numpy as np

def main():
    print("\n--- Ejercicio 6: Generación de Datos Aleatorios ---\n")
    
    # Establecemos una semilla para reproducibilidad
    np.random.seed(42)
    
    # a. Genera un array de 10 números aleatorios entre 0 y 1
    array_aleatorio = np.random.random(10)
    
    # b. Imprime el array
    print("Array de 10 números aleatorios entre 0 y 1:")
    print(array_aleatorio)
    
    # Ejemplos adicionales de generación de datos aleatorios
    print("\nEjemplos adicionales de datos aleatorios:")
    
    # Enteros aleatorios entre 1 y 100
    enteros_aleatorios = np.random.randint(1, 101, size=5)
    print(f"Enteros aleatorios entre 1 y 100: {enteros_aleatorios}")
    
    # Números aleatorios con distribución normal (media=0, desviación estándar=1)
    normal_aleatorios = np.random.normal(0, 1, 5)
    print(f"Distribución normal (media=0, std=1): {normal_aleatorios}")
    
    # Matriz aleatoria 3x3
    matriz_aleatoria = np.random.random((3, 3))
    print("\nMatriz aleatoria 3x3:")
    print(matriz_aleatoria)

if __name__ == "__main__":
    main()