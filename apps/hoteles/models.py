from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from apps.core.models import BaseModel
import uuid
from datetime import timedelta

class Hotel(BaseModel):
    """Modelo para hoteles."""
    nombre = models.CharField(max_length=200)
    direccion = models.TextField()
    ciudad = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=20, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    sitio_web = models.URLField(blank=True, null=True)
    
    # Información de ubicación
    latitud = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitud = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    
    # Categoría y clasificación
    categoria = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Categoría del hotel (1-5 estrellas)"
    )
    
    # Características
    tiene_piscina = models.BooleanField(default=False)
    tiene_spa = models.BooleanField(default=False)
    tiene_gimnasio = models.BooleanField(default=False)
    tiene_wifi = models.BooleanField(default=False)
    tiene_estacionamiento = models.BooleanField(default=False)
    admite_mascotas = models.BooleanField(default=False)
    
    # Información de check-in/check-out
    check_in = models.TimeField(default='14:00')
    check_out = models.TimeField(default='12:00')
    
    descripcion = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Hotel"
        verbose_name_plural = "Hoteles"
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.nombre} - {self.ciudad}"

class HabitacionTipo(BaseModel):
    """Tipos de habitaciones disponibles."""
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    capacidad_adultos = models.PositiveSmallIntegerField(default=2)
    capacidad_ninos = models.PositiveSmallIntegerField(default=0)
    metros_cuadrados = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    
    # Características de la habitación
    tiene_balcon = models.BooleanField(default=False)
    tiene_vista = models.BooleanField(default=False)
    tiene_caja_fuerte = models.BooleanField(default=False)
    tiene_minibar = models.BooleanField(default=False)
    tiene_aire_acondicionado = models.BooleanField(default=True)
    tiene_calefaccion = models.BooleanField(default=True)
    tiene_television = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Tipo de Habitación"
        verbose_name_plural = "Tipos de Habitaciones"
    
    def __str__(self):
        return self.nombre

class Habitacion(BaseModel):
    """Habitaciones específicas de un hotel."""
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='habitaciones')
    tipo = models.ForeignKey(HabitacionTipo, on_delete=models.PROTECT, related_name='habitaciones')
    numero = models.CharField(max_length=10)
    piso = models.PositiveSmallIntegerField(blank=True, null=True)
    disponible = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Habitación"
        verbose_name_plural = "Habitaciones"
        unique_together = ['hotel', 'numero']
    
    def __str__(self):
        return f"{self.hotel.nombre} - Habitación {self.numero}"

class TarifaHabitacion(BaseModel):
    """Tarifas para tipos de habitación en hoteles."""
    habitacion_tipo = models.ForeignKey(HabitacionTipo, on_delete=models.CASCADE, related_name='tarifas')
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='tarifas')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    precio_noche = models.DecimalField(max_digits=10, decimal_places=2)
    moneda = models.CharField(max_length=3, default='EUR')
    disponible = models.BooleanField(default=True)
    
    # Impuestos y cargos
    impuestos = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    cargos_adicionales = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    
    class Meta:
        verbose_name = "Tarifa de Habitación"
        verbose_name_plural = "Tarifas de Habitaciones"
        ordering = ['fecha_inicio']
    
    def precio_total(self):
        return self.precio_noche + self.impuestos + self.cargos_adicionales
    
    def __str__(self):
        return f"{self.habitacion_tipo.nombre} - {self.hotel.nombre} - {self.precio_noche}{self.moneda}"

class HotelImagen(BaseModel):
    """Imágenes para hoteles."""
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to='hoteles/')
    descripcion = models.CharField(max_length=200, blank=True, null=True)
    es_principal = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Imagen de Hotel"
        verbose_name_plural = "Imágenes de Hoteles"
    
    def __str__(self):
        return f"Imagen de {self.hotel.nombre}"

class ServicioHotel(BaseModel):
    """Servicios adicionales ofrecidos por hoteles."""
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    precio_adicional = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    disponible = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Servicio de Hotel"
        verbose_name_plural = "Servicios de Hoteles"
    
    def __str__(self):
        return self.nombre

class HotelServicio(BaseModel):
    """Relación entre hoteles y servicios."""
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='servicios_adicionales')
    servicio = models.ForeignKey(ServicioHotel, on_delete=models.CASCADE)
    disponible = models.BooleanField(default=True)
    precio = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    
    class Meta:
        verbose_name = "Servicio de Hotel Específico"
        verbose_name_plural = "Servicios de Hoteles Específicos"
        unique_together = ['hotel', 'servicio']
    
    def __str__(self):
        return f"{self.hotel.nombre} - {self.servicio.nombre}"

