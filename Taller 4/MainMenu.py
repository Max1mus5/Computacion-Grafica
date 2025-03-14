# Taller número 4. Manejo de Arrays y Operaciones Básicas usando numpy
# Menú principal que integra todos los ejercicios

import numpy as np
import os
import sys

def clear_screen():
    """Limpia la pantalla de la consola."""
    os.system('cls' if os.name == 'nt' else 'clear')

def ejecutar_ejercicio(num_ejercicio):
    """Ejecuta el ejercicio correspondiente al número proporcionado."""
    try:
        # Importamos dinámicamente el módulo del ejercicio
        modulo = __import__(f"Ejercicio{num_ejercicio}")
        # Llamamos a la función principal del ejercicio
        modulo.main()
    except ImportError:
        print(f"Error: No se pudo importar el módulo 'Ejercicio{num_ejercicio}'.")
    except Exception as e:
        print(f"Error al ejecutar el ejercicio {num_ejercicio}: {e}")
    
    input("\nPresione Enter para continuar...")

def mostrar_menu():
    """Muestra el menú de opciones."""
    clear_screen()
    print("=" * 50)
    print("TALLER 4: MANEJO DE ARRAYS Y OPERACIONES BÁSICAS CON NUMPY")
    print("=" * 50)
    print("1. Crear un Array Unidimensional")
    print("2. Crear un Array Multidimensional")
    print("3. Operaciones Básicas con Arrays")
    print("4. Funciones Matemáticas")
    print("5. Indexación y Segmentación")
    print("6. Generación de Datos Aleatorios")
    print("7. Funciones de Agregación")
    print("0. Salir")
    print("=" * 50)

def main():
    """Función principal del programa."""
    while True:
        mostrar_menu()
        
        try:
            opcion = int(input("Seleccione una opción (0-10): "))
            
            if opcion == 0:
                print("¡Gracias por usar el programa! Hasta luego.")
                sys.exit(0)
            elif 1 <= opcion <= 10:
                ejecutar_ejercicio(opcion)
            else:
                print("Opción inválida. Por favor, elija un número entre 0 y 10.")
                input("Presione Enter para continuar...")
        except ValueError:
            print("Por favor, ingrese un número válido.")
            input("Presione Enter para continuar...")

if __name__ == "__main__":
    main()