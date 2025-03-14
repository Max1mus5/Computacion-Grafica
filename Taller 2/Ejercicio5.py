import numpy as np
import re

# Ejercicio 5: Conteo de Palabras
# Crea una función que reciba una cadena de texto y retorne un diccionario con el conteo 
# de cuántas veces aparece cada palabra. Considera ignorar mayúsculas y signos de puntuación.

def contar_palabras(texto):
    """
    Cuenta cuántas veces aparece cada palabra en un texto.
    Ignora mayúsculas y signos de puntuación.
    
    Args:
        texto (str): Cadena de texto a analizar
        
    Returns:
        dict: Diccionario con el conteo de cada palabra
    """
    # Convertir a minúsculas
    texto = texto.lower()
    
    # Eliminar puntuación y caracteres especiales
    texto = re.sub(r'[^\w\s]', '', texto)
    
    # Dividir en palabras
    palabras = texto.split()
    
    # Crear diccionario para el conteo
    conteo = {}
    
    # Contar las palabras
    for palabra in palabras:
        if palabra in conteo:
            conteo[palabra] += 1
        else:
            conteo[palabra] = 1
    
    return conteo

# Versión alternativa usando NumPy y funciones más avanzadas
def contar_palabras_numpy(texto):
    """
    Cuenta cuántas veces aparece cada palabra usando NumPy para procesamiento.
    
    Args:
        texto (str): Cadena de texto a analizar
        
    Returns:
        dict: Diccionario con el conteo de cada palabra
    """
    # Procesar el texto
    texto = texto.lower()
    texto = re.sub(r'[^\w\s]', '', texto)
    palabras = np.array(texto.split())
    
    # Obtener palabras únicas
    palabras_unicas = np.unique(palabras)
    
    # Crear diccionario para almacenar el conteo
    conteo = {}
    
    # Contar cada palabra única
    for palabra in palabras_unicas:
        conteo[palabra] = np.sum(palabras == palabra)
    
    return conteo

# Función de prueba para ejecutar directamente este script
def main():
    print("Conteo de Palabras en una Cadena")
    texto = input("Ingrese un texto: ")
    
    conteo = contar_palabras(texto)
    print("\nConteo de palabras:")
    for palabra, cantidad in conteo.items():
        print(f"'{palabra}': {cantidad}")

if __name__ == "__main__":
    main()