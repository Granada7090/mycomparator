from django.db import models
from django.conf import settings
import uuid
from django.utils import timezone

class BaseModel(models.Model):
    """
    Modelo base abstracto con campos comunes para todos los modelos
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ['-fecha_creacion']

    def delete(self, *args, **kwargs):
        """Eliminación suave (soft delete)"""
        self.activo = False
        self.save()

class Reserva(BaseModel):
    ESTADOS_RESERVA = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
        ('completada', 'Completada')
    ]
    
    TIPOS_RESERVA = [
        ('vuelo', 'Vuelo'),
        ('hotel', 'Hotel'),
        ('paquete', 'Paquete Vuelo + Hotel')
    ]
    
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPOS_RESERVA)
    estado = models.CharField(max_length=10, choices=ESTADOS_RESERVA, default='pendiente')
    
    # Información general
    origen = models.CharField(max_length=100)
    destino = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    
    # Detalles específicos
    detalles = models.JSONField()  # Almacena toda la información de la reserva
    
    # Información de pago
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)
    moneda = models.CharField(max_length=3, default='EUR')
    codigo_reserva = models.CharField(max_length=20, unique=True)
    
    # Información de TravelPayouts
    travelpayouts_id = models.CharField(max_length=100, blank=True, null=True)
    travelpayouts_link = models.URLField(blank=True, null=True)
    
    class Meta:
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.codigo_reserva} - {self.usuario.username} - {self.tipo}"

    def save(self, *args, **kwargs):
        if not self.codigo_reserva:
            self.codigo_reserva = f"RES-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

class Pasajero(models.Model):
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE, related_name='pasajeros')
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True, null=True)
    fecha_nacimiento = models.DateField()
    documento_identidad = models.CharField(max_length=50)
    
    class Meta:
        ordering = ['nombre', 'apellido']
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Pago(BaseModel):
    ESTADOS_PAGO = [
        ('pendiente', 'Pendiente'),
        ('completado', 'Completado'),
        ('fallido', 'Fallido'),
        ('reembolsado', 'Reembolsado')
    ]
    
    reserva = models.OneToOneField(Reserva, on_delete=models.CASCADE)
    estado = models.CharField(max_length=12, choices=ESTADOS_PAGO, default='pendiente')
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    moneda = models.CharField(max_length=3, default='EUR')
    
    # Información de transacción
    id_transaccion = models.CharField(max_length=100, blank=True, null=True)
    metodo_pago = models.CharField(max_length=50, blank=True, null=True)
    fecha_pago = models.DateTimeField(null=True, blank=True)
    
    # Datos de tarjeta (encriptados en producción)
    ultimos_digitos = models.CharField(max_length=4, blank=True, null=True)
    tipo_tarjeta = models.CharField(max_length=20, blank=True, null=True)
    
    class Meta:
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"Pago {self.id_transaccion} - {self.monto}{self.moneda}"
