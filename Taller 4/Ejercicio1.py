# Ejercicio 1: Crear un Array Unidimensional
# a. Crea un array unidimensional con los números del 1 al 10.
# b. Imprime el array.

import numpy as np

def main():
    print("\n--- Ejercicio 1: Crear un Array Unidimensional ---\n")
    
    # a. Crea un array unidimensional con los números del 1 al 10
    array_1d = np.array(range(1, 11))
    
    # b. Imprime el array
    print("Array unidimensional con números del 1 al 10:")
    print(array_1d)
    
    # Información adicional sobre el array
    print("\nInformación del array:")
    print(f"Dimensiones: {array_1d.ndim}")
    print(f"Forma: {array_1d.shape}")
    print(f"Tipo de datos: {array_1d.dtype}")

if __name__ == "__main__":
    main()