#!/bin/bash

# Script de inicio rápido para el Graficador Pygame

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 no está instalado. Por favor, instálalo antes de continuar."
    exit 1
fi

# Verificar si pip está instalado
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 no está instalado. Por favor, instálalo antes de continuar."
    exit 1
fi

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno virtual
echo "Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
echo "Instalando dependencias..."
pip install -r GraphicatorProjectDjango/requirements.txt

# Iniciar el servidor Django
echo "Iniciando el servidor Django..."
cd GraphicatorProjectDjango
python manage.py runserver 0.0.0.0:8000

# Desactivar entorno virtual al salir
deactivate