import numpy as np
import json
import os

# Ejercicio 10: Gestión de Agenda Telefónica 
# Desarrolla un programa que utilice funciones para permitir al usuario agregar, 
# buscar, eliminar y mostrar todos los contactos de una agenda telefónica almacenada 
# en un diccionario.

class AgendaTelefonica:
    """
    Clase para gestionar una agenda telefónica.
    """
    
    def __init__(self):
        """Inicializa una agenda telefónica vacía."""
        self.contactos = {}
        self.archivo = "agenda.json"
        self.cargar_agenda()
    
    def cargar_agenda(self):
        """Carga la agenda desde un archivo si existe."""
        try:
            if os.path.exists(self.archivo):
                with open(self.archivo, 'r') as f:
                    self.contactos = json.load(f)
                print("Agenda cargada correctamente.")
            else:
                print("No se encontró archivo de agenda. Se creará una nueva agenda.")
        except Exception as e:
            print(f"Error al cargar la agenda: {e}")
    
    def guardar_agenda(self):
        """Guarda la agenda en un archivo."""
        try:
            with open(self.archivo, 'w') as f:
                json.dump(self.contactos, f)
            print("Agenda guardada correctamente.")
        except Exception as e:
            print(f"Error al guardar la agenda: {e}")
    
    def agregar_contacto(self, nombre, telefono):
        """
        Agrega un nuevo contacto a la agenda.
        
        Args:
            nombre (str): Nombre del contacto
            telefono (str): Número telefónico
            
        Returns:
            bool: True si se agregó correctamente, False si ya existía
        """
        if nombre in self.contactos:
            print(f"El contacto '{nombre}' ya existe en la agenda.")
            return False
        
        self.contactos[nombre] = telefono
        self.guardar_agenda()
        print(f"Contacto '{nombre}' agregado correctamente.")
        return True
    
    def buscar_contacto(self, nombre):
        """
        Busca un contacto por su nombre.
        
        Args:
            nombre (str): Nombre del contacto a buscar
            
        Returns:
            str or None: Número telefónico si existe, None si no existe
        """
        if nombre in self.contactos:
            return self.contactos[nombre]
        else:
            return None
    
    def eliminar_contacto(self, nombre):
        """
        Elimina un contacto de la agenda.
        
        Args:
            nombre (str): Nombre del contacto a eliminar
            
        Returns:
            bool: True si se eliminó correctamente, False si no existía
        """
        if nombre in self.contactos:
            del self.contactos[nombre]
            self.guardar_agenda()
            print(f"Contacto '{nombre}' eliminado correctamente.")
            return True
        else:
            print(f"El contacto '{nombre}' no existe en la agenda.")
            return False
    
    def mostrar_contactos(self):
        """Muestra todos los contactos de la agenda."""
        if not self.contactos:
            print("La agenda está vacía.")
            return
        
        print("\n=== AGENDA TELEFÓNICA ===")
        print("Nombre\t\tTeléfono")
        print("-" * 30)
        
        # Usar NumPy para ordenar los nombres alfabéticamente
        nombres = np.array(list(self.contactos.keys()))
        nombres_ordenados = np.sort(nombres)
        
        for nombre in nombres_ordenados:
            telefono = self.contactos[nombre]
            # Ajustar espaciado para mejorar visualización
            spacing = "\t" if len(nombre) < 8 else "\t"
            print(f"{nombre}{spacing}{telefono}")
    
    def buscar_por_numero(self, numero):
        """
        Busca contactos por número telefónico.
        
        Args:
            numero (str): Número telefónico a buscar
            
        Returns:
            list: Lista de nombres con ese número telefónico
        """
        coincidencias = []
        for nombre, tel in self.contactos.items():
            if numero in tel:  # Buscar coincidencias parciales
                coincidencias.append(nombre)
        return coincidencias

def mostrar_menu_agenda():
    """Muestra el menú de opciones para la agenda telefónica."""
    print("\n=== MENÚ AGENDA TELEFÓNICA ===")
    print("1. Agregar contacto")
    print("2. Buscar contacto por nombre")
    print("3. Buscar contacto por número")
    print("4. Eliminar contacto")
    print("5. Mostrar todos los contactos")
    print("6. Volver al menú principal")
    print("=" * 30)

def gestionar_agenda():
    """Gestiona la agenda telefónica mediante un menú interactivo."""
    agenda = AgendaTelefonica()
    
    while True:
        mostrar_menu_agenda()
        try:
            opcion = int(input("\nSeleccione una opción (1-6): "))
            
            if opcion == 1:
                nombre = input("Ingrese el nombre del contacto: ")
                telefono = input("Ingrese el número telefónico: ")
                agenda.agregar_contacto(nombre, telefono)
                
            elif opcion == 2:
                nombre = input("Ingrese el nombre a buscar: ")
                telefono = agenda.buscar_contacto(nombre)
                if telefono:
                    print(f"El número de '{nombre}' es: {telefono}")
                else:
                    print(f"No se encontró al contacto '{nombre}'.")
                    
            elif opcion == 3:
                numero = input("Ingrese el número a buscar: ")
                coincidencias = agenda.buscar_por_numero(numero)
                if coincidencias:
                    print(f"Contactos con el número '{numero}':")
                    for nombre in coincidencias:
                        print(f"- {nombre}: {agenda.contactos[nombre]}")
                else:
                    print(f"No se encontraron contactos con el número '{numero}'.")
                    
            elif opcion == 4:
                nombre = input("Ingrese el nombre del contacto a eliminar: ")
                agenda.eliminar_contacto(nombre)
                
            elif opcion == 5:
                agenda.mostrar_contactos()
                
            elif opcion == 6:
                print("Volviendo al menú principal...")
                break
                
            else:
                print("Opción no válida. Por favor, seleccione una opción entre 1 y 6.")
                
        except ValueError:
            print("Error: Ingrese un número válido.")
        
        input("\nPresione Enter para continuar...")

# Función de prueba para ejecutar directamente este script
def main():
    print("Gestión de Agenda Telefónica")
    gestionar_agenda()

if __name__ == "__main__":
    main()