from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from datetime import datetime
import json

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse
from django.core.cache import cache
from django.conf import settings
from datetime import datetime, timedelta
import json
import logging

from .forms import BusquedaHotelForm
from .models import BusquedaHotel, Hotel, Habitacion
from apps.affiliates.interfaces.travelpayouts import TravelPayoutsInterface

logger = logging.getLogger(__name__)

class BuscarHotelesView(View):
    """Vista para búsqueda de hoteles con TravelPayouts"""
    
    template_name = 'hoteles/buscar.html'
    
    def get(self, request):
        form = BusquedaHotelForm()
        
        # Valores por defecto para el formulario
        default_data = {
            'huespedes_adultos': 2,
            'huespedes_ninos': 0,
            'habitaciones': 1,
            'ordenar_por': 'precio'
        }
        
        # Fechas por defecto (mañana y 7 días después)
        tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        next_week = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
        
        context = {
            'form': form,
            'default_data': default_data,
            'fecha_entrada_default': tomorrow,
            'fecha_salida_default': next_week
        }
        
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = BusquedaHotelForm(request.POST)
        
        if form.is_valid():
            # Guardar búsqueda en la base de datos si el usuario está autenticado
            if request.user.is_authenticated:
                busqueda = form.save(commit=False)
                busqueda.usuario = request.user
                busqueda.save()
            
            # Preparar datos para la búsqueda
            destino = form.cleaned_data['destino']
            fecha_entrada = form.cleaned_data['fecha_entrada'].strftime('%Y-%m-%d')
            fecha_salida = form.cleaned_data['fecha_salida'].strftime('%Y-%m-%d')
            adultos = form.cleaned_data['huespedes_adultos']
            niños = form.cleaned_data['huespedes_ninos']
            habitaciones = form.cleaned_data['habitaciones']
            
            # Almacenar datos en sesión para la página de resultados
            request.session['busqueda_hoteles'] = {
                'destino': destino,
                'fecha_entrada': fecha_entrada,
                'fecha_salida': fecha_salida,
                'adultos': adultos,
                'ninos': niños,
                'habitaciones': habitaciones,
                'ordenar_por': form.cleaned_data['ordenar_por']
            }
            
            return redirect('hoteles:resultados')
        
        return render(request, self.template_name, {'form': form})

class ResultadosHotelesView(View):
    """Vista para mostrar resultados de búsqueda de hoteles"""
    
    template_name = 'hoteles/resultados.html'
    
    def get(self, request):
        # Obtener datos de la búsqueda desde la sesión
        busqueda_data = request.session.get('busqueda_hoteles')
        
        if not busqueda_data:
            return redirect('hoteles:buscar')
        
        # Realizar búsqueda con TravelPayouts
        interface = TravelPayoutsInterface()
        
        hoteles = interface.search_hotels(
            destination=busqueda_data['destino'],
            check_in=busqueda_data['fecha_entrada'],
            check_out=busqueda_data['fecha_salida'],
            adults=busqueda_data['adultos'],
            children=busqueda_data['ninos'],
            rooms=busqueda_data['habitaciones'],
            currency='EUR'
        )
        
        # Ordenar resultados según selección del usuario
        if busqueda_data['ordenar_por'] == 'precio':
            hoteles.sort(key=lambda x: x['price'])
        elif busqueda_data['ordenar_por'] == 'estrellas':
