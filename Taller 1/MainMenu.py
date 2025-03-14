# Taller 1\MainMenu.py
# Programa principal con menú interactivo para Física Computacional
# Taller: Caída libre y proyectiles

import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# Añadimos la ruta del proyecto al path para poder importar los módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importamos los ejercicios desde sus respectivas ubicaciones
from Ejercicio1 import calcular_caida_libre
from Ejercicio2 import calcular_tiempo_caida
from Ejercicio3 import calcular_altura_maxima
from Ejercicio4 import calcular_trayectoria_proyectil
from Ejercicio5 import calcular_alcance_horizontal
from Ejercicio6 import calcular_angulo_optimo

def mostrar_menu():
    """
    Muestra el menú principal de opciones del programa
    """
    print("\n===== FÍSICA COMPUTACIONAL EN PYTHON =====")
    print("1. Cálculo de posición y velocidad en caída libre")
    print("2. Cálculo del tiempo de caída desde una altura")
    print("3. Cálculo de altura máxima de un proyectil")
    print("4. Cálculo de trayectoria completa de un proyectil")
    print("5. Cálculo del alcance horizontal de un proyectil")
    print("6. Cálculo del ángulo óptimo para máximo alcance")
    print("7. Salir")
    print("==========================================")

def main():
    """
    Función principal que ejecuta el programa interactivo
    """
    while True:
        mostrar_menu()
        opcion = input("\nSeleccione una opción (1-7): ")
        
        if opcion == '1':
            altura = float(input("Ingrese la altura inicial (m): "))
            tiempo_total = float(input("Ingrese el tiempo total (s): "))
            pasos = int(input("Ingrese el número de pasos de tiempo: "))
            calcular_caida_libre(altura, tiempo_total, pasos)
            
        elif opcion == '2':
            altura = float(input("Ingrese la altura inicial (m): "))
            tiempo = calcular_tiempo_caida(altura)
            print(f"El tiempo de caída es: {tiempo:.2f} segundos")
            
        elif opcion == '3':
            velocidad = float(input("Ingrese la velocidad inicial (m/s): "))
            angulo = float(input("Ingrese el ángulo de lanzamiento (grados): "))
            altura = calcular_altura_maxima(velocidad, angulo)
            print(f"La altura máxima alcanzada es: {altura:.2f} metros")
            
        elif opcion == '4':
            velocidad = float(input("Ingrese la velocidad inicial (m/s): "))
            angulo = float(input("Ingrese el ángulo de lanzamiento (grados): "))
            altura_inicial = float(input("Ingrese la altura inicial (m): "))
            calcular_trayectoria_proyectil(velocidad, angulo, altura_inicial)
            
        elif opcion == '5':
            velocidad = float(input("Ingrese la velocidad inicial (m/s): "))
            angulo = float(input("Ingrese el ángulo de lanzamiento (grados): "))
            altura_inicial = float(input("Ingrese la altura inicial (m): "))
            alcance = calcular_alcance_horizontal(velocidad, angulo, altura_inicial)
            print(f"El alcance horizontal es: {alcance:.2f} metros")
            
        elif opcion == '6':
            velocidad = float(input("Ingrese la velocidad inicial (m/s): "))
            altura_inicial = float(input("Ingrese la altura inicial (m): "))
            angulo = calcular_angulo_optimo(velocidad, altura_inicial)
            print(f"El ángulo óptimo para máximo alcance es: {angulo:.2f} grados")
            
        elif opcion == '7':
            print("Fin Programa")
            break
            
        else:
            print("Opción no válida. Por favor, intente nuevamente.")
        
        input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    main()