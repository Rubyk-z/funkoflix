# Funko Store

Tienda virtual de Funko Pops desarrollada como proyecto académico para la materia Evaluación de Proyecto.

## Stack tecnológico

- Python 3.x
- Django 5.x
- SQLite
- HTML5 + CSS3
- Django Templates
- Django Authentication System

## Cómo levantar el proyecto

### 1. Entrar a la carpeta del proyecto

```bash
cd FunkoStore
```

### 2. Crear y activar entorno virtual

```bash
# Crear
python3 -m venv venv

# Activar (Mac/Linux)
source venv/bin/activate

# Activar (Windows)
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Aplicar migraciones (crea db.sqlite3 con las tablas iniciales)

```bash
python manage.py migrate
```

### 5. Crear superusuario (para acceder al admin)

```bash
python manage.py createsuperuser
```

### 6. Ejecutar el servidor de desarrollo

```bash
python manage.py runserver
```

Abrir en el navegador:
- Sitio: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## Estructura del proyecto

```
FunkoStore/
├── manage.py            # Script de gestión de Django
├── db.sqlite3           # Base de datos (se genera al hacer migrate)
├── requirements.txt
│
├── Project/             # Configuración del proyecto
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── Funkos/              # App principal
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── views.py
│   ├── urls.py
│   └── migrations/
│
├── Templates/
│   ├── base.html
│   ├── Funkos/
│   │   └── home.html
│   └── registration/    # (login.html, register.html, etc.)
│
└── static/
    ├── css/
    │   └── styles.css
    └── src/             # imágenes del sitio (logo, hero, etc.)
```
