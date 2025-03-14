import numpy as np

# Ejercicio 4: Sistema de Calificaciones
# Implementa una función que reciba una lista de calificaciones numéricas y devuelva 
# una lista con las calificaciones convertidas a letras (A, B, C, D, F) según el rango 
# en el que se encuentren.

def convertir_calificaciones(calificaciones):
    """
    Convierte una lista de calificaciones numéricas a letras.
    
    Rangos de conversión:
    - 90-100: A
    - 80-89: B
    - 70-79: C
    - 60-69: D
    - 0-59: F
    
    Args:
        calificaciones (list): Lista de calificaciones numéricas
        
    Returns:
        list: Lista de calificaciones convertidas a letras
    """
    # Convertir la lista a un array de NumPy
    cal_array = np.array(calificaciones)
    
    # Crear un array vacío del mismo tamaño para almacenar las letras
    letras = []
    
    # Recorrer cada calificación y convertirla a letra
    for cal in cal_array:
        if cal >= 90 and cal <= 100:
            letras.append('A')
        elif cal >= 80 and cal < 90:
            letras.append('B')
        elif cal >= 70 and cal < 80:
            letras.append('C')
        elif cal >= 60 and cal < 70:
            letras.append('D')
        elif cal >= 0 and cal < 60:
            letras.append('F')
        else:
            letras.append('Calificación fuera de rango')
    
    return letras

# Versión alternativa usando NumPy de forma más eficiente
def convertir_calificaciones_numpy(calificaciones):
    """
    Convierte una lista de calificaciones numéricas a letras usando NumPy de forma vectorizada.
    
    Args:
        calificaciones (list): Lista de calificaciones numéricas
        
    Returns:
        list: Lista de calificaciones convertidas a letras
    """
    cal_array = np.array(calificaciones)
    
    # Preinicializar un array de letras con 'F'
    letras = np.full(cal_array.shape, 'F', dtype=object)
    
    # Usar máscaras condicionales para asignar letras
    letras[cal_array >= 90] = 'A'
    letras[(cal_array >= 80) & (cal_array < 90)] = 'B'
    letras[(cal_array >= 70) & (cal_array < 80)] = 'C'
    letras[(cal_array >= 60) & (cal_array < 70)] = 'D'
    
    # Marcar calificaciones fuera de rango
    letras[(cal_array < 0) | (cal_array > 100)] = 'Calificación fuera de rango'
    
    return letras.tolist()

# Función de prueba para ejecutar directamente este script
def main():
    print("Sistema de Calificaciones a Letras")
    try:
        entrada = input("Ingrese calificaciones numéricas separadas por espacios: ")
        calificaciones = [float(x) for x in entrada.split()]
        
        letras = convertir_calificaciones(calificaciones)
        print("Calificaciones convertidas a letras:")
        for i, letra in enumerate(letras):
            print(f"Calificación {calificaciones[i]}: {letra}")
            
    except ValueError:
        print("Error: Ingrese números válidos para las calificaciones.")

if __name__ == "__main__":
    main()