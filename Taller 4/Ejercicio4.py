# Ejercicio 4: Funciones Matemáticas
# a. Crea un array con los números del 1 al 5.
# b. Calcula la exponencial de cada elemento del array y guarda el resultado en un nuevo array.
# c. Imprime el nuevo array.

import numpy as np

def main():
    print("\n--- Ejercicio 4: Funciones Matemáticas ---\n")
    
    # a. Crea un array con los números del 1 al 5
    array = np.array(range(1, 6))
    
    print("Array original:")
    print(array)
    
    # b. Calcula la exponencial de cada elemento del array y guarda el resultado en un nuevo array
    # La exponencial de x es e^x, donde e es el número de Euler (≈ 2.71828)
    array_exp = np.exp(array)
    
    # c. Imprime el nuevo array
    print("\nExponencial de cada elemento (e^x):")
    print(array_exp)
    
    # Mostramos otras funciones matemáticas comunes
    print("\nOtras funciones matemáticas:")
    print(f"Logaritmo natural (ln(x)): {np.log(array)}")
    print(f"Seno (sin(x)): {np.sin(array)}")
    print(f"Coseno (cos(x)): {np.cos(array)}")
    print(f"Raíz cuadrada (sqrt(x)): {np.sqrt(array)}")

if __name__ == "__main__":
    main()