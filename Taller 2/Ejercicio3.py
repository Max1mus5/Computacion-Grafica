import numpy as np

# Ejercicio 3: Transformación de Listas con Map y Lambda
# Escribe un script que utilice map y una función lambda para convertir todas las temperaturas
# de una lista de grados Celsius a Fahrenheit.

def celsius_a_fahrenheit(temperaturas_celsius):
    """
    Convierte una lista de temperaturas de Celsius a Fahrenheit 
    utilizando map y una función lambda.
    
    Args:
        temperaturas_celsius (list): Lista de temperaturas en grados Celsius
        
    Returns:
        list: Lista de temperaturas convertidas a grados Fahrenheit
    """
    # Fórmula: F = C * 9/5 + 32
    # Usar map y lambda para aplicar la conversión a cada elemento
    return list(map(lambda c: c * 9/5 + 32, temperaturas_celsius))

# Versión alternativa usando NumPy
def celsius_a_fahrenheit_numpy(temperaturas_celsius):
    """
    Convierte una lista de temperaturas de Celsius a Fahrenheit usando NumPy.
    
    Args:
        temperaturas_celsius (list): Lista de temperaturas en grados Celsius
        
    Returns:
        list: Lista de temperaturas convertidas a grados Fahrenheit
    """
    # Convertir la lista a un array de NumPy
    celsius_array = np.array(temperaturas_celsius)
    
    # Aplicar la fórmula de conversión
    fahrenheit_array = celsius_array * 9/5 + 32
    
    # Convertir el array de NumPy de vuelta a una lista
    return fahrenheit_array.tolist()

# Función de prueba para ejecutar directamente este script
def main():
    print("Conversión de Temperaturas de Celsius a Fahrenheit")
    try:
        entrada = input("Ingrese temperaturas en Celsius separadas por espacios: ")
        temperaturas = [float(x) for x in entrada.split()]
        
        # Usar la versión con map y lambda
        fahrenheit = celsius_a_fahrenheit(temperaturas)
        print(f"Usando map y lambda - Temperaturas en Fahrenheit: {fahrenheit}")
        
        # Usar la versión con NumPy
        fahrenheit_numpy = celsius_a_fahrenheit_numpy(temperaturas)
        print(f"Usando NumPy - Temperaturas en Fahrenheit: {fahrenheit_numpy}")
        
    except ValueError:
        print("Error: Ingrese números válidos para las temperaturas.")

if __name__ == "__main__":
    main()