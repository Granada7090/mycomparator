#!/usr/bin/env python3
"""
Script para probar la conexión con TravelPayouts
"""
import os
import sys
import django
from pathlib import Path

# Configurar Django
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.affiliates.interfaces.travelpayouts import TravelPayoutsInterface

def test_connection():
    """Probar la conexión con TravelPayouts"""
    print("🔍 Probando conexión con TravelPayouts...")
    
    # Crear instancia del cliente
    client = TravelPayoutsInterface()
    
    print(f"📋 Configuración:")
    print(f"   API Key: {client.api_key[:10]}... (oculta por seguridad)")
    print(f"   Base URL: {client.base_url}")
    print(f"   Marker: {client.marker}")
    print(f"   Host: {client.host}")
    
    # Probar obtención de aeropuertos
    print("\n🛫 Probando obtención de aeropuertos...")
    airports = client.get_airports()
    
    if airports:
        print(f"✅ Success! Se obtuvieron {len(airports)} aeropuertos")
        print(f"   Primer aeropuerto: {airports[0]['name']} ({airports[0]['code']})")
    else:
        print("❌ Error: No se pudieron obtener aeropuertos")
        return False
    
    # Probar búsqueda de vuelos simple
    print("\n✈️  Probando búsqueda de vuelos (MAD-BCN)...")
    flights = client.search_flights(
        origin="MAD",
        destination="BCN",
        departure_date="2024-02-15"
    )
    
    if flights:
        print("✅ Success! Se obtuvieron resultados de búsqueda")
        print(f"   Tipo de respuesta: {type(flights)}")
        if isinstance(flights, dict) and 'data' in flights:
            print(f"   Número de resultados: {len(flights.get('data', []))}")
    else:
        print("⚠️  Búsqueda devolvió None (puede ser normal si no hay datos)")
    
    # Probar creación de URL de booking
    print("\n🔗 Probando creación de URL de booking...")
    search_data = {
        'origin': 'MAD',
        'destination': 'BCN',
        'departure_date': '2024-02-15',
        'adults': 1,
        'currency': 'EUR'
    }
    
    booking_url = client.create_booking_url(search_data)
    print(f"✅ URL de booking: {booking_url}")
    
    print("\n🎉 ¡Prueba completada!")
    return True

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)