from django.contrib import admin
from .models import Aeropuerto, Aerolinea, Vuelo, BusquedaVuelo

@admin.register(Aeropuerto)
class AeropuertoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'ciudad', 'pais', 'codigo_iata', 'codigo_icao']
    list_filter = ['pais', 'ciudad']
    search_fields = ['nombre', 'ciudad', 'codigo_iata', 'codigo_icao']
    ordering = ['ciudad', 'nombre']

@admin.register(Aerolinea)
class AerolineaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'codigo_iata', 'codigo_icao', 'pais']
    list_filter = ['pais']
    search_fields = ['nombre', 'codigo_iata', 'codigo_icao']
    ordering = ['nombre']

@admin.register(Vuelo)
class VueloAdmin(admin.ModelAdmin):
    list_display = ['aerolinea', 'numero_vuelo', 'origen', 'destino', 'fecha_salida', 'precio_base', 'asientos_disponibles']
    list_filter = ['aerolinea', 'origen', 'destino', 'fecha_salida']
    search_fields = ['numero_vuelo', 'aerolinea__nombre', 'origen__ciudad', 'destino__ciudad']
    ordering = ['-fecha_salida']
    date_hierarchy = 'fecha_salida'

@admin.register(BusquedaVuelo)
class BusquedaVueloAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'origen', 'destino', 'fecha_ida', 'fecha_vuelta', 'clase']
    list_filter = ['origen', 'destino', 'fecha_ida', 'clase']
    search_fields = ['usuario__username', 'origen__ciudad', 'destino__ciudad']
    ordering = ['-fecha_creacion']
    date_hierarchy = 'fecha_ida'
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
