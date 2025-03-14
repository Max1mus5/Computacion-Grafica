# Taller número 3. Programación Numérica con Python y NumPy.
# Menú principal que integra todos los ejercicios del taller.

import os
import numpy as np
import importlib

def clear_screen():
    """Limpia la pantalla de la consola."""
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    while True:
        clear_screen()
        print("\n===== TALLER 3: PROGRAMACIÓN NUMÉRICA CON PYTHON Y NUMPY =====")
        print("\nMenú de opciones:")
        print("1. Creación y Propiedades de Arrays")
        print("2. Operaciones Básicas")
        print("3. Indexación y Slicing")
        print("4. Broadcasting y Funciones Universales")
        print("5. Manipulación de Formas y Algebra Lineal")
        print("6. Trabajo con Datos Faltantes")
        print("7. Guardar y Cargar Arrays")
        print("0. Salir")
        
        try:
            opcion = int(input("\nSeleccione una opción (0-7): "))
            
            if opcion == 0:
                print("¡Gracias por utilizar el programa!")
                break
            elif opcion >= 1 and opcion <= 7:
                # Importar dinámicamente el módulo correspondiente
                modulo = importlib.import_module(f"Ejercicio{opcion}")
                
                # Ejecutar la función principal del módulo
                modulo.main()
                
                input("\nPresione Enter para volver al menú principal...")
            else:
                print("Opción no válida. Intente nuevamente.")
                input("Presione Enter para continuar...")
        except ValueError:
            print("Por favor, ingrese un número válido.")
            input("Presione Enter para continuar...")
        except ImportError:
            print(f"Error: No se pudo importar el módulo Ejercicio{opcion}.")
            print("Asegúrese de que el archivo correspondiente existe en el mismo directorio.")
            input("Presione Enter para continuar...")
        except Exception as e:
            print(f"Error inesperado: {e}")
            input("Presione Enter para continuar...")

if __name__ == "__main__":
    main()