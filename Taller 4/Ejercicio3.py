# Ejercicio 3: Operaciones Básicas con Arrays
# a. Crea dos arrays unidimensionales con los números del 1 al 5.
# b. Suma los dos arrays y guarda el resultado en un nuevo array.
# c. Imprime el resultado.

import numpy as np

def main():
    print("\n--- Ejercicio 3: Operaciones Básicas con Arrays ---\n")
    
    # a. Crea dos arrays unidimensionales con los números del 1 al 5
    array1 = np.array(range(1, 6))
    array2 = np.array(range(1, 6))
    
    print("Array 1:")
    print(array1)
    
    print("\nArray 2:")
    print(array2)
    
    # b. Suma los dos arrays y guarda el resultado en un nuevo array
    resultado = array1 + array2
    
    # c. Imprime el resultado
    print("\nResultado de la suma:")
    print(resultado)
    
    # Mostramos otras operaciones básicas para ilustrar
    print("\nOtras operaciones básicas:")
    print(f"Resta (array1 - array2): {array1 - array2}")
    print(f"Multiplicación (array1 * array2): {array1 * array2}")
    print(f"División (array1 / array2): {array1 / array2}")
    print(f"Potencia (array1 ** 2): {array1 ** 2}")

if __name__ == "__main__":
    main()