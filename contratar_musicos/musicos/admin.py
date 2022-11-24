from django.contrib import admin
from contratar_musicos.musicos.models import *
# Register your models here.


class ImagenMusicoAdmin(admin.TabularInline):
    model = ImagenMusico


class DemoAdmin(admin.TabularInline):
    model = Demo


class GeoLocalizacionAdmin(admin.TabularInline):
    model = GeoLocalizacion

#
# class ContactoAdmin(admin.TabularInline):
#     model = Contacto

#
# class PrecioAdmin(admin.TabularInline):
#     model = Precio


class MusicoAdmin(admin.ModelAdmin):
    inlines = [ImagenMusicoAdmin, GeoLocalizacionAdmin]


admin.site.register(EstiloMusica)
admin.site.register(InfoAdicional)
admin.site.register(TipoCobro)
admin.site.register(Precio)
admin.site.register(Servicios)
admin.site.register(TipoDemo)
admin.site.register(TipoMusico)
admin.site.register(GeoLocalizacion)
admin.site.register(Contacto)
admin.site.register(ImagenMusico)
admin.site.register(Musico, MusicoAdmin)
admin.site.register(Demo)
