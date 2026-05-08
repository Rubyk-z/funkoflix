"""
Vistas de la app Funkos.
Cada función recibe un 'request' (la solicitud HTTP) y devuelve una 'response'
(la respuesta HTTP), generalmente renderizando un template.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import RegistroForm


def home(request):
    """
    Vista principal del sitio.
    Por ahora solo muestra la home estática para verificar que el setup funciona.
    Más adelante traerá los Funkos desde la base de datos.
    """
    return render(request, 'Funkos/home.html')


def register(request):
    """
    Vista de registro de nuevos usuarios.
    - GET  → muestra el formulario vacío
    - POST → valida y crea el usuario; si todo está OK, lo loguea automáticamente
    """
    # Si el usuario ya está logueado, no tiene sentido que vea el registro
    if request.user.is_authenticated:
        return redirect('Funkos:home')

    if request.method == 'POST':
        # request.POST contiene los datos enviados por el formulario
        form = RegistroForm(request.POST)

        if form.is_valid():
            # form.save() crea el usuario en la BD
            user = form.save()

            # login() arma la sesión: el usuario queda logueado automáticamente
            login(request, user)

            # Mensaje flash que se mostrará en la siguiente página
            messages.success(request, f'¡Bienvenido a Funko Store, {user.username}! 🎉')

            return redirect('Funkos:home')
    else:
        # GET: mostramos un formulario vacío
        form = RegistroForm()

    return render(request, 'registration/register.html', {'form': form})


@login_required
def mi_cuenta(request):
    """
    Vista privada de prueba: solo accesible si el usuario está logueado.
    El decorador @login_required redirige automáticamente al login si no lo está.
    Más adelante esta página mostrará el historial de compras del usuario.
    """
    return render(request, 'Funkos/mi_cuenta.html')
