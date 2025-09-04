from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from apps.affiliates.interfaces.travelpayouts import TravelPayoutsInterface

def buscar_vuelos(request):
    if request.method == 'POST':
        origen = request.POST.get('origen')
        destino = request.POST.get('destino')
        fecha_ida = request.POST.get('fecha_ida')
        fecha_vuelta = request.POST.get('fecha_vuelta')
        pasajeros = request.POST.get('pasajeros', 1)
        clase = request.POST.get('clase', 'economy')
        
        # Usar TravelPayouts para buscar vuelos reales
        travelpayouts = TravelPayoutsInterface()
        resultados = travelpayouts.buscar_vuelos(
            origen=origen,
            destino=destino,
            fecha_ida=fecha_ida,
            fecha_vuelta=fecha_vuelta,
            pasajeros=int(pasajeros)
        )
        
        context = {
            'resultados': resultados,
            'origen': origen,
            'destino': destino,
            'fecha_ida': fecha_ida,
            'fecha_vuelta': fecha_vuelta,
            'pasajeros': pasajeros,
            'clase': clase
        }
        
        return render(request, 'vuelos/resultados.html', context)
    
    return redirect('home')

def resultados_vuelos(request):
    # Esta vista ahora se maneja en buscar_vuelos
    return redirect('home')

@csrf_exempt
@require_POST
def webhook_vuelos(request):
    try:
        data = json.loads(request.body)
        # Procesar webhook de TravelPayouts
        print("Webhook recibido:", data)
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
