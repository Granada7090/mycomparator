from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from apps.core.models import BaseModel

class Usuario(AbstractUser):
    """Modelo de usuario personalizado."""
    telefono = models.CharField(
        max_length=15, 
        blank=True,
        null=True,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Formato de teléfono inválido.")]
    )
    fecha_nacimiento = models.DateField(null=True, blank=True)
    preferencias = models.JSONField(default=dict, blank=True)
    
    # Campos de auditoría (en lugar de heredar de BaseModel)
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')
    activo = models.BooleanField(default=True, verbose_name='Activo')
    
    class Meta:
        db_table = 'usuarios'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return self.email or self.username
    
    def delete(self, *args, **kwargs):
        """Eliminación lógica."""
        self.activo = False
        self.save()
    
    def hard_delete(self, *args, **kwargs):
        """Eliminación física."""
        super().delete(*args, **kwargs)
