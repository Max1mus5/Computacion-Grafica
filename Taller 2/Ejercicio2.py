import numpy as np

# Ejercicio 2: Filtrado de Lista
# Desarrolla una función que reciba una lista de números y devuelva 
# solo aquellos que sean pares. Utiliza un bucle y condicionales dentro de la función.

def filtrar_pares(lista):
    """
    Filtra una lista de números y devuelve solo los pares.
    
    Args:
        lista (list): Lista de números
        
    Returns:
        list: Lista con solo los números pares
    """
    # Convertir la lista a un array de NumPy
    arr = np.array(lista)
    
    # Crear una lista vacía para almacenar los números pares
    pares = []
    
    # Recorrer el array y verificar si cada número es par
    for num in arr:
        if num % 2 == 0:
            pares.append(num)
    
    return pares

# Versión alternativa usando NumPy directamente
def filtrar_pares_numpy(lista):
    """
    Filtra una lista de números y devuelve solo los pares usando NumPy.
    
    Args:
        lista (list): Lista de números
        
    Returns:
        list: Lista con solo los números pares
    """
    arr = np.array(lista)
    return arr[arr % 2 == 0].tolist()

# Función de prueba para ejecutar directamente este script
def main():
    print("Filtrado de Lista por Números Pares")
    try:
        entrada = input("Ingrese una lista de números separados por espacios: ")
        numeros = [int(x) for x in entrada.split()]
        
        pares = filtrar_pares(numeros)
        pares_numpy = filtrar_pares_numpy(numeros)
        
        print(f"Usando bucle y condicionales - Números pares: {pares}")
        print(f"Usando NumPy directamente - Números pares: {pares_numpy}")
        
    except ValueError:
        print("Error: Ingrese números enteros válidos.")

if __name__ == "__main__":
    main()