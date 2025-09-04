#!/usr/bin/env python3
"""
Test de diferentes endpoints de TravelPayouts
"""
import os
import sys
import django
import requests
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv

# Configurar Django
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
load_dotenv(os.path.join(BASE_DIR, '.env'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

def test_endpoints():
    api_key = os.getenv('TRAVELPAYOUTS_API_KEY')
    headers = {'X-Access-Token': api_key}
    
    # Endpoints a probar
    endpoints = [
        {
            'name': 'Week Matrix',
            'url': 'https://api.travelpayouts.com/v2/prices/week-matrix',
            'params': {'currency': 'EUR', 'origin': 'MAD', 'destination': 'BCN', 'show_to_affiliates': 'true'}
        },
        {
            'name': 'Cheap Tickets', 
            'url': 'https://api.travelpayouts.com/v1/prices/cheap',
            'params': {'currency': 'EUR', 'origin': 'MAD', 'destination': 'BCN'}
        },
        {
            'name': 'Month Matrix',
            'url': 'https://api.travelpayouts.com/v2/prices/month-matrix', 
            'params': {'currency': 'EUR', 'origin': 'MAD', 'destination': 'BCN', 'show_to_affiliates': 'true'}
        }
    ]
    
    print("🔍 Probando diferentes endpoints de TravelPayouts...")
    
    for endpoint in endpoints:
        print(f"\n📡 Probando: {endpoint['name']}")
        try:
            response = requests.get(endpoint['url'], params=endpoint['params'], headers=headers, timeout=30)
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   Success: {data.get('success', 'Unknown')}")
                if 'data' in data:
                    print(f"   Results: {len(data.get('data', []))}")
                print(f"   Response: {data}")
            else:
                print(f"   Error: {response.text}")
        except Exception as e:
            print(f"   Exception: {e}")

if __name__ == "__main__":
    test_endpoints()
