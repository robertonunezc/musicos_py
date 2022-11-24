from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from .models import *
from django.conf import settings
from django.core.mail import send_mail

__author__ = 'jorge'


@receiver(post_save, sender=Usuario)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=Usuario)
def set_nombre_completo(sender, instance=None, **kwargs):
    usuario = instance
    if usuario.nombre_completo != usuario.get_full_name():
        usuario.nombre_completo = usuario.get_full_name()
        usuario.save()


@receiver(post_save, sender=Usuario)
def send_email_confirmation(sender, instance=None, created=False, **kwargs):
    if created:
        token = instance.auth_token
        mensaje = u"Bienvenido a nuestro sitio, para activar su cuenta y poder utilizar todas las funciones del sitio "\
                  u"de click en el enlace a continuación {}/confirmacion/email/{}/. "\
                  u"Si te registraste con tu cuenta de Facebook haz caso omiso de este correo. Atte 123Dreamit"\
            .format(settings.CM_HOST, token.key)

        send_mail(u'Confirmación cuenta en ContratarMusicos', mensaje, settings.DEFAULT_FROM_EMAIL,
                  [instance.email], fail_silently=False)

