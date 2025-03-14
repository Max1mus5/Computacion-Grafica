# Ejercicio 4: Broadcasting y Funciones Universales
# Pistas:
# - Crea A usando np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]).
# - Para sumar un escalar a A y aplicar una ufunc, simplemente haz A + 10 y np.sqrt(A).

import numpy as np

def main():
    print("\n===== Ejercicio 4: Broadcasting y Funciones Universales =====")
    
    # Crear matriz A
    A = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    print(f"\nMatriz A:")
    print(A)
    
    # Broadcasting con escalar
    print(f"\nBroadcasting con escalar:")
    
    # Sumar un escalar a todos los elementos
    A_plus_10 = A + 10
    print(f"\nA + 10:")
    print(A_plus_10)
    
    # Multiplicar todos los elementos por un escalar
    A_times_2 = A * 2
    print(f"\nA * 2:")
    print(A_times_2)
    
    # Broadcasting con arrays
    print(f"\nBroadcasting con arrays:")
    
    # Crear un vector fila
    row_vector = np.array([10, 20, 30])
    print(f"\nVector fila:")
    print(row_vector)
    
    # Sumar el vector fila a cada fila de A
    A_plus_row = A + row_vector
    print(f"\nA + vector fila (broadcasting):")
    print(A_plus_row)
    
    # Crear un vector columna
    col_vector = np.array([[100], [200], [300]])
    print(f"\nVector columna:")
    print(col_vector)
    
    # Sumar el vector columna a cada columna de A
    A_plus_col = A + col_vector
    print(f"\nA + vector columna (broadcasting):")
    print(A_plus_col)
    
    # Funciones universales (ufuncs)
    print(f"\nFunciones universales (ufuncs):")
    
    # Raíz cuadrada
    sqrt_A = np.sqrt(A)
    print(f"\nRaíz cuadrada de A (np.sqrt(A)):")
    print(sqrt_A)
    
    # Exponencial
    exp_A = np.exp(A)
    print(f"\nExponencial de A (np.exp(A)):")
    print(exp_A)
    
    # Logaritmo natural
    log_A_plus_1 = np.log1p(A)  # log(1+x) es más estable numéricamente para valores pequeños
    print(f"\nLogaritmo natural de (A+1) (np.log1p(A)):")
    print(log_A_plus_1)
    
    # Funciones trigonométricas
    sin_A = np.sin(A)
    print(f"\nSeno de A (np.sin(A)):")
    print(sin_A)
    
    # Funciones de redondeo
    print(f"\nFunciones de redondeo:")
    decimal_A = A / 3
    print(f"\nA / 3:")
    print(decimal_A)
    
    print(f"\nRedondeo hacia abajo (np.floor(A/3)):")
    print(np.floor(decimal_A))
    
    print(f"\nRedondeo hacia arriba (np.ceil(A/3)):")
    print(np.ceil(decimal_A))
    
    print(f"\nRedondeo al entero más cercano (np.round(A/3)):")
    print(np.round(decimal_A))

if __name__ == "__main__":
    main()