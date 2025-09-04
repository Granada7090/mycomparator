from django.contrib import admin
from .models import (
    Hotel, HabitacionTipo, Habitacion, TarifaHabitacion,
    HotelImagen, ServicioHotel, HotelServicio, BusquedaHotel
)

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ciudad', 'pais', 'categoria', 'tiene_wifi', 'tiene_piscina')
    list_filter = ('categoria', 'pais', 'ciudad', 'tiene_wifi', 'tiene_piscina', 'tiene_spa')
    search_fields = ('nombre', 'ciudad', 'pais', 'direccion')
    filter_horizontal = ()
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')

@admin.register(HabitacionTipo)
class HabitacionTipoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'capacidad_adultos', 'capacidad_ninos', 'metros_cuadrados')
    list_filter = ('capacidad_adultos', 'capacidad_ninos')
    search_fields = ('nombre', 'descripcion')

@admin.register(Habitacion)
class HabitacionAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'tipo', 'numero', 'piso', 'disponible')
    list_filter = ('hotel', 'tipo', 'disponible', 'piso')
    search_fields = ('numero', 'hotel__nombre')

@admin.register(TarifaHabitacion)
class TarifaHabitacionAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'habitacion_tipo', 'fecha_inicio', 'fecha_fin', 'precio_noche', 'moneda', 'disponible')
    list_filter = ('hotel', 'habitacion_tipo', 'moneda', 'disponible')
    search_fields = ('hotel__nombre', 'habitacion_tipo__nombre')
    date_hierarchy = 'fecha_inicio'

@admin.register(HotelImagen)
class HotelImagenAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'descripcion', 'es_principal')
    list_filter = ('hotel', 'es_principal')
    search_fields = ('hotel__nombre', 'descripcion')

@admin.register(ServicioHotel)
class ServicioHotelAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio_adicional', 'disponible')
    list_filter = ('disponible',)
    search_fields = ('nombre', 'descripcion')

@admin.register(HotelServicio)
class HotelServicioAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'servicio', 'disponible', 'precio')
    list_filter = ('hotel', 'servicio', 'disponible')
    search_fields = ('hotel__nombre', 'servicio__nombre')

@admin.register(BusquedaHotel)
class BusquedaHotelAdmin(admin.ModelAdmin):
    list_display = ('destino', 'fecha_entrada', 'fecha_salida', 'adultos', 'ninos', 'total_resultados', 'usuario')
    list_filter = ('destino', 'fecha_entrada', 'api_utilizada')
    search_fields = ('destino', 'usuario__username')
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')
    date_hierarchy = 'fecha_entrada'
