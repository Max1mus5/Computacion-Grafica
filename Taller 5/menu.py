import numpy as np
from Functions import *

def main():
    print("Taller 5 - Manipulación Avanzada de Arrays con NumPy")
    print("=================================================")
    
    # Ejercicio 1: Crear vector A
    A = create_vector([2, 3, 5, 1, 4, 7, 9, 8, 6, 10])
    print("\n1) Vector A creado:")
    print(A)
    
    # Ejercicio 2: Crear vector B
    B = create_range_vector(11, 20)
    print("\n2) Vector B creado:")
    print(B)
    
    # Ejercicio 3: Concatenar vectores A y B
    C = concatenate_vectors(A, B)
    print("\n3) Vector C (concatenación de A y B):")
    print(C)
    
    # Ejercicio 4: Valor mínimo en vector C
    min_value = find_min(C)
    print("\n4) Valor mínimo en el vector C:")
    print(min_value)
    
    # Ejercicio 5: Valor máximo en vector C
    max_value = find_max(C)
    print("\n5) Valor máximo en el vector C:")
    print(max_value)
    
    # Ejercicio 6: Longitud del vector C
    length = get_length(C)
    print("\n6) Longitud del vector C:")
    print(length)
    
    # Ejercicio 7: Promedio manual del vector C
    avg_manual = calculate_average_manually(C)
    print("\n7) Promedio manual del vector C:")
    print(avg_manual)
    
    # Ejercicio 8: Promedio con NumPy del vector C
    avg_numpy = calculate_average(C)
    print("\n8) Promedio con NumPy del vector C:")
    print(avg_numpy)
    
    # Ejercicio 9: Mediana del vector C
    median = calculate_median(C)
    print("\n9) Mediana del vector C:")
    print(median)
    
    # Ejercicio 10: Suma de elementos del vector C
    total_sum = calculate_sum(C)
    print("\n10) Suma de elementos del vector C:")
    print(total_sum)
    
    # Ejercicio 11: Vector D con elementos mayores que 5
    D = filter_greater_than(C, 5)
    print("\n11) Vector D (elementos de C mayores que 5):")
    print(D)
    
    # Ejercicio 12: Vector E con elementos entre 5 y 15
    E = filter_between(C, 5, 15)
    print("\n12) Vector E (elementos de C mayores que 5 y menores que 15):")
    print(E)
    
    # Ejercicio 13: Cambiar elementos 5 y 15 por '7'
    # Nota: Los índices en Python comienzan en 0, así que el elemento 5 es C[4] y elemento 15 es C[14]
    C_copy = C.copy()  # Hacemos una copia para no afectar el vector original
    C_modified = replace_element(C_copy, 4, 7)
    C_modified = replace_element(C_modified, 14, 7)
    print("\n13) Vector C con elementos 5 y 15 cambiados por 7:")
    print(C_modified)
    
    # Ejercicio 14: Determinar la moda del vector C
    mode = find_mode(C)
    print("\n14) Moda del vector C:")
    print(mode)
    
    # Ejercicio 15: Ordenar vector C de menor a mayor
    C_sorted = sort_vector(C)
    print("\n15) Vector C ordenado de menor a mayor:")
    print(C_sorted)
    
    # Ejercicio 16: Multiplicar vector C por 10
    C_multiplied = multiply_vector(C, 10)
    print("\n16) Vector C multiplicado por 10:")
    print(C_multiplied)
    
    # Ejercicio 17: Cambiar elementos del 6 al 8 por 60, 70 y 80
    # Nota: Los índices en Python comienzan en 0, así que los elementos 6-8 son C[5:8]
    C_copy2 = C.copy()  # Hacemos una copia para no afectar el vector original
    C_modified2 = replace_range_with_values(C_copy2, 5, 7, [60, 70, 80])
    print("\n17) Vector C con elementos 6 al 8 cambiados por 60, 70 y 80:")
    print(C_modified2)
    
    # Ejercicio 18: Cambiar elementos del 14 al 16 por 140, 150 y 160
    # Nota: Los índices en Python comienzan en 0, así que los elementos 14-16 son C[13:16]
    C_copy3 = C.copy()  # Hacemos una copia para no afectar el vector original
    C_modified3 = replace_range_with_values(C_copy3, 13, 15, [140, 150, 160])
    print("\n18) Vector C con elementos 14 al 16 cambiados por 140, 150 y 160:")
    print(C_modified3)
    
if __name__ == "__main__":
    main()