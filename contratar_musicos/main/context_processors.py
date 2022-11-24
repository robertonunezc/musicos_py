from contratar_musicos.main.models import *
from contratar_musicos.musicos.models import *


def menu_superior(request):
    tipos_musico = TipoMusico.objects.all()
    return {'tipos_musico': tipos_musico}


# def enviar_boletin(request):
#     form_boletin = BoletinForm()
#     mensaje = None
#     if request.method == 'POST':
#         form = BoletinForm(request.POST)
#         if form.is_valid():
#             nombre = form.cleaned_data['nombre']
#             email = form.cleaned_data['email']
#             zona = form.cleaned_data['zona']
#             texto = 'De {} email: {} \n Zona: {} \n Deseo unirme al boletín'.format(nombre,
#                                                             email,
#                                                             zona)
#             send_mail('Correo desde la web para boletín', texto, settings.DEFAULT_FROM_EMAIL,
#                       ['hola@zonareal.mx'], fail_silently=True)
#             mensaje = "Se ha enviado su suscripción"
#
#     return {'formulario': form_boletin, 'mensaje': mensaje }