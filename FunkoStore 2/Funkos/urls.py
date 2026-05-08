"""
URLs de la app Funkos.
Acá registramos las rutas relacionadas con el catálogo, carrito, órdenes, etc.
"""

from django.urls import path
from . import views

# El namespace 'Funkos' permite usar {% url 'Funkos:home' %} en templates
app_name = 'Funkos'

urlpatterns = [
    # Página principal (catálogo)
    path('', views.home, name='home'),

    # Registro de nuevos usuarios
    # Las rutas /accounts/login/ y /accounts/logout/ ya vienen de django.contrib.auth.urls
    # (ver Project/urls.py), por eso solo necesitamos agregar el registro acá.
    path('register/', views.register, name='register'),

    # Zona privada (requiere login)
    path('mi-cuenta/', views.mi_cuenta, name='mi_cuenta'),
]
