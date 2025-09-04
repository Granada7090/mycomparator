from django.core.management.base import BaseCommand
from apps.vuelos.models import Aeropuerto

class Command(BaseCommand):
    help = 'Carga datos de aeropuertos de prueba'

    def handle(self, *args, **options):
        aeropuertos = [
            {
                'nombre': 'Adolfo Suárez Madrid-Barajas',
                'ciudad': 'Madrid',
                'pais': 'Spain',
                'codigo_iata': 'MAD',
                'codigo_icao': 'LEMD',
                'latitud': 40.471926,
                'longitud': -3.56264
            },
            {
                'nombre': 'Barcelona-El Prat',
                'ciudad': 'Barcelona',
                'pais': 'Spain',
                'codigo_iata': 'BCN',
                'codigo_icao': 'LEBL',
                'latitud': 41.297445,
                'longitud': 2.083294
            },
            {
                'nombre': 'Málaga-Costa del Sol',
                'ciudad': 'Málaga',
                'pais': 'Spain',
                'codigo_iata': 'AGP',
                'codigo_icao': 'LEMG',
                'latitud': 36.6749,
                'longitud': -4.499106
            },
            {
                'nombre': 'Palma de Mallorca',
                'ciudad': 'Palma de Mallorca',
                'pais': 'Spain',
                'codigo_iata': 'PMI',
                'codigo_icao': 'LEPA',
                'latitud': 39.55361,
                'longitud': 2.727778
            },
            {
                'nombre': 'Alicante-Elche',
                'ciudad': 'Alicante',
                'pais': 'Spain',
                'codigo_iata': 'ALC',
                'codigo_icao': 'LEAL',
                'latitud': 38.282169,
                'longitud': -0.558156
            },
            {
                'nombre': 'Heathrow',
                'ciudad': 'London',
                'pais': 'United Kingdom',
                'codigo_iata': 'LHR',
                'codigo_icao': 'EGLL',
                'latitud': 51.47002,
                'longitud': -0.454295
            },
            {
                'nombre': 'Charles de Gaulle',
                'ciudad': 'Paris',
                'pais': 'France',
                'codigo_iata': 'CDG',
                'codigo_icao': 'LFPG',
                'latitud': 49.0097,
                'longitud': 2.5479
            },
            {
                'nombre': 'Schiphol',
                'ciudad': 'Amsterdam',
                'pais': 'Netherlands',
                'codigo_iata': 'AMS',
                'codigo_icao': 'EHAM',
                'latitud': 52.308613,
                'longitud': 4.763889
            }
        ]

        for aeropuerto_data in aeropuertos:
            aeropuerto, created = Aeropuerto.objects.get_or_create(
                codigo_iata=aeropuerto_data['codigo_iata'],
                defaults=aeropuerto_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Aeropuerto creado: {aeropuerto}'))
            else:
                self.stdout.write(self.style.WARNING(f'Aeropuerto ya existe: {aeropuerto}'))

        self.stdout.write(self.style.SUCCESS('Datos de aeropuertos cargados exitosamente'))
