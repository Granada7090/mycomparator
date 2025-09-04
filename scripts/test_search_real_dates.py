#!/usr/bin/env python3
"""
Test de búsqueda con fechas reales (no futuras)
"""
import os
import sys
import django
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv

# Configurar Django - CORREGIR la ruta
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
load_dotenv(os.path.join(BASE_DIR, '.env'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.affiliates.interfaces.travelpayouts import TravelPayoutsInterface

def test_with_real_dates():
    print("🔍 Probando búsqueda con fechas REALES...")
    
    client = TravelPayoutsInterface()
    
    # Usar fechas reales (mañana + 2 días) - AÑO ACTUAL
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    return_date = (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d')
    
    print(f"📅 Fechas: {tomorrow} -> {return_date}")
    print(f"📆 Año actual: {datetime.now().year}")
    
    # Probar rutas populares
    routes = [
        ('MAD', 'BCN'),
        ('BCN', 'MAD'), 
        ('MAD', 'LON'),
        ('BCN', 'PMI')
    ]
    
    for origin, destination in routes:
        print(f"\n✈️  Probando: {origin}→{destination}")
        
        resultados = client.search_flights(
            origin=origin,
            destination=destination,
            departure_date=tomorrow,
            return_date=return_date
        )
        
        if resultados and resultados.get('success'):
            num_flights = len(resultados.get('data', []))
            print(f"   ✅ {num_flights} vuelos encontrados")
            if num_flights > 0:
                print(f"   💰 Mejor precio: {resultados['data'][0].get('value', 'N/A')} EUR")
                print(f"   📊 Datos: {resultados['data'][0]}")
        else:
            print("   ❌ No se encontraron resultados")
            if resultados:
                print(f"   📋 Respuesta API: {resultados}")
    
    print("\n🎉 Test completado!")

if __name__ == "__main__":
    test_with_real_dates()
