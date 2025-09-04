from rest_framework import serializers
from .models import Vuelo, Aeropuerto, BusquedaVuelo

class AeropuertoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aeropuerto
        fields = '__all__'

class VueloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vuelo
        fields = '__all__'

class BusquedaVueloSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusquedaVuelo
        fields = '__all__'
