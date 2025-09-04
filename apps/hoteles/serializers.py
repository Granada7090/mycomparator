from rest_framework import serializers
from .models import Hotel, HabitacionTipo, Habitacion, TarifaHabitacion, HotelImagen, ServicioHotel, HotelServicio

class HotelImagenSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelImagen
        fields = ['id', 'imagen', 'descripcion', 'es_principal']

class ServicioHotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicioHotel
        fields = ['id', 'nombre', 'descripcion', 'precio_adicional']

class HotelServicioSerializer(serializers.ModelSerializer):
    servicio = ServicioHotelSerializer(read_only=True)
    
    class Meta:
        model = HotelServicio
        fields = ['id', 'servicio', 'disponible', 'precio']

class HabitacionTipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HabitacionTipo
        fields = ['id', 'nombre', 'descripcion', 'capacidad_adultos', 'capacidad_ninos', 
                 'metros_cuadrados', 'tiene_balcon', 'tiene_vista', 'tiene_caja_fuerte',
                 'tiene_minibar', 'tiene_aire_acondicionado', 'tiene_calefaccion', 'tiene_television']

class TarifaHabitacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TarifaHabitacion
        fields = ['id', 'fecha_inicio', 'fecha_fin', 'precio_noche', 'moneda', 
                 'disponible', 'impuestos', 'cargos_adicionales', 'precio_total']

class HabitacionSerializer(serializers.ModelSerializer):
    tipo = HabitacionTipoSerializer(read_only=True)
    tarifas = TarifaHabitacionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Habitacion
        fields = ['id', 'numero', 'piso', 'disponible', 'tipo', 'tarifas']

class HotelSerializer(serializers.ModelSerializer):
    imagenes = HotelImagenSerializer(many=True, read_only=True)
    servicios = HotelServicioSerializer(many=True, read_only=True)
    habitaciones = HabitacionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Hotel
        fields = ['id', 'nombre', 'direccion', 'ciudad', 'pais', 'codigo_postal',
                 'telefono', 'email', 'sitio_web', 'latitud', 'longitud', 'categoria',
                 'tiene_piscina', 'tiene_spa', 'tiene_gimnasio', 'tiene_wifi',
                 'tiene_estacionamiento', 'admite_mascotas', 'check_in', 'check_out',
                 'descripcion', 'imagenes', 'servicios', 'habitaciones', 'creado_en', 'actualizado_en']

class HotelListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listas de hoteles."""
    imagen_principal = serializers.SerializerMethodField()
    
    class Meta:
        model = Hotel
        fields = ['id', 'nombre', 'ciudad', 'pais', 'categoria', 'latitud', 'longitud', 'imagen_principal']
    
    def get_imagen_principal(self, obj):
        imagen_principal = obj.imagenes.filter(es_principal=True).first()
        if imagen_principal:
            return self.context['request'].build_absolute_uri(imagen_principal.imagen.url)
        return None

class BusquedaHotelSerializer(serializers.Serializer):
    """Serializer para parámetros de búsqueda de hoteles."""
    destino = serializers.CharField(required=True)
    fecha_entrada = serializers.DateField(required=True)
    fecha_salida = serializers.DateField(required=True)
    huespedes = serializers.IntegerField(min_value=1, max_value=10, default=2)
    habitaciones = serializers.IntegerField(min_value=1, max_value=5, default=1)
    
    def validate(self, data):
        if data['fecha_entrada'] >= data['fecha_salida']:
            raise serializers.ValidationError("La fecha de entrada debe ser anterior a la fecha de salida.")
        return data
