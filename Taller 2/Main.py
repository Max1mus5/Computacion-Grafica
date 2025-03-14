import numpy as np
import os
import sys

# Importar funciones de cada ejercicio
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from Ejercicio1 import realizar_operacion
from Ejercicio2 import filtrar_pares
from Ejercicio3 import celsius_a_fahrenheit
from Ejercicio4 import convertir_calificaciones
from Ejercicio5 import contar_palabras
from Ejercicio6 import buscar_elemento
from Ejercicio7 import validar_parentesis
from Ejercicio8 import ordenar_tuplas
from Ejercicio9 import generar_contrasena
from Ejercicio10 import gestionar_agenda

def mostrar_menu():
    """Muestra el menú principal con todas las opciones disponibles."""
    print("\n" + "=" * 50)
    print("MENÚ PRINCIPAL - TALLER 2 PYTHON")
    print("=" * 50)
    print("1. Operaciones Básicas (Calculadora)")
    print("2. Filtrado de Lista por Números Pares")
    print("3. Conversión de Temperaturas de Celsius a Fahrenheit")
    print("4. Sistema de Calificaciones a Letras")
    print("5. Conteo de Palabras en una Cadena")
    print("6. Búsqueda de Elemento en Lista")
    print("7. Validación de Secuencia de Paréntesis")
    print("8. Ordenamiento Personalizado de Lista de Tuplas")
    print("9. Generador de Contraseñas Aleatorias")
    print("10. Gestión de Agenda Telefónica")
    print("11. Salir del Programa")
    print("=" * 50)

def ejecutar_menu():
    """Ejecuta el menú interactivo que permite al usuario elegir diferentes opciones."""
    while True:
        mostrar_menu()
        try:
            opcion = int(input("\nSeleccione una opción (1-11): "))
            
            if opcion == 1:
                print("\n--- Calculadora Básica ---")
                num1 = float(input("Ingrese el primer número: "))
                num2 = float(input("Ingrese el segundo número: "))
                op = input("Ingrese la operación (+, -, *, /): ")
                resultado = realizar_operacion(num1, num2, op)
                if resultado is not None:
                    print(f"Resultado: {resultado}")
                
            elif opcion == 2:
                print("\n--- Filtrado de Lista por Números Pares ---")
                entrada = input("Ingrese una lista de números separados por espacios: ")
                numeros = [int(x) for x in entrada.split()]
                pares = filtrar_pares(numeros)
                print(f"Números pares: {pares}")
                
            elif opcion == 3:
                print("\n--- Conversión de Temperaturas de Celsius a Fahrenheit ---")
                entrada = input("Ingrese temperaturas en Celsius separadas por espacios: ")
                temperaturas = [float(x) for x in entrada.split()]
                fahrenheit = celsius_a_fahrenheit(temperaturas)
                print(f"Temperaturas en Fahrenheit: {fahrenheit}")
                
            elif opcion == 4:
                print("\n--- Sistema de Calificaciones a Letras ---")
                entrada = input("Ingrese calificaciones numéricas separadas por espacios: ")
                calificaciones = [float(x) for x in entrada.split()]
                letras = convertir_calificaciones(calificaciones)
                print("Calificaciones convertidas a letras:")
                for i, letra in enumerate(letras):
                    print(f"Calificación {calificaciones[i]}: {letra}")
                
            elif opcion == 5:
                print("\n--- Conteo de Palabras en una Cadena ---")
                texto = input("Ingrese un texto: ")
                conteo = contar_palabras(texto)
                print("Conteo de palabras:")
                for palabra, cantidad in conteo.items():
                    print(f"'{palabra}': {cantidad}")
                
            elif opcion == 6:
                print("\n--- Búsqueda de Elemento en Lista ---")
                entrada = input("Ingrese una lista de elementos separados por espacios: ")
                lista = entrada.split()
                elemento = input("Ingrese el elemento a buscar: ")
                indice = buscar_elemento(lista, elemento)
                if indice != -1:
                    print(f"El elemento '{elemento}' se encuentra en la posición {indice}.")
                else:
                    print(f"El elemento '{elemento}' no se encuentra en la lista.")
                
            elif opcion == 7:
                print("\n--- Validación de Secuencia de Paréntesis ---")
                secuencia = input("Ingrese una secuencia de paréntesis (solo '(' y ')'): ")
                if validar_parentesis(secuencia):
                    print("La secuencia de paréntesis es válida.")
                else:
                    print("La secuencia de paréntesis no es válida.")
                
            elif opcion == 8:
                print("\n--- Ordenamiento Personalizado de Lista de Tuplas ---")
                personas = []
                n = int(input("Ingrese la cantidad de personas: "))
                for i in range(n):
                    nombre = input(f"Ingrese el nombre de la persona {i+1}: ")
                    edad = int(input(f"Ingrese la edad de {nombre}: "))
                    personas.append((nombre, edad))
                
                ordenados = ordenar_tuplas(personas)
                print("\nLista ordenada por edad y nombre:")
                for persona in ordenados:
                    print(f"Nombre: {persona[0]}, Edad: {persona[1]}")
                
            elif opcion == 9:
                print("\n--- Generador de Contraseñas Aleatorias ---")
                longitud = int(input("Ingrese la longitud deseada para la contraseña: "))
                contrasena = generar_contrasena(longitud)
                print(f"Contraseña generada: {contrasena}")
                
            elif opcion == 10:
                print("\n--- Gestión de Agenda Telefónica ---")
                gestionar_agenda()
                
            elif opcion == 11:
                print("\nGracias por utilizar el programa. ¡Hasta pronto!")
                break
                
            else:
                print("\nOpción no válida. Por favor, seleccione una opción entre 1 y 11.")
                
        except ValueError:
            print("\nError: Ingrese un número válido.")
        
        input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    ejecutar_menu()