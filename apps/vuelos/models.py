from django.db import models
from django.conf import settings
from apps.core.models import BaseModel

class Aeropuerto(BaseModel):
    nombre = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)
    codigo_iata = models.CharField(max_length=3, unique=True)
    codigo_icao = models.CharField(max_length=4, unique=True, blank=True, null=True)
    latitud = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitud = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    
    class Meta:
        ordering = ['ciudad', 'nombre']
        verbose_name = 'Aeropuerto'
        verbose_name_plural = 'Aeropuertos'
    
    def __str__(self):
        return f"{self.ciudad} - {self.nombre} ({self.codigo_iata})"

class Aerolinea(BaseModel):
    nombre = models.CharField(max_length=100)
    codigo_iata = models.CharField(max_length=2, unique=True)
    codigo_icao = models.CharField(max_length=3, unique=True, blank=True, null=True)
    pais = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        ordering = ['nombre']
        verbose_name = 'Aerolínea'
        verbose_name_plural = 'Aerolíneas'
    
    def __str__(self):
        return f"{self.nombre} ({self.codigo_iata})"

class Vuelo(BaseModel):
    aerolinea = models.ForeignKey(Aerolinea, on_delete=models.CASCADE, related_name='vuelos')
    numero_vuelo = models.CharField(max_length=10)
    origen = models.ForeignKey(Aeropuerto, on_delete=models.CASCADE, related_name='vuelos_salida')
    destino = models.ForeignKey(Aeropuerto, on_delete=models.CASCADE, related_name='vuelos_llegada')
    fecha_salida = models.DateTimeField()
    fecha_llegada = models.DateTimeField()
    duracion = models.DurationField()
    precio_base = models.DecimalField(max_digits=10, decimal_places=2)
    asientos_disponibles = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['fecha_salida']
        unique_together = ['aerolinea', 'numero_vuelo', 'fecha_salida']
        verbose_name = 'Vuelo'
        verbose_name_plural = 'Vuelos'
    
    def __str__(self):
        return f"{self.aerolinea.codigo_iata}{self.numero_vuelo} - {self.origen.codigo_iata} to {self.destino.codigo_iata}"

class BusquedaVuelo(BaseModel):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='busquedas_vuelos')
    origen = models.ForeignKey(Aeropuerto, on_delete=models.CASCADE, related_name='busquedas_origen')
    destino = models.ForeignKey(Aeropuerto, on_delete=models.CASCADE, related_name='busquedas_destino')
    fecha_ida = models.DateField()
    fecha_vuelta = models.DateField(blank=True, null=True)
    pasajeros_adultos = models.IntegerField(default=1)
    pasajeros_ninos = models.IntegerField(default=0)
    pasajeros_bebes = models.IntegerField(default=0)
    clase = models.CharField(max_length=20, choices=[
        ('economy', 'Economy'),
        ('premium_economy', 'Premium Economy'),
        ('business', 'Business'),
        ('first', 'First Class')
    ], default='economy')
    precio_minimo = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    precio_maximo = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    resultados = models.JSONField(blank=True, null=True)
    
    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = 'Búsqueda de Vuelo'
        verbose_name_plural = 'Búsquedas de Vuelos'
    
    def __str__(self):
        return f"{self.origen.codigo_iata}-{self.destino.codigo_iata} - {self.fecha_ida}"
