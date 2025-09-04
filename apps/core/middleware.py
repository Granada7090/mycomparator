from django.http import HttpResponse
from django.conf import settings
import ipaddress

class MaintenanceModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # IPs permitidas (TravelPayouts + tu IP)
        allowed_ips = [
            '52.28.132.157',    # TravelPayouts API
            '52.28.132.158',    # TravelPayouts Webhook
            '52.28.132.159',    # TravelPayouts
            '172.20.10.2',      # Tu IP local
            # Agrega aquí tu IP pública actual
        ]
        
        # URLs que siempre deben funcionar (APIs, webhooks)
        api_paths = [
            '/api/',
            '/webhook/',
            '/travelpayouts/',
            '/affiliates/',
        ]
        
        client_ip = self.get_client_ip(request)
        
        # Permitir acceso a APIs y TravelPayouts
        if any(request.path.startswith(path) for path in api_paths):
            return self.get_response(request)
            
        # Permitir IPs autorizadas
        if client_ip in allowed_ips:
            return self.get_response(request)
            
        # Para todos los demás: modo mantenimiento
        return HttpResponse(self.maintenance_page(), status=503)
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def maintenance_page(self):
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>MyComparator - Próximamente</title>
            <style>
                body { 
                    font-family: Arial, sans-serif; 
                    text-align: center; 
                    padding: 50px; 
                    background: linear-gradient(135deg, #ff7e00, #ffaa00);
                    color: white;
                }
                .logo { font-size: 3em; font-weight: bold; margin-bottom: 20px; }
                .message { font-size: 1.5em; margin: 30px 0; }
                .countdown { font-size: 2em; margin: 20px 0; }
            </style>
        </head>
        <body>
            <div class="logo">🌍 MyComparator.net</div>
            <div class="message">🚀 Estamos preparando algo increíble</div>
            <div class="countdown">📍 Próximamente...</div>
            <p>Comparador de vuelos y hoteles con los mejores precios</p>
        </body>
        </html>
        """
