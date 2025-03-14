# Ejercicio 7: Funciones de Agregación
# a. Crea un array con los números del 1 al 5.
# b. Calcula la media de los elementos del array.
# c. Imprime la media.

import numpy as np

def main():
    print("\n--- Ejercicio 7: Funciones de Agregación ---\n")
    
    # a. Crea un array con los números del 1 al 5
    array = np.array(range(1, 6))
    
    print("Array original:")
    print(array)
    
    # b. Calcula la media de los elementos del array
    media = np.mean(array)
    
    # c. Imprime la media
    print(f"\nMedia del array: {media}")
    
    # Ejemplos adicionales de funciones de agregación
    print("\nOtras funciones de agregación:")
    print(f"Suma de todos los elementos: {np.sum(array)}")
    print(f"Valor mínimo: {np.min(array)}")
    print(f"Valor máximo: {np.max(array)}")
    print(f"Mediana: {np.median(array)}")
    print(f"Desviación estándar: {np.std(array)}")
    print(f"Varianza: {np.var(array)}")
    
    # Ejemplo con una matriz 2x3
    matriz = np.array([[1, 2, 3], [4, 5, 6]])
    print("\nMatriz 2x3:")
    print(matriz)
    print(f"Media de toda la matriz: {np.mean(matriz)}")
    print(f"Media por filas: {np.mean(matriz, axis=1)}")
    print(f"Media por columnas: {np.mean(matriz, axis=0)}")

if __name__ == "__main__":
    main()