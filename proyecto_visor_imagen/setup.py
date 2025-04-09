#!/usr/bin/env python
"""
Script para configurar el entorno de desarrollo o producción.
"""
import os
import sys
import subprocess

def main():
    """Función principal para configurar el entorno."""
    # Determinar si estamos en desarrollo o producción
    env = os.environ.get('DJANGO_ENV', 'development')
    
    if env == 'production':
        print("Configurando entorno de producción...")
        requirements_file = 'requirements.txt'
    else:
        print("Configurando entorno de desarrollo...")
        requirements_file = 'requirements-dev.txt'
    
    # Instalar dependencias
    print(f"Instalando dependencias desde {requirements_file}...")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', requirements_file])
    
    print("Configuración completada con éxito.")

if __name__ == '__main__':
    main()