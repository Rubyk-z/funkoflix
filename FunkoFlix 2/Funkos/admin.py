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
    Acá vas a cargar y gestionar tus productos.

    Implementa BAJA LÓGICA (soft delete): en lugar de eliminar un Funko,
    se lo marca como inactivo (activo=False). Así deja de mostrarse en la
    tienda pero permanece en la base de datos para conservar el histórico.
    """

    # Columnas en la lista de productos (incluye 'activo' para ver el estado)
    list_display = (
        'nombre',
        'franquicia',
        'categoria',
        'precio',
        'stock',
        'rareza',
        'es_exclusivo',
        'activo',
    )

    # Filtros laterales (incluye 'activo' para filtrar dados de baja)
    list_filter = ('activo', 'categoria', 'franquicia', 'rareza', 'es_exclusivo')

    # Buscador
    search_fields = ('nombre', 'descripcion', 'franquicia__nombre')

    # Slug autocompletado a partir del nombre
    prepopulated_fields = {'slug': ('nombre',)}

    # Permite editar estos campos directamente desde la lista
    list_editable = ('precio', 'stock', 'es_exclusivo', 'activo')

    # Acciones personalizadas que aparecen en el desplegable de la lista
    actions = ['dar_de_baja', 'dar_de_alta']

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
        ('Estado', {
            'fields': ('activo',),
            'description': 'Desmarcá "activo" para dar de baja el Funko sin eliminarlo de la base de datos.',
        }),
    )

    @admin.action(description='Dar de baja los Funkos seleccionados (sin eliminar)')
    def dar_de_baja(self, request, queryset):
        """
        Acción de baja lógica: marca los Funkos seleccionados como inactivos.
        No los elimina de la base de datos.
        """
        actualizados = queryset.update(activo=False)
        self.message_user(
            request,
            f'{actualizados} Funko(s) dado(s) de baja. Siguen en la base de datos pero ya no se muestran en la tienda.'
        )

    @admin.action(description='Dar de alta los Funkos seleccionados (reactivar)')
    def dar_de_alta(self, request, queryset):
        """
        Acción inversa: reactiva los Funkos seleccionados.
        """
        actualizados = queryset.update(activo=True)
        self.message_user(
            request,
            f'{actualizados} Funko(s) reactivado(s). Vuelven a mostrarse en la tienda.'
        )
