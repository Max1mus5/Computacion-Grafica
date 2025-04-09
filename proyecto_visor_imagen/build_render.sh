#!/bin/bash
# Script para preparar el proyecto Django para Render

echo "Iniciando build del proyecto Django para Render..."

# Actualizar dependencias
echo "Actualizando dependencias..."
pip install -r requirements.txt

# Configurar para producción
echo "Configurando para producción..."

# Crear directorio static si no existe
mkdir -p static

# Recolectar archivos estáticos
echo "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

echo "Build completado con éxito!"