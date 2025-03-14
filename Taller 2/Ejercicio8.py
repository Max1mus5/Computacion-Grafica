import numpy as np
from operator import itemgetter

# Ejercicio 8: Ordenamiento Personalizado
# Implementa una función que ordene una lista de tuplas (nombre, edad) primero por edad 
# y luego por nombre (ambos en orden ascendente). Puedes usar la función sort o sorted 
# con parámetros personalizados.

def ordenar_tuplas(lista_tuplas):
    """
    Ordena una lista de tuplas (nombre, edad) primero por edad y luego por nombre.
    
    Args:
        lista_tuplas (list): Lista de tuplas con formato (nombre, edad)
        
    Returns:
        list: Lista ordenada de tuplas
    """
    # Usar sorted con una clave personalizada
    # itemgetter(1) ordena por el segundo elemento (edad)
    # itemgetter(0) ordena por el primer elemento (nombre)
    return sorted(lista_tuplas, key=lambda x: (x[1], x[0]))

# Versión alternativa usando NumPy para sortear
def ordenar_tuplas_numpy(lista_tuplas):
    """
    Ordena una lista de tuplas (nombre, edad) usando NumPy.
    
    Args:
        lista_tuplas (list): Lista de tuplas con formato (nombre, edad)
        
    Returns:
        list: Lista ordenada de tuplas
    """
    # Convertir a un array estructurado de NumPy
    dtype = [('nombre', 'U30'), ('edad', int)]
    arr = np.array([(t[0], t[1]) for t in lista_tuplas], dtype=dtype)
    
    # Ordenar el array
    arr_ordenado = np.sort(arr, order=['edad', 'nombre'])
    
    # Convertir de vuelta a lista de tuplas
    return [(t['nombre'], t['edad']) for t in arr_ordenado]

# Función de prueba para ejecutar directamente este script
def main():
    print("Ordenamiento Personalizado de Lista de Tuplas")
    personas = []
    
    try:
        n = int(input("Ingrese la cantidad de personas: "))
        for i in range(n):
            nombre = input(f"Ingrese el nombre de la persona {i+1}: ")
            edad = int(input(f"Ingrese la edad de {nombre}: "))
            personas.append((nombre, edad))
        
        # Ordenar usando la función principal
        ordenados = ordenar_tuplas(personas)
        
        print("\nPersonas ordenadas por edad y nombre:")
        for persona in ordenados:
            print(f"Nombre: {persona[0]}, Edad: {persona[1]}")
            
    except ValueError:
        print("Error: Ingrese valores válidos.")

if __name__ == "__main__":
    main()