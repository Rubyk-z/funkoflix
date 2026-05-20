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
    funkos_destacados = Funko.objects.filter(
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
    Catálogo: muestra TODOS los Funkos en un grid.
    Requiere sesión iniciada.
    """
    funkos = Funko.objects.all().order_by('-creado_en')
    return render(request, 'Funkos/catalogo.html', {
        'funkos': funkos,
    })


@login_required
def categorias(request):
    """Lista de categorías con cantidad de productos."""
    cats = Categoria.objects.annotate(total_funkos=Count('funkos'))
    return render(request, 'Funkos/categorias.html', {
        'categorias': cats,
    })


@login_required
def categoria_detail(request, slug):
    """Productos de una categoría específica."""
    categoria = get_object_or_404(Categoria, slug=slug)
    funkos = categoria.funkos.all()
    return render(request, 'Funkos/categoria_detail.html', {
        'categoria': categoria,
        'funkos': funkos,
    })


@login_required
def exclusivos(request):
    """Solo Funkos marcados como exclusivos."""
    funkos = Funko.objects.filter(es_exclusivo=True)
    return render(request, 'Funkos/exclusivos.html', {
        'funkos': funkos,
    })


@login_required
def product_detail(request, slug):
    """Ficha del producto."""
    funko = get_object_or_404(Funko, slug=slug)
    relacionados = Funko.objects.filter(
        franquicia=funko.franquicia,
    ).exclude(id=funko.id)[:4]
    return render(request, 'Funkos/product_detail.html', {
        'funko': funko,
        'relacionados': relacionados,
    })


@login_required
def search(request):
    """Búsqueda en nombre, descripción y franquicia."""
    query = request.GET.get('q', '').strip()
    funkos = Funko.objects.none()

    if query:
        funkos = Funko.objects.filter(
            Q(nombre__icontains=query) |
            Q(descripcion__icontains=query) |
            Q(franquicia__nombre__icontains=query)
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
            messages.success(request, f'¡Bienvenido a Funko Store, {user.username}! 🎉')
            return redirect('Funkos:home')
    else:
        form = RegistroForm()

    return render(request, 'registration/register.html', {'form': form})
