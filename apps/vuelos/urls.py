from django.urls import path
from . import views

urlpatterns = [
    path('buscar/', views.buscar_vuelos, name='buscar_vuelos'),
    path('resultados/', views.resultados_vuelos, name='resultados_vuelos'),
    path('webhook/', views.webhook_vuelos, name='webhook_vuelos'),
]
