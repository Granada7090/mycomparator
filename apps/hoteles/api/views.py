from django.http import JsonResponse
from django.views import View
from django.core.cache import cache
import logging
from apps.affiliates.interfaces.travelpayouts import TravelPayoutsInterface

logger = logging.getLogger(__name__)

class APIBuscarHotelesView(View):
    """API endpoint para búsqueda de hoteles"""
    
    def get(self, request):
        # Obtener parámetros de la query string
        destino = request.GET.get('destino')
        fecha_entrada = request.GET.get('fecha_entrada')
        fecha_salida = request.GET.get('fecha_salida')
        adultos = int(request.GET.get('adultos', 2))
        niños = int(request.GET.get('ninos', 0))
        habitaciones = int(request.GET.get('habitaciones', 1))
        ordenar_por = request.GET.get('ordenar_por', 'precio')
        
        # Validar parámetros requeridos
        if not all([destino, fecha_entrada, fecha_salida]):
            return JsonResponse({'error': 'Parámetros requeridos: destino, fecha_entrada, fecha_salida'}, status=400)
        
        # Realizar búsqueda con TravelPayouts
        interface = TravelPayoutsInterface()
        
        hoteles = interface.search_hotels(
            destination=destino,
            check_in=fecha_entrada,
            check_out=fecha_salida,
            adults=adultos,
            children=niños,
            rooms=habitaciones,
            currency='EUR'
        )
        
        # Ordenar resultados
        if ordenar_por == 'precio':
            hoteles.sort(key=lambda x: x['price'])
        elif ordenar_por == 'estrellas':
            hoteles.sort(key=lambda x: x['stars'], reverse=True)
        elif ordenar_por == 'rating':
            hoteles.sort(key=lambda x: x['rating'], reverse=True)
        
        return JsonResponse({
            'success': True,
            'results': hoteles,
            'count': len(hoteles)
        })
