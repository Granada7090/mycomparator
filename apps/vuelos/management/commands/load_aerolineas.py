from django.core.management.base import BaseCommand
from apps.vuelos.models import Aerolinea

class Command(BaseCommand):
    help = 'Carga datos de aerolíneas de prueba'

    def handle(self, *args, **options):
        aerolineas = [
            {'nombre': 'Iberia', 'codigo_iata': 'IB', 'codigo_icao': 'IBE', 'pais': 'Spain'},
            {'nombre': 'Vueling', 'codigo_iata': 'VY', 'codigo_icao': 'VLG', 'pais': 'Spain'},
            {'nombre': 'Ryanair', 'codigo_iata': 'FR', 'codigo_icao': 'RYR', 'pais': 'Ireland'},
            {'nombre': 'Air Europa', 'codigo_iata': 'UX', 'codigo_icao': 'AEA', 'pais': 'Spain'},
            {'nombre': 'British Airways', 'codigo_iata': 'BA', 'codigo_icao': 'BAW', 'pais': 'United Kingdom'},
            {'nombre': 'Lufthansa', 'codigo_iata': 'LH', 'codigo_icao': 'DLH', 'pais': 'Germany'},
            {'nombre': 'Air France', 'codigo_iata': 'AF', 'codigo_icao': 'AFR', 'pais': 'France'},
            {'nombre': 'KLM', 'codigo_iata': 'KL', 'codigo_icao': 'KLM', 'pais': 'Netherlands'},
        ]

        for aerolinea_data in aerolineas:
            aerolinea, created = Aerolinea.objects.get_or_create(
                codigo_iata=aerolinea_data['codigo_iata'],
                defaults=aerolinea_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Aerolínea creada: {aerolinea}'))
            else:
                self.stdout.write(self.style.WARNING(f'Aerolínea ya existe: {aerolinea}'))

        self.stdout.write(self.style.SUCCESS('Datos de aerolíneas cargados exitosamente'))
