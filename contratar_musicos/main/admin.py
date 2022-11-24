from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .admin_forms import *
from django.utils.translation import ugettext, ugettext_lazy as _


class UsuarioAdmin(UserAdmin):
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'apem', 'email')}),
        # (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        # (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        # ("Info", {'fields': ('image', 'tipo_usuario', 'clave', 'clave_nivel_superior')}),
    )
    # filter_horizontal = ('ciudades', 'sucursales',)

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Token)
admin.site.register(Municipio)
admin.site.register(Estado)
admin.site.register(Pais)
