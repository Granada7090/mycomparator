from django.shortcuts import render, redirect
from django.conf import settings
import requests

def home(request):
    """Página principal - Rediseñada para afiliación"""
    return render(request, 'core/home.html')

def redirect_to_affiliate(request, provider_type, search_id):
    """
    Redirección directa a proveedor afiliado
    provider_type: 'vuelo', 'hotel', 'paquete'
    search_id: ID de la búsqueda o oferta
    """
    # Aquí iría la lógica para construir la URL de afiliado
    # Por ahora, redirección genérica
    affiliate_url = f"https://www.booking.com/searchresults.html"
    
    # Registrar el clic para comisiones (opcional)
    print(f"🔗 Redirección afiliado: {provider_type} - {search_id}")
    
    return redirect(affiliate_url)

def affiliate_webhook(request):
    """Webhook para recibir confirmaciones de comisiones"""
    if request.method == 'POST':
        # Procesar datos de comisión de TravelPayouts
        data = request.POST
        print(f"💰 Comisión recibida: {data}")
        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'error'})
