from .base import *
import socket

# Configuración de desarrollo
DEBUG = True

# Obtener IP local automáticamente
try:
    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[:-1] + '1' for ip in ips] + ['127.0.0.1', 'localhost']
except:
    INTERNAL_IPS = ['127.0.0.1', 'localhost']

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '172.20.10.2',  # Tu IP local
    '.localhost.run',
    '.serveo.net',
    '.ngrok.io',
]

# Configuración de base de datos
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Configuración de email para desarrollo
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Debug toolbar COMENTADO temporalmente
# if DEBUG:
#     INSTALLED_APPS += ['debug_toolbar']
#     MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
#     DEBUG_TOOLBAR_CONFIG = {
#         'SHOW_TOOLBAR_CALLBACK': lambda request: True,
#     }
