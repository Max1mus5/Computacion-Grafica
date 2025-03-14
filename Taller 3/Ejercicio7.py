# Ejercicio 7: Guardar y Cargar Arrays
# Pistas:
# - np.save('mi_array.npy', data) guarda el array data.
# - Usa np.load('mi_array.npy') para cargar el array desde el archivo.

import numpy as np
import os

def main():
    print("\n===== Ejercicio 7: Guardar y Cargar Arrays =====")
    
    # Crear un array para guardar
    data = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])
    print(f"\nArray original:")
    print(data)
    
    # Guardar el array en formato .npy (formato binario de NumPy)
    filename = 'mi_array.npy'
    np.save(filename, data)
    print(f"\nArray guardado como '{filename}'")
    
    # Verificar que el archivo existe
    if os.path.exists(filename):
        file_size = os.path.getsize(filename)
        print(f"El archivo existe y tiene un tamaño de {file_size} bytes")
    else:
        print(f"Error: El archivo no se guardó correctamente")
    
    # Cargar el array desde el archivo
    loaded_data = np.load(filename)
    print(f"\nArray cargado desde '{filename}':")
    print(loaded_data)
    
    # Verificar que los arrays son iguales
    is_equal = np.array_equal(data, loaded_data)
    print(f"\n¿Los arrays son iguales? {is_equal}")
    
    # Guardar múltiples arrays en un solo archivo
    array1 = np.array([1, 2, 3])
    array2 = np.array([4, 5, 6])
    array3 = np.array([7, 8, 9])
    
    multi_filename = 'multiple_arrays'
    np.savez(multi_filename, a=array1, b=array2, c=array3)
    print(f"\nMúltiples arrays guardados como '{multi_filename}'")
    
    # Cargar múltiples arrays
    loaded_arrays = np