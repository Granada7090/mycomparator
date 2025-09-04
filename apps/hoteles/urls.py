from django.urls import path
from . import views

urlpatterns = [
    path('buscar/', views.buscar_hoteles, name='buscar_hoteles'),
    path('resultados/', views.resultados_hoteles, name='resultados_hoteles'),
    path('webhook/', views.webhook_hoteles, name='webhook_hoteles'),
]
