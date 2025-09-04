"""
Este archivo settings.py es para compatibilidad hacia atrás.
El proyecto ahora usa config/settings/ para la configuración.
"""
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Añadir apps al path
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# Importar configuración según entorno
if os.environ.get('DJANGO_SETTINGS_MODULE'):
    # Ya está configurado por manage.py o servidor
    pass
else:
    # Configuración por defecto para desarrollo
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')

# Importar la configuración real
from django.conf import settings

# Exponer las configuraciones
from config.settings.base import *
