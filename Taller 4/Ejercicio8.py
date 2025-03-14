# Ejercicio 8: Creación de Arrays con Funciones de Fábrica
# a. Crea un array de 5 elementos, todos inicializados con el valor 7.
# b. Imprime el array.

import numpy as np

def main():
    print("\n--- Ejercicio 8: Creación de Arrays con Funciones de Fábrica ---\n")
    
    # a. Crea un array de 5 elementos, todos inicializados con el valor 7
    array_de_sietes = np.full(5, 7)
    
    # b. Imprime el array
    print("Array de 5 elementos con valor 7:")
    print(array_de_sietes)
    
    # Ejemplos adicionales de funciones de fábrica
    print("\nOtros ejemplos de funciones de fábrica:")
    
    # Array de ceros
    array_ceros = np.zeros(5)
    print(f"Array de ceros: {array_ceros}")
    
    # Array de unos
    array_unos = np.ones(5)
    print(f"Array de unos: {array_unos}")
    
    # Array con valores equidistantes
    array_espaciado = np.linspace(0, 10, 5)  # 5 valores entre 0 y 10
    print(f"Array con valores equidistantes: {array_espaciado}")
    
    # Matriz identidad 3x3
    matriz_identidad = np.eye(3)
    print("\nMatriz identidad 3x3:")
    print(matriz_identidad)
    
    # Matriz diagonal
    matriz_diagonal = np.diag([1, 2, 3])
    print("\nMatriz diagonal:")
    print(matriz_diagonal)

if __name__ == "__main__":
    main()