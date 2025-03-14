import numpy as np

# Ejercicio 7: Validación de Paréntesis
# Escribe una función que tome una cadena de solo paréntesis ( y ) y determine si la secuencia 
# es válida (cada paréntesis abierto tiene un correspondiente paréntesis cerrado).

def validar_parentesis(secuencia):
    """
    Valida si una secuencia de paréntesis es válida.
    Una secuencia válida tiene cada paréntesis abierto con su correspondiente cierre.
    
    Args:
        secuencia (str): Cadena que contiene solo paréntesis ( y )
        
    Returns:
        bool: True si la secuencia es válida, False en caso contrario
    """
    # Usar una pila para verificar los paréntesis
    pila = []
    
    # Recorrer cada carácter en la secuencia
    for char in secuencia:
        if char == '(':
            # Si es un paréntesis de apertura, lo añadimos a la pila
            pila.append(char)
        elif char == ')':
            # Si es un paréntesis de cierre, debe haber uno de apertura en la pila
            if not pila:  # Si la pila está vacía, no hay coincidencia
                return False
            # Eliminar el último paréntesis de apertura (coincidencia encontrada)
            pila.pop()
        else:
            # Si hay otros caracteres diferentes a paréntesis, la secuencia no es válida
            return False
    
    # La secuencia es válida si la pila queda vacía (todos los paréntesis tienen su par)
    return len(pila) == 0

# Versión alternativa usando NumPy para contar
def validar_parentesis_numpy(secuencia):
    """
    Valida si una secuencia de paréntesis es válida usando NumPy para contar.
    
    Args:
        secuencia (str): Cadena que contiene solo paréntesis ( y )
        
    Returns:
        bool: True si la secuencia es válida, False en caso contrario
    """
    # Verificar que solo contenga paréntesis
    if any(char not in '()' for char in secuencia):
        return False
    
    # Convertir a un array de NumPy donde ( es 1 y ) es -1
    arr = np.array([1 if char == '(' else -1 for char in secuencia])
    
    # Calcular la suma acumulativa
    sumas = np.cumsum(arr)
    
    # La secuencia es válida si:
    # 1. La suma final es 0 (igual número de aperturas y cierres)
    # 2. Nunca hay más cierres que aperturas (la suma nunca es negativa)
    return np.all(sumas >= 0) and sumas[-1] == 0 if len(sumas) > 0 else True

# Función de prueba para ejecutar directamente este script
def main():
    print("Validación de Secuencia de Paréntesis")
    secuencia = input("Ingrese una secuencia de paréntesis (solo '(' y ')'): ")
    
    # Validar usando el método de la pila
    if validar_parentesis(secuencia):
        print("La secuencia de paréntesis es válida.")
    else:
        print("La secuencia de paréntesis no es válida.")

if __name__ == "__main__":
    main()