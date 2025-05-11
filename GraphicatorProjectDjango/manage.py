#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    # Verificar si se está ejecutando en modo local
    if len(sys.argv) > 2 and sys.argv[2] == "local":
        print("Modo local detectado. Ejecutando versión con Pygame...")
        # Importar y ejecutar la aplicación local
        from GraphicatorProject.local_app import run_local_app
        run_local_app()
        return
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GraphicatorProject.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
