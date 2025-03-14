# Ejercicio 2: Operaciones Básicas
# Pistas:
# - La suma y la resta se pueden hacer directamente (a + b, a - b).
# - Para el producto elemento a elemento, simplemente multiplica a y b.
# - Utiliza np.sum(a) para sumar todos los elementos dentro de a.

import numpy as np

def main():
    print("\n===== Ejercicio 2: Operaciones Básicas =====")
    
    # Crear dos arrays para realizar operaciones
    a = np.array([1, 2, 3, 4, 5])
    b = np.array([6, 7, 8, 9, 10])
    
    print(f"\nArray a:")
    print(a)
    print(f"\nArray b:")
    print(b)
    
    # Suma de arrays
    suma = a + b
    print(f"\nSuma (a + b):")
    print(suma)
    
    # Resta de arrays
    resta = b - a
    print(f"\nResta (b - a):")
    print(resta)
    
    # Multiplicación elemento a elemento
    multiplicacion = a * b
    print(f"\nMultiplicación elemento a elemento (a * b):")
    print(multiplicacion)
    
    # División elemento a elemento
    division = b / a
    print(f"\nDivisión elemento a elemento (b / a):")
    print(division)
    
    # Potencia elemento a elemento
    potencia = a ** 2
    print(f"\nPotencia al cuadrado (a ** 2):")
    print(potencia)
    
    # Operaciones estadísticas
    print(f"\nOperaciones estadísticas:")
    print(f"Suma de todos los elementos de a: {np.sum(a)}")
    print(f"Promedio de a: {np.mean(a)}")
    print(f"Valor mínimo de a: {np.min(a)}")
    print(f"Valor máximo de a: {np.max(a)}")
    print(f"Desviación estándar de a: {np.std(a)}")
    
    # Operaciones con matrices
    print(f"\nOperaciones con matrices:")
    
    # Crear dos matrices
    A = np.array([[1, 2], [3, 4]])
    B = np.array([[5, 6], [7, 8]])
    
    print(f"\nMatriz A:")
    print(A)
    print(f"\nMatriz B:")
    print(B)
    
    # Producto matricial
    producto_matricial = np.dot(A, B)
    print(f"\nProducto matricial (np.dot(A, B)):")
    print(producto_matricial)
    
    # Alternativa para el producto matricial
    producto_matricial_alt = A @ B
    print(f"\nProducto matricial alternativo (A @ B):")
    print(producto_matricial_alt)

if __name__ == "__main__":
    main()