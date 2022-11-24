from contratar_musicos.musicos.models import *
from django.forms import ModelForm

class ContactoForm(ModelForm):
    class Meta:
        model = Contacto
        fields = '__all__'


class LocalizacionForm(ModelForm):
    class Meta:
        model = GeoLocalizacion
        fields = '__all__'


class RegistroMusicoForm(ModelForm):
    # Embed form
    contacto = ContactoForm()
    localizacion = LocalizacionForm()

    class Meta:
        model = Musico
        fields = ('nombre', 'descripcion', 'tipo_musico', 'estilo_musica','servicio_musica', 'contacto')
        # exclude = ['usuario']


class UsuarioForm(ModelForm):
    class Meta:
        model = Usuario
        fields = ['email', 'username', 'password']
