"""
URLs de la app Funkos.
Acá registramos las rutas relacionadas con el catálogo, carrito, órdenes, etc.
"""

from django.urls import path
from . import views

app_name = 'Funkos'

urlpatterns = [
    # Home
    path('', views.home, name='home'),

    # Catálogo
    path('catalogo/', views.catalogo, name='catalogo'),

    # Categorías
    path('categorias/', views.categorias, name='categorias'),
    path('categoria/<slug:slug>/', views.categoria_detail, name='categoria_detail'),

    # Exclusivos
    path('exclusivos/', views.exclusivos, name='exclusivos'),

    # Detalle de producto
    # <slug:slug> captura la parte de la URL como un string limpio (a-z, 0-9, guiones)
    path('producto/<slug:slug>/', views.product_detail, name='product_detail'),

    # Búsqueda
    path('buscar/', views.search, name='search'),

    # Auth
    path('register/', views.register, name='register'),
    path('mi-cuenta/', views.mi_cuenta, name='mi_cuenta'),
]
