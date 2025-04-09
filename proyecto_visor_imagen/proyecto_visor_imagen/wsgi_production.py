"""
WSGI config for production environment.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyecto_visor_imagen.settings')

application = get_wsgi_application()