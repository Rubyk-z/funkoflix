"""
URLs raíz del proyecto.
Acá se decide a qué app va cada URL que recibe el servidor.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Panel de administración de Django
    # http://127.0.0.1:8000/admin/
    path('admin/', admin.site.urls),

    # URLs de autenticación nativas de Django:
    # /accounts/login/, /accounts/logout/, etc.
    path('accounts/', include('django.contrib.auth.urls')),

    # URLs raíz del sitio: las maneja la app Funkos
    path('', include('Funkos.urls')),
]


# Solo en desarrollo: servir las imágenes subidas (carpeta media/).
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
