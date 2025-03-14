# Ejercicio 5: Indexación y Segmentación
# a. Crea un array con los números del 1 al 10.
# b. Selecciona los elementos pares del array y guarda el resultado en un nuevo array.
# c. Imprime el nuevo array.

import numpy as np

def main():
    print("\n--- Ejercicio 5: Indexación y Segmentación ---\n")
    
    # a. Crea un array con los números del 1 al 10
    array = np.array(range(1, 11))
    
    print("Array original:")
    print(array)
    
    # b. Selecciona los elementos pares del array y guarda el resultado en un nuevo array
    # Método 1: Usando indexación booleana
    numeros_pares = array[array % 2 == 0]
    
    # Método alternativo: Usando slicing (comenzando desde el índice 1 y tomando cada 2 elementos)
    # numeros_pares = array[1::2]  # Esto seleccionaría posiciones pares (valores impares)
    # Para seleccionar valores pares, sería:
    # numeros_pares = array[::2]  # Esto seleccionaría posiciones impares (valores pares si empezamos en 1)
    
    # c. Imprime el nuevo array
    print("\nElementos pares del array:")
    print(numeros_pares)
    
    # Ejemplos adicionales de indexación y segmentación
    print("\nEjemplos adicionales de indexación y segmentación:")
    print(f"Primeros 3 elementos: {array[:3]}")
    print(f"Últimos 3 elementos: {array[-3:]}")
    print(f"Elementos del índice 2 al 7: {array[2:8]}")
    print(f"Elementos en posiciones pares (índices 0,2,4...): {array[::2]}")
    print(f"Array invertido: {array[::-1]}")

if __name__ == "__main__":
    main()