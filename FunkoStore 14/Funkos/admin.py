"""
Configuración del panel administrativo de Django.
Acá registramos los modelos para que aparezcan en /admin/ y los podamos
crear, editar y eliminar visualmente.
"""

from django.contrib import admin
from .models import Categoria, Franquicia, Funko


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    """Admin de Categoría."""

    # Columnas a mostrar en la lista
    list_display = ('nombre', 'slug')

    # Genera el slug automáticamente a partir del nombre
    prepopulated_fields = {'slug': ('nombre',)}

    # Caja de búsqueda en la parte superior
    search_fields = ('nombre',)


@admin.register(Franquicia)
class FranquiciaAdmin(admin.ModelAdmin):
    """Admin de Franquicia."""

    list_display = ('nombre', 'categoria')
    list_filter = ('categoria',)              # Filtro lateral por categoría
    prepopulated_fields = {'slug': ('nombre',)}
    search_fields = ('nombre',)


@admin.register(Funko)
class FunkoAdmin(admin.ModelAdmin):
    """
    Admin de Funko (el más completo porque es el modelo principal).
    Acá vas a cargar tus productos.
    """

    # Columnas en la lista de productos
    list_display = (
        'nombre',
        'franquicia',
        'categoria',
        'precio',
        'stock',
        'rareza',
        'es_exclusivo',
    )

    # Filtros laterales para encontrar productos rápido
    list_filter = ('categoria', 'franquicia', 'rareza', 'es_exclusivo')

    # Buscador
    search_fields = ('nombre', 'descripcion', 'franquicia__nombre')

    # Slug autocompletado a partir del nombre
    prepopulated_fields = {'slug': ('nombre',)}

    # Permite editar estos campos directamente desde la lista (sin abrir el detalle)
    list_editable = ('precio', 'stock', 'es_exclusivo')

    # Organización del formulario de edición en secciones
    fieldsets = (
        ('Información básica', {
            'fields': ('nombre', 'slug', 'descripcion', 'imagen'),
        }),
        ('Clasificación', {
            'fields': ('categoria', 'franquicia', 'rareza', 'es_exclusivo'),
        }),
        ('Precio y stock', {
            'fields': ('precio', 'stock'),
        }),
    )
