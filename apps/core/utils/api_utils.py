import os
import requests
import json
from django.conf import settings
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

def get_travelpayouts_hoteles(destino, fecha_entrada, fecha_salida, adultos=2, ninos=0, habitaciones=1):
    """
    Obtener hoteles reales de TravelPayouts API
    Docs: https://travelpayouts.github.io/slate/#hotels
    """
    try:
        api_key = getattr(settings, 'TRAVELPAYOUTS_API_KEY', 'demo')
        marker = getattr(settings, 'TRAVELPAYOUTS_MARKER', '12345')
        
        # Para desarrollo, usar datos simulados si no hay API key
        if api_key == 'demo':
            from apps.hoteles.api.views import simular_busqueda_hoteles
            return simular_busqueda_hoteles(destino, fecha_entrada, fecha_salida, adultos)
        
        url = "https://engine.hotellook.com/api/v2/search/start.json"
        params = {
            'destination': destino,
            'checkIn': fecha_entrada,
            'checkOut': fecha_salida,
            'adults': adultos,
            'children': ninos,
            'rooms': habitaciones,
            'token': api_key,
            'marker': marker
        }
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        search_data = response.json()
        search_id = search_data.get('searchId')
        
        # Obtener resultados (polling)
        results_url = "https://engine.hotellook.com/api/v2/search/getResult.json"
        results_params = {
            'searchId': search_id,
            'token': api_key
        }
        
        # Esperar resultados (simplificado para demo)
        import time
        time.sleep(2)
        
        results_response = requests.get(results_url, params=results_params, timeout=30)
        results_response.raise_for_status()
        
        return results_response.json().get('hotels', [])
        
    except Exception as e:
        logger.error(f"Error TravelPayouts API: {str(e)}")
        # Fallback a datos simulados
        from apps.hoteles.api.views import simular_busqueda_hoteles
        return simular_busqueda_hoteles(destino, fecha_entrada, fecha_salida, adultos)

def get_amadeus_vuelos(origen, destino, fecha_ida, fecha_vuelta=None, adultos=1, ninos=0):
    """
    Obtener vuelos reales de Amadeus API
    Docs: https://developers.amadeus.com/self-service/category/flights
    """
    try:
        client_id = getattr(settings, 'AMADEUS_CLIENT_ID', 'demo')
        client_secret = getattr(settings, 'AMADEUS_CLIENT_SECRET', 'demo')
        
        # Para desarrollo, usar datos simulados si no hay API key
        if client_id == 'demo':
            from apps.vuelos.api.views import simular_busqueda_vuelos
            return simular_busqueda_vuelos(origen, destino, fecha_ida, fecha_vuelta, adultos)
        
        # Obtener token de acceso
        auth_url = "https://test.api.amadeus.com/v1/security/oauth2/token"
        auth_data = {
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret
        }
        
        auth_response = requests.post(auth_url, data=auth_data, timeout=30)
        auth_response.raise_for_status()
        
        access_token = auth_response.json().get('access_token')
        
        # Buscar vuelos
        search_url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
        headers = {'Authorization': f'Bearer {access_token}'}
        
        params = {
            'originLocationCode': origen,
            'destinationLocationCode': destino,
            'departureDate': fecha_ida,
            'adults': adultos,
            'children': ninos,
            'max': 20
        }
        
        if fecha_vuelta:
            params['returnDate'] = fecha_vuelta
        
        search_response = requests.get(search_url, headers=headers, params=params, timeout=30)
        search_response.raise_for_status()
        
        return search_response.json().get('data', [])
        
    except Exception as e:
        logger.error(f"Error Amadeus API: {str(e)}")
        # Fallback a datos simulados
        from apps.vuelos.api.views import simular_busqueda_vuelos
        return simular_busqueda_vuelos(origen, destino, fecha_ida, fecha_vuelta, adultos)

def get_rapidapi_vuelos(origen, destino, fecha_ida, fecha_vuelta=None, adultos=1):
    """
    Backup con RapidAPI (Skyscanner, etc.)
    """
    try:
        rapidapi_key = getattr(settings, 'RAPIDAPI_KEY', 'demo')
        
        if rapidapi_key == 'demo':
            from apps.vuelos.api.views import simular_busqueda_vuelos
            return simular_busqueda_vuelos(origen, destino, fecha_ida, fecha_vuelta, adultos)
        
        url = "https://skyscanner-api.p.rapidapi.com/v3/flights/search"
        
        headers = {
            'X-RapidAPI-Key': rapidapi_key,
            'X-RapidAPI-Host': 'skyscanner-api.p.rapidapi.com'
        }
        
        payload = {
            "query": {
                "market": "ES",
                "locale": "es-ES",
                "currency": "EUR",
                "queryLegs": [
                    {
                        "originPlace": {"query": origen},
                        "destinationPlace": {"query": destino},
                        "date": {"year": int(fecha_ida[:4]), "month": int(fecha_ida[5:7]), "day": int(fecha_ida[8:10])}
                    }
                ],
                "adults": adultos,
                "cabinClass": "CABIN_CLASS_ECONOMY"
            }
        }
        
        if fecha_vuelta:
            payload["query"]["queryLegs"].append({
                "originPlace": {"query": destino},
                "destinationPlace": {"query": origen},
                "date": {"year": int(fecha_vuelta[:4]), "month": int(fecha_vuelta[5:7]), "day": int(fecha_vuelta[8:10])}
            })
        
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        
        return response.json().get('content', {}).get('results', {})
        
    except Exception as e:
        logger.error(f"Error RapidAPI: {str(e)}")
        from apps.vuelos.api.views import simular_busqueda_vuelos
        return simular_busqueda_vuelos(origen, destino, fecha_ida, fecha_vuelta, adultos)
