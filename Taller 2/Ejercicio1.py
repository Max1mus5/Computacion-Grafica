import numpy as np

# Ejercicio 1: Calculadora Básica
# Crea una función para cada operación básica (suma, resta, multiplicación, división) 
# que acepte dos argumentos y devuelva el resultado.
# Implementa una función principal que solicite al usuario números y la operación a realizar,
# utilizando las funciones creadas.

def suma(a, b):
    """
    Suma dos números usando NumPy.
    
    Args:
        a (float): Primer número
        b (float): Segundo número
        
    Returns:
        float: Resultado de la suma
    """
    return np.add(a, b)

def resta(a, b):
    """
    Resta dos números usando NumPy.
    
    Args:
        a (float): Primer número
        b (float): Segundo número
        
    Returns:
        float: Resultado de la resta
    """
    return np.subtract(a, b)

def multiplicacion(a, b):
    """
    Multiplica dos números usando NumPy.
    
    Args:
        a (float): Primer número
        b (float): Segundo número
        
    Returns:
        float: Resultado de la multiplicación
    """
    return np.multiply(a, b)

def division(a, b):
    """
    Divide dos números usando NumPy.
    
    Args:
        a (float): Primer número (dividendo)
        b (float): Segundo número (divisor)
        
    Returns:
        float: Resultado de la división
    """
    if b == 0:
        print("Error: No se puede dividir por cero.")
        return None
    return np.divide(a, b)

def realizar_operacion(num1, num2, operacion):
    """
    Realiza una operación matemática básica según la operación especificada.
    
    Args:
        num1 (float): Primer número
        num2 (float): Segundo número
        operacion (str): Operación a realizar (+, -, *, /)
        
    Returns:
        float: Resultado de la operación
    """
    if operacion == '+':
        return suma(num1, num2)
    elif operacion == '-':
        return resta(num1, num2)
    elif operacion == '*':
        return multiplicacion(num1, num2)
    elif operacion == '/':
        return division(num1, num2)
    else:
        print("Error: Operación no válida. Use +, -, *, /")
        return None

# Función de prueba para ejecutar directamente este script
def main():
    print("Calculadora Básica")
    try:
        num1 = float(input("Ingrese el primer número: "))
        num2 = float(input("Ingrese el segundo número: "))
        operacion = input("Ingrese la operación (+, -, *, /): ")
        
        resultado = realizar_operacion(num1, num2, operacion)
        if resultado is not None:
            print(f"Resultado: {resultado}")
            
    except ValueError:
        print("Error: Ingrese números válidos.")

if __name__ == "__main__":
    main()