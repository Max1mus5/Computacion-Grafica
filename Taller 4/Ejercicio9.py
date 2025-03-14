# Ejercicio 9: Operaciones de Alineación y Broadcasting
# a. Crea dos arrays: uno con los números del 1 al 3 y otro con los números del 4 al 6.
# b. Suma los dos arrays utilizando broadcasting y guarda el resultado en un nuevo array.
# c. Imprime el nuevo array.

import numpy as np

def main():
    print("\n--- Ejercicio 9: Operaciones de Alineación y Broadcasting ---\n")
    
    # a. Crea dos arrays: uno con los números del 1 al 3 y otro con los números del 4 al 6
    array1 = np.array([1, 2, 3])
    array2 = np.array([4, 5, 6])
    
    print("Array 1:")
    print(array1)
    
    print("\nArray 2:")
    print(array2)
    
    # b. Suma los dos arrays y guarda el resultado en un nuevo array
    # Nota: En este caso no es realmente broadcasting ya que ambos arrays tienen la misma forma
    # pero mostramos ejemplos de broadcasting a continuación
    resultado_suma = array1 + array2
    
    # c. Imprime el nuevo array
    print("\nResultado de la suma:")
    print(resultado_suma)
    
    # Ejemplos verdaderos de broadcasting
    print("\nEjemplos de broadcasting:")
    
    # Escalar + array
    escalar = 10
    resultado_escalar = escalar + array1
    print(f"Escalar (10) + array1: {resultado_escalar}")
    
    # Array 1D + array 2D
    array_1d = np.array([1, 2, 3])
    array_2d = np.array([[10], [20], [30]])
    
    print("\nArray 1D:")
    print(array_1d)
    print("\nArray 2D:")
    print(array_2d)
    
    resultado_broadcasting = array_1d + array_2d
    print("\nResultado del broadcasting (array_1d + array_2d):")
    print(resultado_broadcasting)
    
    # Explicación del resultado
    print("\nExplicación de broadcasting:")
    print("El array_1d (1,2,3) se expande a:")
    print("[[1, 2, 3],")
    print(" [1, 2, 3],")
    print(" [1, 2, 3]]")
    print("\nEl array_2d ([10],[20],[30]) se expande a:")
    print("[[10, 10, 10],")
    print(" [20, 20, 20],")
    print(" [30, 30, 30]]")
    print("\nLuego se suman elemento por elemento para obtener el resultado.")

if __name__ == "__main__":
    main()