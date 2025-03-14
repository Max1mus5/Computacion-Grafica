# Ejercicio 10: Funciones de Transformación y Redimensionamiento
# a. Crea un array con los números del 1 al 6.
# b. Cambia la forma del array a una matriz 2x3.
# c. Imprime la matriz.

import numpy as np

def main():
    print("\n--- Ejercicio 10: Funciones de Transformación y Redimensionamiento ---\n")
    
    # a. Crea un array con los números del 1 al 6
    array = np.array(range(1, 7))
    
    print("Array original:")
    print(array)
    print(f"Forma original: {array.shape}")
    
    # b. Cambia la forma del array a una matriz 2x3
    matriz = array.reshape(2, 3)
    
    # c. Imprime la matriz
    print("\nMatriz transformada (2x3):")
    print(matriz)
    print(f"Nueva forma: {matriz.shape}")
    
    # Ejemplos adicionales de transformación y redimensionamiento
    print("\nEjemplos adicionales de transformación:")
    
    # Transponer la matriz
    transpuesta = matriz.T
    print("\nMatriz transpuesta:")
    print(transpuesta)
    print(f"Forma de la transpuesta: {transpuesta.shape}")
    
    # Aplanar la matriz a 1D
    aplanada = matriz.flatten()
    print("\nMatriz aplanada:")
    print(aplanada)
    print(f"Forma aplanada: {aplanada.shape}")
    
    # Redimensionar a 3x2
    redimensionada = matriz.reshape(3, 2)
    print("\nMatriz redimensionada a 3x2:")
    print(redimensionada)
    print(f"Forma redimensionada: {redimensionada.shape}")
    
    # Redimensionamiento con -1 (automático)
    auto_dimensionada = array.reshape(-1, 2)  # -1 significa "calcular automáticamente"
    print("\nMatriz auto-dimensionada (-1, 2):")
    print(auto_dimensionada)
    print(f"Forma auto-dimensionada: {auto_dimensionada.shape}")
    
    # Añadir una nueva dimensión
    nueva_dim = array[:, np.newaxis]
    print("\nArray con nueva dimensión:")
    print(nueva_dim)
    print(f"Forma con nueva dimensión: {nueva_dim.shape}")

if __name__ == "__main__":
    main()