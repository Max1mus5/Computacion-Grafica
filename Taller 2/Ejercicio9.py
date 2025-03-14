import numpy as np
import random
import string

# Ejercicio 9: Generador de Contraseñas
# Crea una función que genere una contraseña aleatoria que consista en una combinación de 
# letras mayúsculas, minúsculas, números y símbolos. La longitud de la contraseña debe ser 
# un parámetro de la función.

def generar_contrasena(longitud):
    """
    Genera una contraseña aleatoria con una longitud especificada.
    La contraseña incluye letras mayúsculas, minúsculas, números y símbolos.
    
    Args:
        longitud (int): Longitud deseada para la contraseña
        
    Returns:
        str: Contraseña generada
    """
    # Definir los conjuntos de caracteres
    mayusculas = string.ascii_uppercase
    minusculas = string.ascii_lowercase
    numeros = string.digits
    simbolos = string.punctuation
    
    # Combinar todos los caracteres disponibles
    todos_caracteres = mayusculas + minusculas + numeros + simbolos
    
    # Asegurarse de que la contraseña tenga al menos un carácter de cada tipo
    if longitud < 4:
        print("La longitud debe ser al menos 4 para incluir todos los tipos de caracteres.")
        return None
    
    # Seleccionar un carácter de cada tipo
    pwd = [
        random.choice(mayusculas),
        random.choice(minusculas),
        random.choice(numeros),
        random.choice(simbolos)
    ]
    
    # Completar el resto de la contraseña con caracteres aleatorios
    for _ in range(longitud - 4):
        pwd.append(random.choice(todos_caracteres))
    
    # Mezclar los caracteres para evitar un patrón predecible
    random.shuffle(pwd)
    
    # Convertir la lista de caracteres a una cadena
    return ''.join(pwd)

# Versión alternativa usando NumPy para la generación aleatoria
def generar_contrasena_numpy(longitud):
    """
    Genera una contraseña aleatoria usando NumPy para la selección aleatoria.
    
    Args:
        longitud (int): Longitud deseada para la contraseña
        
    Returns:
        str: Contraseña generada
    """
    # Definir los conjuntos de caracteres
    mayusculas = np.array(list(string.ascii_uppercase))
    minusculas = np.array(list(string.ascii_lowercase))
    numeros = np.array(list(string.digits))
    simbolos = np.array(list(string.punctuation))
    
    # Combinar todos los caracteres disponibles
    todos_caracteres = np.concatenate([mayusculas, minusculas, numeros, simbolos])
    
    # Verificar la longitud mínima
    if longitud < 4:
        print("La longitud debe ser al menos 4 para incluir todos los tipos de caracteres.")
        return None
    
    # Seleccionar caracteres de cada tipo
    caracteres_obligatorios = [
        np.random.choice(mayusculas),
        np.random.choice(minusculas),
        np.random.choice(numeros),
        np.random.choice(simbolos)
    ]
    
    # Seleccionar el resto de caracteres
    caracteres_adicionales = np.random.choice(todos_caracteres, size=longitud-4)
    
    # Combinar y mezclar
    todos = np.concatenate([caracteres_obligatorios, caracteres_adicionales])
    np.random.shuffle(todos)
    
    # Unir en una cadena
    return ''.join(todos)

# Función de prueba para ejecutar directamente este script
def main():
    print("Generador de Contraseñas Aleatorias")
    try:
        longitud = int(input("Ingrese la longitud deseada para la contraseña: "))
        
        if longitud < 4:
            print("La longitud debe ser al menos 4 para incluir todos los tipos de caracteres.")
            return
        
        contrasena = generar_contrasena(longitud)
        print(f"Contraseña generada: {contrasena}")
        
    except ValueError:
        print("Error: Ingrese un número entero válido para la longitud.")

if __name__ == "__main__":
    main()