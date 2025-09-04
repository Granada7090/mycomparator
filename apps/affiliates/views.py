from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    """Dashboard de afiliados"""
    return render(request, 'affiliates/dashboard.html')

@login_required
def stats(request):
    """Estadísticas de afiliados"""
    return render(request, 'affiliates/stats.html')
