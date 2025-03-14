# Ejercicio 2: Crear un Array Multidimensional
# a. Crea una matriz 2D con 3 filas y 3 columnas, llenada con números del 1 al 9.
# b. Imprime la matriz.

import numpy as np

def main():
    print("\n--- Ejercicio 2: Crear un Array Multidimensional ---\n")
    
    # a. Crea una matriz 2D con 3 filas y 3 columnas, llenada con números del 1 al 9
    # Primero creamos un array con los números del 1 al 9
    numeros = np.arange(1, 10)
    
    # Luego lo reorganizamos en una matriz 3x3
    matriz_2d = numeros.reshape(3, 3)
    
    # b. Imprime la matriz
    print("Matriz 2D con 3 filas y 3 columnas (números del 1 al 9):")
    print(matriz_2d)
    
    # Información adicional sobre la matriz
    print("\nInformación de la matriz:")
    print(f"Dimensiones: {matriz_2d.ndim}")
    print(f"Forma: {matriz_2d.shape}")
    print(f"Tipo de datos: {matriz_2d.dtype}")

if __name__ == "__main__":
    main()