class BusquedaHotel(BaseModel):
    """Modelo para almacenar búsquedas de hoteles realizadas por usuarios."""
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    destino = models.CharField(max_length=100)
    fecha_entrada = models.DateField()
    fecha_salida = models.DateField()
    adultos = models.PositiveSmallIntegerField(default=2)
    ninos = models.PositiveSmallIntegerField(default=0)
    habitaciones = models.PositiveSmallIntegerField(default=1)
    
    # Filtros de búsqueda
    precio_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    precio_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    categoria_min = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True,
        blank=True
    )
    categoria_max = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True,
        blank=True
    )
    
    # Servicios deseados
    servicios = models.ManyToManyField(ServicioHotel, blank=True)
    
    # Resultados de la búsqueda (almacenados como JSON)
    resultados = models.JSONField(null=True, blank=True)
    total_resultados = models.PositiveIntegerField(default=0)
    
    # Información de la API
    api_utilizada = models.CharField(max_length=50, default='travelpayouts')
    api_response = models.JSONField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Búsqueda de Hotel"
        verbose_name_plural = "Búsquedas de Hoteles"
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"Búsqueda Hotel: {self.destino} - {self.fecha_entrada} a {self.fecha_salida}"

def generar_codigo_reserva():
    """Función para generar código de reserva (evita problemas con lambda)."""
    return uuid.uuid4().hex[:12].upper()

class ReservaHotel(BaseModel):
    """Modelo para reservas de hotel confirmadas (después del pago)."""
    ESTADOS = [
        ('pendiente', 'Pendiente de pago'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
        ('completada', 'Completada'),
    ]
    
    codigo_reserva = models.CharField(max_length=12, unique=True, default=generar_codigo_reserva)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservas_hotel')
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='reservas')
    habitacion_tipo = models.ForeignKey(HabitacionTipo, on_delete=models.PROTECT, null=True, blank=True)
    
    # Datos de la estancia
    fecha_entrada = models.DateField()
    fecha_salida = models.DateField()
    noches = models.PositiveIntegerField(default=1)
    adultos = models.PositiveSmallIntegerField(default=2)
    ninos = models.PositiveSmallIntegerField(default=0)
    habitaciones = models.PositiveSmallIntegerField(default=1)
    
    # Información de pago
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)
    moneda = models.CharField(max_length=3, default='EUR')
    impuestos = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    comision = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    
    # Estado y tracking
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    fecha_pago = models.DateTimeField(null=True, blank=True)
    metodo_pago = models.CharField(max_length=50, blank=True, null=True)
    referencia_pago = models.CharField(max_length=100, blank=True, null=True)
    
    # Información del huésped
    nombre_huesped = models.CharField(max_length=200)
    email_huesped = models.EmailField()
    telefono_huesped = models.CharField(max_length=20, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    
    # Servicios adicionales
    servicios_adicionales = models.ManyToManyField(ServicioHotel, blank=True)
    
    class Meta:
        verbose_name = "Reserva de Hotel"
        verbose_name_plural = "Reservas de Hoteles"
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"Reserva {self.codigo_reserva} - {self.hotel.nombre}"
    
    def save(self, *args, **kwargs):
        # Calcular número de noches automáticamente
        if self.fecha_entrada and self.fecha_salida:
            self.noches = (self.fecha_salida - self.fecha_entrada).days
        super().save(*args, **kwargs)
    
    def generar_codigo_qr(self):
        """Generar código QR con información de la reserva."""
        from django.urls import reverse
        from django.conf import settings
        
        url_verificacion = f"{settings.SITE_URL}{reverse('hoteles:verificar_reserva', kwargs={'codigo': self.codigo_reserva})}"
        datos_qr = f"""
RESERVA HOTEL: {self.codigo_reserva}
Hotel: {self.hotel.nombre}
Check-in: {self.fecha_entrada} a las {self.hotel.check_in}
Check-out: {self.fecha_salida} a las {self.hotel.check_out}
Huésped: {self.nombre_huesped}
Verificar: {url_verificacion}
        """
        return datos_qr.strip()
    
    @property
    def puede_cancelar(self):
        """Verificar si la reserva puede ser cancelada."""
        from django.utils import timezone
        if self.estado != 'confirmada':
            return False
        # Permitir cancelación hasta 24 horas antes del check-in
        return (self.fecha_entrada - timezone.now().date()).days >= 1
    
    @property
    def precio_por_noche(self):
        """Calcular precio por noche."""
        if self.noches > 0:
            return self.precio_total / self.noches
        return self.precio_total
