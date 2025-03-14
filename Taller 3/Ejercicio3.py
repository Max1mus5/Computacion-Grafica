# Ejercicio 3: Indexación y Slicing
# Pistas:
# - Recuerda que en Python, el índice comienza en 0, así que el quinto elemento es data[4].
# - Para obtener una subsección, utiliza data[2:7].

import numpy as np

def main():
    print("\n===== Ejercicio 3: Indexación y Slicing =====")
    
    # Crear un array de ejemplo
    data = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
    print(f"\nArray original:")
    print(data)
    
    # Indexación básica
    print(f"\nIndexación básica:")
    print(f"Primer elemento (data[0]): {data[0]}")
    print(f"Quinto elemento (data[4]): {data[4]}")
    print(f"Último elemento (data[-1]): {data[-1]}")
    
    # Slicing (rebanado)
    print(f"\nSlicing (rebanado):")
    print(f"Elementos del índice 2 al 7 (data[2:7]):")
    print(data[2:7])
    
    print(f"Elementos desde el inicio hasta el índice 5 (data[:5]):")
    print(data[:5])
    
    print(f"Elementos desde el índice 5 hasta el final (data[5:]):")
    print(data[5:])
    
    print(f"Elementos desde el inicio hasta el final, tomando cada 2 elementos (data[::2]):")
    print(data[::2])
    
    # Indexación y slicing en arrays multidimensionales
    print(f"\nIndexación y slicing en arrays multidimensionales:")
    
    # Crear un array 2D
    data_2d = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])
    print(f"\nArray 2D:")
    print(data_2d)
    
    # Indexación básica
    print(f"\nIndexación básica en array 2D:")
    print(f"Elemento en la fila 1, columna 2 (data_2d[1, 2]): {data_2d[1, 2]}")
    
    # Slicing en filas y columnas
    print(f"\nSlicing en filas y columnas:")
    print(f"Primera fila (data_2d[0]):")
    print(data_2d[0])
    
    print(f"Primera columna (data_2d[:, 0]):")
    print(data_2d[:, 0])
    
    print(f"Submatriz (filas 0 a 1, columnas 1 a 3) (data_2d[0:2, 1:3]):")
    print(data_2d[0:2, 1:3])
    
    # Indexación booleana
    print(f"\nIndexación booleana:")
    
    # Crear una máscara booleana
    mask = data > 50
    print(f"Máscara booleana (data > 50):")
    print(mask)
    
    # Aplicar la máscara
    filtered_data = data[mask]
    print(f"Elementos mayores a 50:")
    print(filtered_data)
    
    # Forma alternativa de indexación booleana
    print(f"Forma alternativa (data[data > 50]):")
    print(data[data > 50])

if __name__ == "__main__":
    main()