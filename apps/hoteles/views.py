from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from apps.affiliates.interfaces.travelpayouts import TravelPayoutsInterface

def buscar_hoteles(request):
    if request.method == 'POST':
        origen = request.POST.get('origen')
        destino = request.POST.get('destino')
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')
        huespedes = request.POST.get('huespedes', 1)
        habitaciones = request.POST.get('habitaciones', 1)
        
        # Usar TravelPayouts para buscar hoteles reales
        travelpayouts = TravelPayoutsInterface()
        resultados = travelpayouts.buscar_hoteles(
            destino=destino,
            fecha_entrada=check_in,
            fecha_salida=check_out,
            huespedes=int(huespedes)
        )
        
        context = {
            'resultados': resultados,
            'origen': origen,
            'destino': destino,
            'check_in': check_in,
            'check_out': check_out,
            'huespedes': huespedes,
            'habitaciones': habitaciones
        }
        
        return render(request, 'hoteles/resultados.html', context)
    
    return redirect('home')

def resultados_hoteles(request):
    # Esta vista ahora se maneja en buscar_hoteles
    return redirect('home')

@csrf_exempt
@require_POST
def webhook_hoteles(request):
    try:
        data = json.loads(request.body)
        # Procesar webhook de TravelPayouts para hoteles
        print("Webhook hoteles recibido:", data)
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
