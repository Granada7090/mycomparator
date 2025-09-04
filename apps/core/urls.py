from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('paquete/', views.buscar_paquete, name='buscar_paquete'),
    path('checkout/iniciar/', views.iniciar_checkout, name='iniciar_checkout'),
    path('checkout/<int:reserva_id>/', views.proceso_checkout, name='proceso_checkout'),
    path('reserva/confirmacion/<int:reserva_id>/', views.confirmacion_reserva, name='confirmacion_reserva'),
    path('mis-reservas/', views.mis_reservas, name='mis_reservas'),
    path('reserva/<int:reserva_id>/', views.detalle_reserva, name='detalle_reserva'),
]
