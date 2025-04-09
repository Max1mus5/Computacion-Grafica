#!/bin/bash
# Script para preparar el proyecto Django para producción

echo "Iniciando build del proyecto Django..."

# Actualizar dependencias
echo "Actualizando dependencias..."
pip install -r requirements.txt

# Configurar para producción
echo "Configurando para producción..."
# Aquí podrías modificar settings.py programáticamente si lo necesitas
# Por ejemplo, cambiar DEBUG = False

# Recolectar archivos estáticos
echo "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

# Ejecutar migraciones
echo "Ejecutando migraciones..."
python manage.py migrate

# Comprimir archivos estáticos (opcional, requiere django-compressor)
# echo "Comprimiendo archivos estáticos..."
# python manage.py compress

echo "Build completado con éxito!"