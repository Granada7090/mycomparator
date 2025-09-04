from django.urls import path
from . import views

app_name = 'affiliates'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('stats/', views.stats, name='stats'),
]
