from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional

class AffiliateAPI(ABC):
    """
    Clase abstracta para interfaces de APIs de afiliados
    """
    
    @abstractmethod
    def buscar_vuelos(self, origen: str, destino: str, fecha_ida: str, 
                     fecha_vuelta: str = None, pasajeros: int = 1) -> Optional[Dict]:
        """Busca vuelos entre dos aeropuertos"""
        pass
    
    @abstractmethod
    def buscar_hoteles(self, destino: str, fecha_entrada: str, 
                      fecha_salida: str, huespedes: int = 1) -> Optional[Dict]:
        """Busca hoteles en un destino"""
        pass
    
    @abstractmethod
    def obtener_detalle_hotel(self, hotel_id: str) -> Optional[Dict]:
        """Obtiene detalles específicos de un hotel"""
        pass
    
    @abstractmethod
    def obtener_ubicaciones(self, query: str) -> Optional[List[Dict]]:
        """Busca aeropuertos, ciudades y hoteles por nombre"""
        pass
