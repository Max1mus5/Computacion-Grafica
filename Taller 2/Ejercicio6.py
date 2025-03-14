import numpy as np

# Ejercicio 6: Función de Búsqueda
# Desarrolla una función que busque un elemento dado dentro de una lista y devuelva su índice 
# si lo encuentra o -1 si no está presente. No utilices métodos predefinidos como .index().

def buscar_elemento(lista, elemento):
    """
    Busca un elemento en una lista y devuelve su índice o -1 si no lo encuentra.
    No utiliza métodos predefinidos como .index().
    
    Args:
        lista (list): Lista donde buscar el elemento
        elemento: Elemento a buscar
        
    Returns:
        int: Índice del elemento o -1 si no se encuentra
    """
    # Recorrer la lista con un bucle y un índice
    for i in range(len(lista)):
        if lista[i] == elemento:
            return i
    
    # Si no se encuentra, devolver -1
    return -1

# Versión alternativa usando NumPy
def buscar_elemento_numpy(lista, elemento):
    """
    Busca un elemento en una lista usando NumPy y devuelve su índice.
    
    Args:
        lista (list): Lista donde buscar el elemento
        elemento: Elemento a buscar
        
    Returns:
        int: Índice del elemento o -1 si no se encuentra
    """
    # Convertir la lista a un array de NumPy
    arr = np.array(lista)
    
    # Buscar donde el elemento coincide
    indices = np.where(arr == elemento)[0]
    
    # Verificar si se encontraron coincidencias
    if len(indices) > 0:
        return int(indices[0])  # Devolver el primer índice encontrado
    else:
        return -1

# Función de prueba para ejecutar directamente este script
def main():
    print("Búsqueda de Elemento en Lista")
    entrada = input("Ingrese una lista de elementos separados por espacios: ")
    lista = entrada.split()
    
    elemento = input("Ingrese el elemento a buscar: ")
    
    indice = buscar_elemento(lista, elemento)
    
    if indice != -1:
        print(f"El elemento '{elemento}' se encuentra en la posición {indice}.")
    else:
        print(f"El elemento '{elemento}' no se encuentra en la lista.")

if __name__ == "__main__":
    main()