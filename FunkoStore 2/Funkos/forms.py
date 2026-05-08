"""
Formularios de la app Funkos.
Acá definimos los formularios personalizados que extienden los de Django.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistroForm(UserCreationForm):
    """
    Formulario de registro de usuarios.
    Hereda de UserCreationForm (que ya maneja username, password1 y password2)
    y le agregamos el email como campo obligatorio.
    """

    # Campo email adicional con validación de formato
    email = forms.EmailField(
        required=True,
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'tu@email.com',
        })
    )

    class Meta:
        model = User
        # Orden en que aparecerán los campos en el formulario
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        """
        Sobrescribimos __init__ para agregarle clases CSS y placeholders
        a los campos heredados (username, password1, password2).
        """
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Tu nombre de usuario',
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Contraseña',
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Repetí la contraseña',
        })

        # Etiquetas en español
        self.fields['username'].label = 'Usuario'
        self.fields['password1'].label = 'Contraseña'
        self.fields['password2'].label = 'Confirmar contraseña'

    def save(self, commit=True):
        """
        Sobrescribimos save() para guardar también el email.
        UserCreationForm por defecto solo guarda username y password.
        """
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
