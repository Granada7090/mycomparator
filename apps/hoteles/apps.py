from django.apps import AppConfig

class HotelesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.hoteles'
    verbose_name = 'Gestión de Hoteles'
    
    def ready(self):
        # Importar señales si es necesario
        try:
            import apps.hoteles.signals
        except ImportError:
            pass
