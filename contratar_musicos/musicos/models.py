from django.db import models
from contratar_musicos.main.models import *
from contratar_musicos.main.utils import PathAndRename

from django.template.defaultfilters import slugify

# Create your models here.
path_and_rename_musicos = PathAndRename("musicos")
TIPOS_PRECIOS = (
    (0, 'POR HORA'),
    (1, 'POR CANCION'),
    (2, 'POR EVENTO'),
    (3, 'GENERAL'),
)


class Musico(models.Model):
    usuario = models.ForeignKey('main.Usuario', related_name='musicos', on_delete=models.SET_DEFAULT, default=None)
    nombre = models.CharField(max_length=30)
    imagen_principal = models.FileField(null=True, upload_to=path_and_rename_musicos)
    descripcion = models.TextField()
    valoracion = models.FloatField(null=True, blank=True, default=0)
    tipo_musico = models.ForeignKey('TipoMusico', related_name='musicos', on_delete=models.SET_DEFAULT, default=None)
    precio = models.ForeignKey('Precio', related_name='musicos', null=True, blank=True, on_delete=models.SET_DEFAULT,
                               default=None)
    estilo_musica = models.ManyToManyField('EstiloMusica', related_name='musico')
    servicio_musica = models.ManyToManyField('Servicios', related_name='musico')
    slug = models.SlugField(max_length=60, editable=False, unique=True, null=True, blank=True)
    demo = models.ForeignKey('Demo', blank=True, null=True, on_delete=models.SET_NULL)
    info_adicional = models.ManyToManyField('InfoAdicional')
    cantidad_visitas = models.IntegerField(default=0, blank=True, null=True)
    contacto = models.OneToOneField('Contacto', null=True, blank=True, related_name='musico',
                                    on_delete=models.SET_DEFAULT, default=None)

    # TODO revisar los precios para agregar

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nombre)
        return super(Musico, self).save(*args, **kwargs)


class InfoAdicional(models.Model):
    pregunta = models.TextField(max_length=250)
    respuesta = models.TextField(max_length=250)

    def __str__(self):
        return self.pregunta


class EstiloMusica(models.Model):
    nombre = models.CharField(max_length=30)

    def __str__(self):
        return self.nombre


class TipoCobro(models.Model):
    nombre = models.CharField(max_length=30)

    def __str__(self):
        return self.nombre


class Precio(models.Model):
    valor_minimo = models.IntegerField()
    valor_maximo = models.IntegerField()
    tipo_cobro = models.ForeignKey('TipoCobro', on_delete=models.SET_DEFAULT, default=None)

    def __str__(self):
        return '${}'.format(self.valor_maximo)


class Servicios(models.Model):
    nombre = models.CharField(max_length=30)

    def __str__(self):
        return self.nombre


class TipoMusico(models.Model):
    nombre = models.CharField(max_length=30)
    slug = models.SlugField(max_length=60, editable=False, unique=True, null=True, blank=True)

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nombre)
        return super(TipoMusico, self).save(*args, **kwargs)


class GeoLocalizacion(models.Model):
    municipio = models.ForeignKey('main.Municipio', on_delete=models.CASCADE)
    estado = models.ForeignKey('main.Estado', on_delete=models.CASCADE)
    pais = models.ForeignKey('main.Pais', on_delete=models.CASCADE)
    musico = models.ForeignKey('Musico', related_name='localizacion', blank=True, null=True
                               , on_delete=models.CASCADE)

    def __str__(self):
        return "{}-{}-{}".format(self.municipio, self.estado, self.pais)


class Contacto(models.Model):
    telefono = models.CharField(max_length=12)
    email = models.CharField(max_length=30, null=True, blank=True)
    web = models.CharField(max_length=30, null=True, blank=True)
    facebook = models.CharField(max_length=30, null=True, blank=True)
    twitter = models.CharField(max_length=30, null=True, blank=True)
    instagram = models.CharField(max_length=30, null=True, blank=True)
    youtube = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.telefono


class ImagenMusico(models.Model):
    image = models.FileField(null=True, blank=True)
    texto = models.CharField(max_length=100, blank=True, null=True)
    musico = models.ForeignKey('Musico', related_name='imagenes_galeria', blank=True, null=True,
                               on_delete=models.CASCADE)

    def __str__(self):
        return self.musico.slug


class TipoDemo(models.Model):
    nombre = models.CharField(max_length=30)

    def __str__(self):
        return self.nombre


class Demo(models.Model):
    nombre = models.CharField(max_length=150, default="Demo")
    video = models.CharField(max_length=150)
    audio = models.FileField(null=True, blank=True)

    def __str__(self):
        return self.nombre
