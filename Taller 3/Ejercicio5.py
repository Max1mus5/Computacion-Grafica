# Ejercicio 5: Manipulación de Formas y Algebra Lineal
# Pistas:
# - Usa .reshape(3, 2) para cambiar la forma de M.
# - El producto punto de M y su transpuesta (M.T) se puede calcular con np.dot(M, M.T).

import numpy as np

def main():
    print("\n===== Ejercicio 5: Manipulación de Formas y Algebra Lineal =====")
    
    # Crear una matriz
    M = np.array([1, 2, 3, 4, 5, 6])
    print(f"\nArray original M:")
    print(M)
    print(f"Forma: {M.shape}")
    
    # Cambiar la forma a una matriz 3x2
    M_reshaped = M.reshape(3, 2)
    print(f"\nMatriz M con forma cambiada (3x2):")
    print(M_reshaped)
    print(f"Forma: {M_reshaped.shape}")
    
    # Obtener la transpuesta de M
    M_transpose = M_reshaped.T
    print(f"\nTranspuesta de M (M.T):")
    print(M_transpose)
    print(f"Forma: {M_transpose.shape}")
    
    # Producto punto entre M y su transpuesta
    dot_product = np.dot(M_reshaped, M_transpose)
    print(f"\nProducto punto de M y su transpuesta (np.dot(M, M.T)):")
    print(dot_product)
    print(f"Forma: {dot_product.shape}")
    
    # Operaciones de álgebra lineal
    print(f"\nOperaciones de álgebra lineal:")
    
    # Crear una matriz cuadrada para demostrar operaciones de álgebra lineal
    A = np.array([[4, 2], [3, 1]])
    print(f"\nMatriz A:")
    print(A)
    
    # Determinante
    det_A = np.linalg.det(A)
    print(f"\nDeterminante de A (np.linalg.det(A)): {det_A}")
    
    # Inversa
    inv_A = np.linalg.inv(A)
    print(f"\nInversa de A (np.linalg.inv(A)):")
    print(inv_A)
    
    # Verificar la inversa (debería dar la matriz identidad)
    identity_check = np.dot(A, inv_A)
    print(f"\nA · A^(-1) (debería ser aproximadamente la matriz identidad):")
    print(identity_check)
    
    # Autovalores y autovectores
    eigenvalues, eigenvectors = np.linalg.eig(A)
    print(f"\nAutovalores de A (np.linalg.eig(A)[0]):")
    print(eigenvalues)
    print(f"\nAutovectores de A (np.linalg.eig(A)[1]):")
    print(eigenvectors)
    
    # Resolver un sistema de ecuaciones lineales
    print(f"\nResolviendo sistema de ecuaciones lineales:")
    
    # Sistema: 4x + 2y = 8, 3x + y = 5
    b = np.array([8, 5])
    print(f"\nMatriz A:")
    print(A)
    print(f"Vector b:")
    print(b)
    
    solution = np.linalg.solve(A, b)
    print(f"\nSolución (np.linalg.solve(A, b)):")
    print(f"x = {solution[0]}, y = {solution[1]}")
    
    # Verificar la solución
    verification = np.dot(A, solution)
    print(f"\nVerificación (A · solución):")
    print(verification)
    
    # Norma de una matriz/vector
    norm_A = np.linalg.norm(A)
    print(f"\nNorma de A (np.linalg.norm(A)): {norm_A}")

if __name__ == "__main__":
    main()