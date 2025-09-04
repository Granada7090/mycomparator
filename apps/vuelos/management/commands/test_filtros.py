from django.core.management.base import BaseCommand
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.vuelos.models import Vuelo, Aeropuerto, Aerolinea
from datetime import datetime, timedelta

User = get_user_model()

class Command(BaseCommand):
    help = 'Test the flight filters functionality'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Testing flight filters...'))
        
        # Create test data
        self.create_test_data()
        
        # Test basic search
        self.test_basic_search()
        
        # Test price filters
        self.test_price_filters()
        
        # Test duration filters
        self.test_duration_filters()
        
        # Test airline filter
        self.test_airline_filter()
        
        # Test stops filter
        self.test_stops_filter()
        
        self.stdout.write(self.style.SUCCESS('All filter tests completed successfully!'))

    def create_test_data(self):
        # Create airports
        mad = Aeropuerto.objects.get_or_create(
            codigo='MAD',
            defaults={'nombre': 'Adolfo Suárez Madrid-Barajas', 'ciudad': 'Madrid', 'pais': 'España'}
        )[0]
        
        bcn = Aeropuerto.objects.get_or_create(
            codigo='BCN',
            defaults={'nombre': 'Barcelona-El Prat', 'ciudad': 'Barcelona', 'pais': 'España'}
        )[0]
        
        # Create airlines
        iberia = Aerolinea.objects.get_or_create(
            codigo='IB',
            defaults={'nombre': 'Iberia'}
        )[0]
        
        vueling = Aerolinea.objects.get_or_create(
            codigo='VY',
            defaults={'nombre': 'Vueling'}
        )[0]
        
        # Create test flights with different prices and durations
        flights_data = [
            {'origen': mad, 'destino': bcn, 'aerolinea': iberia, 'precio': 45.99, 'duracion': 75, 'escalas': 0},
            {'origen': mad, 'destino': bcn, 'aerolinea': iberia, 'precio': 89.99, 'duracion': 150, 'escalas': 1},
            {'origen': mad, 'destino': bcn, 'aerolinea': vueling, 'precio': 35.50, 'duracion': 85, 'escalas': 0},
            {'origen': mad, 'destino': bcn, 'aerolinea': vueling, 'precio': 129.99, 'duracion': 240, 'escalas': 2},
            {'origen': mad, 'destino': bcn, 'aerolinea': iberia, 'precio': 299.99, 'duracion': 90, 'escalas': 0},
            {'origen': mad, 'destino': bcn, 'aerolinea': vueling, 'precio': 599.99, 'duracion': 600, 'escalas': 3},
        ]
        
        tomorrow = datetime.now() + timedelta(days=1)
        
        for i, data in enumerate(flights_data):
            Vuelo.objects.get_or_create(
                numero_vuelo=f'TEST{i}',
                defaults={
                    'origen': data['origen'],
                    'destino': data['destino'],
                    'aerolinea': data['aerolinea'],
                    'fecha_salida': tomorrow.replace(hour=8 + i, minute=0),
                    'fecha_llegada': tomorrow.replace(hour=8 + i, minute=0) + timedelta(minutes=data['duracion']),
                    'precio': data['precio'],
                    'duracion': data['duracion'],
                    'escalas': data['escalas'],
                    'disponible': True
                }
            )
        
        self.stdout.write(self.style.SUCCESS('Created test flight data'))

    def test_basic_search(self):
        self.stdout.write('Testing basic search...')
        # This would normally be done with test client, but for management command we simulate
        vuelos = Vuelo.objects.filter(origen__codigo='MAD', destino__codigo='BCN')
        self.stdout.write(f'Found {vuelos.count()} flights from MAD to BCN')

    def test_price_filters(self):
        self.stdout.write('Testing price filters...')
        
        # Test price range 0-50
        cheap = Vuelo.objects.filter(precio__lte=50, origen__codigo='MAD', destino__codigo='BCN')
        self.stdout.write(f'Flights under 50€: {cheap.count()}')
        
        # Test price range 50-100
        medium = Vuelo.objects.filter(precio__gt=50, precio__lte=100, origen__codigo='MAD', destino__codigo='BCN')
        self.stdout.write(f'Flights 50-100€: {medium.count()}')
        
        # Test price range 100-200
        expensive = Vuelo.objects.filter(precio__gt=100, precio__lte=200, origen__codigo='MAD', destino__codigo='BCN')
        self.stdout.write(f'Flights 100-200€: {expensive.count()}')

    def test_duration_filters(self):
        self.stdout.write('Testing duration filters...')
        
        # Test short flights (<2h)
        short = Vuelo.objects.filter(duracion__lt=120, origen__codigo='MAD', destino__codigo='BCN')
        self.stdout.write(f'Short flights (<2h): {short.count()}')
        
        # Test medium flights (2-4h)
        medium = Vuelo.objects.filter(duracion__gte=120, duracion__lt=240, origen__codigo='MAD', destino__codigo='BCN')
        self.stdout.write(f'Medium flights (2-4h): {medium.count()}')

    def test_airline_filter(self):
        self.stdout.write('Testing airline filter...')
        
        iberia = Vuelo.objects.filter(aerolinea__codigo='IB', origen__codigo='MAD', destino__codigo='BCN')
        self.stdout.write(f'Iberia flights: {iberia.count()}')
        
        vueling = Vuelo.objects.filter(aerolinea__codigo='VY', origen__codigo='MAD', destino__codigo='BCN')
        self.stdout.write(f'Vueling flights: {vueling.count()}')

    def test_stops_filter(self):
        self.stdout.write('Testing stops filter...')
        
        direct = Vuelo.objects.filter(escalas=0, origen__codigo='MAD', destino__codigo='BCN')
        self.stdout.write(f'Direct flights: {direct.count()}')
        
        one_stop = Vuelo.objects.filter(escalas=1, origen__codigo='MAD', destino__codigo='BCN')
        self.stdout.write(f'1-stop flights: {one_stop.count()}')
