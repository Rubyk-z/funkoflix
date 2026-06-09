"""
Modelos de la app Funkos.
Cada clase representa una tabla en la base de datos.
Los atributos de la clase son las columnas de la tabla.
"""

from django.db import models
from django.urls import reverse


class Categoria(models.Model):
    """
    Categoría general de Funkos: Series, Películas, Videojuegos, Cultura Pop.
    Una categoría puede tener muchas franquicias y muchos funkos asociados.
    """

    nombre = models.CharField(
        max_length=50,
        unique=True,                   # No puede haber dos categorías con el mismo nombre
        verbose_name='Nombre',
    )
    slug = models.SlugField(
        max_length=60,
        unique=True,
        help_text='Versión URL-amigable del nombre (ej: "series-de-tv")',
    )
    descripcion = models.TextField(
        blank=True,                    # Campo opcional
        verbose_name='Descripción',
    )

    class Meta:
        # Configuración extra del modelo
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['nombre']          # Orden por defecto al hacer queries

    def __str__(self):
        # Se muestra cuando imprimimos el objeto (útil en el admin)
        return self.nombre


class Franquicia(models.Model):
    """
    Franquicia específica: Stranger Things, Marvel, Zelda, Star Wars, etc.
    Pertenece a una categoría (uno-a-muchos: una categoría tiene muchas franquicias).
    """

    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    slug = models.SlugField(max_length=120, unique=True)

    # ForeignKey: relación uno-a-muchos.
    # Una categoría tiene muchas franquicias. Una franquicia pertenece a UNA categoría.
    # related_name='franquicias' permite hacer: categoria.franquicias.all()
    # on_delete=PROTECT impide borrar una categoría si tiene franquicias asociadas.
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name='franquicias',
        verbose_name='Categoría',
    )

    class Meta:
        verbose_name = 'Franquicia'
        verbose_name_plural = 'Franquicias'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Funko(models.Model):
    """
    El producto: un Funko Pop coleccionable.
    Es el modelo central del catálogo.
    """

    # Choices: opciones predefinidas para el campo "rareza".
    # Se traducen como un dropdown en el admin y un campo con valores fijos en la BD.
    RAREZA_COMUN = 'comun'
    RAREZA_RARA = 'rara'
    RAREZA_EXCLUSIVA = 'exclusiva'
    RAREZA_LIMITADA = 'limitada'

    RAREZA_CHOICES = [
        (RAREZA_COMUN, 'Común'),
        (RAREZA_RARA, 'Rara'),
        (RAREZA_EXCLUSIVA, 'Exclusiva'),
        (RAREZA_LIMITADA, 'Edición limitada'),
    ]

    # ----- Datos básicos -----
    nombre = models.CharField(max_length=150, verbose_name='Nombre')
    slug = models.SlugField(
        max_length=180,
        unique=True,
        help_text='Versión URL del nombre (ej: "eleven-stranger-things")',
    )
    descripcion = models.TextField(verbose_name='Descripción')

    # ----- Precio y stock -----
    precio = models.DecimalField(
        max_digits=10,                 # Hasta 99,999,999.99
        decimal_places=2,              # 2 decimales (centavos)
        verbose_name='Precio',
    )
    stock = models.PositiveIntegerField(
        default=0,                     # Si no se especifica, arranca en 0
        verbose_name='Stock disponible',
    )

    # ----- Imagen -----
    # ImageField requiere Pillow (ya lo instalaste).
    # upload_to: subcarpeta dentro de MEDIA_ROOT donde se guardan los archivos.
    imagen = models.ImageField(
        upload_to='funkos/',
        blank=True,
        null=True,
        verbose_name='Imagen',
    )

    # ----- Clasificación -----
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name='funkos',
        verbose_name='Categoría',
    )
    franquicia = models.ForeignKey(
        Franquicia,
        on_delete=models.PROTECT,
        related_name='funkos',
        verbose_name='Franquicia',
    )
    rareza = models.CharField(
        max_length=20,
        choices=RAREZA_CHOICES,
        default=RAREZA_COMUN,
        verbose_name='Rareza',
    )
    es_exclusivo = models.BooleanField(
        default=False,
        verbose_name='¿Es exclusivo?',
        help_text='Marcalo si es un Funko exclusivo o de edición especial',
    )

    # ----- Baja lógica (soft delete) -----
    # En lugar de borrar un Funko de la base de datos, lo marcamos como inactivo.
    # Esto mantiene la integridad del histórico (órdenes pasadas que lo incluyen).
    # Un Funko con activo=False NO se muestra en la tienda, pero sigue en la BD.
    activo = models.BooleanField(
        default=True,
        verbose_name='¿Activo?',
        help_text='Si lo desmarcás, el Funko se da de baja: deja de mostrarse en la tienda '
                  'pero NO se elimina de la base de datos.',
    )

    # ----- Metadata automática -----
    creado_en = models.DateTimeField(auto_now_add=True)   # Se setea al crear
    actualizado_en = models.DateTimeField(auto_now=True)  # Se actualiza al modificar

    class Meta:
        verbose_name = 'Funko'
        verbose_name_plural = 'Funkos'
        ordering = ['-creado_en']      # Los más nuevos primero

    def __str__(self):
        return f'{self.nombre} ({self.franquicia.nombre})'

    def get_absolute_url(self):
        """
        URL canónica del producto. La usaremos en los templates con {{ funko.get_absolute_url }}
        para enlazar al detalle del Funko.
        """
        return reverse('Funkos:product_detail', kwargs={'slug': self.slug})

    @property
    def en_stock(self):
        """
        Propiedad calculada: True si hay stock disponible.
        Se usa como {{ funko.en_stock }} en los templates.
        """
        return self.stock > 0
