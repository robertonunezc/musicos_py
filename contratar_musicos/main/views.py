from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from contratar_musicos.main.models import *



@login_required
def index(request):
    return render(request, 'musicos/index.html')

# This view renders a page with success message.
def success(request):
    return render(request, "registration/success.html")


def success_reset(request):
    return render(request, "registration/password_reset_complete.html")


def contacto(request):
    return render(request, "contacto.html")

def confirmar_registro(request, token):
    mensaje = None
    try:
        token = Token.objects.get(key=token)

        if token.user:
            usuario = token.user
            usuario.is_active = True
            usuario.save()
            mensaje = "Se ha confirmado su correo. Ya pude utilizar todas las funciones de nuestro sitio."
            # token.delete()
    except Token.DoesNotExist:
        mensaje = "Código activación no encontrado. Contacte con el administrador"

    context = {'mensaje': mensaje}

    return render(request, "registration/success_confirmation.html", context)
