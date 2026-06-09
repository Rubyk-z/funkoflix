"""
Configuración principal del proyecto FunkoFlix.
Acá se define cómo se comporta toda la aplicación: base de datos,
apps activas, templates, archivos estáticos, autenticación, etc.
"""

from pathlib import Path

# BASE_DIR apunta a la carpeta raíz del proyecto (donde está manage.py).
BASE_DIR = Path(__file__).resolve().parent.parent


# =============================================================
#  CONFIGURACIÓN DE SEGURIDAD
# =============================================================

# Clave secreta usada por Django para firmar sesiones, cookies, etc.
# IMPORTANTE: en producción esto se carga desde una variable de entorno.
SECRET_KEY = 'django-insecure-cambiar-esta-clave-en-produccion'

# DEBUG=True muestra errores detallados en el navegador. Solo para desarrollo.
DEBUG = True

ALLOWED_HOSTS = []


# =============================================================
#  APLICACIONES INSTALADAS
# =============================================================

INSTALLED_APPS = [
    # Apps por defecto de Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Nuestras apps
    'Funkos',
]


# =============================================================
#  MIDDLEWARE
# =============================================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'Project.urls'


# =============================================================
#  TEMPLATES
# =============================================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'Templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Project.wsgi.application'


# =============================================================
#  BASE DE DATOS
# =============================================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# =============================================================
#  VALIDACIÓN DE CONTRASEÑAS
# =============================================================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# =============================================================
#  INTERNACIONALIZACIÓN
# =============================================================

LANGUAGE_CODE = 'es-ar'
TIME_ZONE = 'America/Argentina/Buenos_Aires'
USE_I18N = True
USE_TZ = True


# =============================================================
#  ARCHIVOS ESTÁTICOS (CSS, JS, imágenes del sitio)
# =============================================================

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']


# =============================================================
#  ARCHIVOS SUBIDOS POR EL USUARIO (imágenes de Funkos)
# =============================================================

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# =============================================================
#  AUTENTICACIÓN
# =============================================================

LOGIN_REDIRECT_URL = 'Funkos:home'
LOGOUT_REDIRECT_URL = 'Funkos:home'
LOGIN_URL = 'login'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
