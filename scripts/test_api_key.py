#!/usr/bin/env python3
"""
Test simple para verificar que la API key de TravelPayouts funciona
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def test_api_key():
    api_key = os.getenv('TRAVELPAYOUTS_API_KEY')
    print(f"🔑 API Key: {api_key[:8]}...")
    
    # Test simple de conexión
    test_url = "https://api.travelpayouts.com/data/airports.json"
    
    try:
        response = requests.get(test_url, timeout=10)
        if response.status_code == 200:
            airports = response.json()
            print(f"✅ Conexión exitosa! {len(airports)} aeropuertos obtenidos")
            print(f"   Primer aeropuerto: {airports[0]['name']} ({airports[0]['code']})")
            return True
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

if __name__ == "__main__":
    success = test_api_key()
    exit(0 if success else 1)
