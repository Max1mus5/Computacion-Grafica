# Ejercicio 1: Creación y Propiedades de Arrays
# Pistas:
# - Usa np.array(range(1, 11)) para crear el array.
# - Para cambiar la forma, emplea el método .reshape(2, 5) en el array creado.
# - Accede a las propiedades .shape, .size, y .ndim para imprimir las dimensiones, la forma y el tamaño.

import numpy as np

def main():
    print("\n===== Ejercicio 1: Creación y Propiedades de Arrays =====")
    
    # Crear un array de números del 1 al 10
    array_original = np.array(range(1, 11))
    print(f"\nArray original:")
    print(array_original)
    
    # Mostrar propiedades del array original
    print(f"\nPropiedades del array original:")
    print(f"Dimensiones: {array_original.ndim}")
    print(f"Forma: {array_original.shape}")
    print(f"Tamaño: {array_original.size}")
    print(f"Tipo de datos: {array_original.dtype}")
    
    # Cambiar la forma del array a una matriz de 2x5
    array_reshape = array_original.reshape(2, 5)
    print(f"\nArray con forma cambiada (2x5):")
    print(array_reshape)
    
    # Mostrar propiedades del array con forma cambiada
    print(f"\nPropiedades del array con forma cambiada:")
    print(f"Dimensiones: {array_reshape.ndim}")
    print(f"Forma: {array_reshape.shape}")
    print(f"Tamaño: {array_reshape.size}")
    
    # Demostrar otras formas de crear arrays
    print("\nOtras formas de crear arrays:")
    
    # Crear array de ceros
    zeros_array = np.zeros((3, 3))
    print(f"\nArray de ceros (3x3):")
    print(zeros_array)
    
    # Crear array de unos
    ones_array = np.ones((2, 4))
    print(f"\nArray de unos (2x4):")
    print(ones_array)
    
    # Crear array con valores aleatorios
    random_array = np.random.rand(3, 3)
    print(f"\nArray con valores aleatorios (3x3):")
    print(random_array)

if __name__ == "__main__":
    main()