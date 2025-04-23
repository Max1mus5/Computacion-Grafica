#!/bin/bash

# Verificar si Python está instalado
if ! command -v python &> /dev/null; then
    echo "Python no está instalado. Por favor, instálalo antes de continuar."
    exit 1
fi

# Verificar si pip está instalado
if ! command -v pip &> /dev/null; then
    echo "pip no está instalado. Por favor, instálalo antes de continuar."
    exit 1
fi

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "Creando entorno virtual..."
    python -m venv venv
fi

# Activar entorno virtual
echo "Activando entorno virtual..."
source venv/bin/activate || source venv/Scripts/activate

# Instalar dependencias
echo "Instalando dependencias..."
pip install -r requirements.txt

# Ejecutar servidor Django
echo "Iniciando servidor Django..."
python manage.py runserver

# Desactivar entorno virtual al salir
deactivate