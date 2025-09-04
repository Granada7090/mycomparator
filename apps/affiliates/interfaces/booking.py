import requests
from django.conf import settings
from .abstract import AffiliateAPI
import logging

logger = logging.getLogger(__name__)

class BookingAPI(AffiliateAPI):
    """Implementación de la API de Booking.com"""
    
    def __init__(self):
        api_key = getattr(settings, 'BOOKING_API_KEY', None)
        base_url = "https://api.booking.com"
        super().__init__(api_key, base_url)
    
    def setup_session(self):
        """Configurar sesión con headers por defecto"""
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {self.api_key}',
            'Accept': 'application/json'
        })
    
    def buscar_vuelos(self, origen, destino, fecha_salida, fecha_regreso=None, pasajeros=1, clase='economy'):
        """Booking.com no ofrece API de vuelos directamente"""
        logger.warning("Booking.com no tiene API pública para vuelos")
        return None
    
    def buscar_hoteles(self, destino, check_in, check_out, huespedes=1, habitaciones=1):
        """Buscar hoteles usando Booking.com"""
        if not self.api_key:
            logger.warning("Booking API key no configurada")
            return None
        
        try:
            endpoint = f"{self.base_url}/v1/hotels"
            params = {
                'checkin': check_in,
                'checkout': check_out,
                'adults': huespedes,
                'rooms': habitaciones,
                'dest_type': 'city',
                'dest_id': destino,  # Esto debería ser el ID de destino de Booking
                'order_by': 'price',
                'rows': 100
            }
            
            response = self.session.get(endpoint, params=params, timeout=30)
            response.raise_for_status()
            
            return response.json()
            
        except requests.RequestException as e:
            return self.handle_error(e, {'destino': destino})
    
    def get_detalle_vuelo(self, vuelo_id):
        """Booking.com no ofrece API de vuelos directamente"""
        return None
    
    def get_detalle_hotel(self, hotel_id):
        """Obtener detalles de un hotel específico"""
        if not self.api_key:
            return None
        
        try:
            endpoint = f"{self.base_url}/v1/hotels/{hotel_id}"
            response = self.session.get(endpoint, timeout=30)
            response.raise_for_status()
            
            return response.json()
            
        except requests.RequestException as e:
            return self.handle_error(e, {'hotel_id': hotel_id})
