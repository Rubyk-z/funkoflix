"""
Vistas de la app Funkos.

Importante: todas las vistas del catálogo, categorías, exclusivos, detalle y
búsqueda están protegidas con @login_required. Si un usuario no autenticado
intenta acceder, Django lo redirige automáticamente al login.

La home (vista 'home') es pública: muestra contenido distinto si el usuario
está logueado (productos destacados) o si no lo está (pantalla de bienvenida).
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count

from .forms import RegistroForm
from .models import Categoria, Franquicia, Funko


# =============================================================
#  HOME (pública: muestra bienvenida o catálogo según sesión)
# =============================================================

def home(request):
    """
    - Si el usuario NO está logueado → pantalla de bienvenida.
    - Si SÍ está logueado → home con destacados.
    """
    if not request.user.is_authenticated:
        # Renderiza la pantalla de bienvenida (welcome.html)
        return render(request, 'Funkos/welcome.html')

    # Usuario logueado: mostrar destacados
    # Solo Funkos activos (los dados de baja no se muestran)
    funkos_destacados = Funko.objects.filter(
        activo=True,
        es_exclusivo=True,
        stock__gt=0,
    )[:4]
    return render(request, 'Funkos/home.html', {
        'funkos_destacados': funkos_destacados,
    })


# =============================================================
#  CATÁLOGO Y NAVEGACIÓN (todo protegido con login)
# =============================================================

@login_required
def catalogo(request):
    """
    Catálogo: muestra TODOS los Funkos activos en un grid.
    Requiere sesión iniciada.
    """
    # Solo Funkos activos (filtramos los dados de baja)
    funkos = Funko.objects.filter(activo=True).order_by('-creado_en')
    return render(request, 'Funkos/catalogo.html', {
        'funkos': funkos,
    })


@login_required
def categorias(request):
    """Lista de categorías con cantidad de productos activos."""
    # Count con filtro: solo cuenta los Funkos activos de cada categoría
    cats = Categoria.objects.annotate(
        total_funkos=Count('funkos', filter=Q(funkos__activo=True))
    )
    return render(request, 'Funkos/categorias.html', {
        'categorias': cats,
    })


@login_required
def categoria_detail(request, slug):
    """Productos activos de una categoría específica."""
    categoria = get_object_or_404(Categoria, slug=slug)
    funkos = categoria.funkos.filter(activo=True)
    return render(request, 'Funkos/categoria_detail.html', {
        'categoria': categoria,
        'funkos': funkos,
    })


@login_required
def exclusivos(request):
    """Solo Funkos exclusivos y activos."""
    funkos = Funko.objects.filter(activo=True, es_exclusivo=True)
    return render(request, 'Funkos/exclusivos.html', {
        'funkos': funkos,
    })


@login_required
def product_detail(request, slug):
    """Ficha del producto. Si está dado de baja, devuelve 404."""
    funko = get_object_or_404(Funko, slug=slug, activo=True)
    relacionados = Funko.objects.filter(
        activo=True,
        franquicia=funko.franquicia,
    ).exclude(id=funko.id)[:4]
    return render(request, 'Funkos/product_detail.html', {
        'funko': funko,
        'relacionados': relacionados,
    })


@login_required
def search(request):
    """Búsqueda en nombre, descripción y franquicia (solo activos)."""
    query = request.GET.get('q', '').strip()
    funkos = Funko.objects.none()

    if query:
        funkos = Funko.objects.filter(
            Q(activo=True) & (
                Q(nombre__icontains=query) |
                Q(descripcion__icontains=query) |
                Q(franquicia__nombre__icontains=query)
            )
        ).distinct()

    return render(request, 'Funkos/search.html', {
        'query': query,
        'funkos': funkos,
        'total': funkos.count(),
    })


@login_required
def mi_cuenta(request):
    """Vista privada del usuario."""
    return render(request, 'Funkos/mi_cuenta.html')


# =============================================================
#  AUTENTICACIÓN (público)
# =============================================================

def register(request):
    """
    Registro de nuevos usuarios.
    Después de registrarse, el usuario queda automáticamente logueado.
    """
    if request.user.is_authenticated:
        return redirect('Funkos:home')

    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # (Sin mensaje flash: el usuario va directo a la home ya logueado)
            return redirect('Funkos:home')
    else:
        form = RegistroForm()

    return render(request, 'registration/register.html', {'form': form})
