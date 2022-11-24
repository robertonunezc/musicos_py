from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
import binascii
import os


class Usuario(AbstractUser):
    objects = UserManager()
    apem = models.CharField('Apellido Materno', max_length=30, null=True, blank=True)
    nombre_completo = models.CharField(max_length=100, null=True, blank=True, editable=False)
    verificado = models.BooleanField(default=False)

    def get_full_name(self):
        full_name = '%s %s %s' % (self.first_name, self.apem, self.last_name)
        return full_name.strip()


# todo modificar token para que sean sesiones
class Token(models.Model):
    key = models.CharField(max_length=40, primary_key=True)
    user = models.OneToOneField('Usuario', related_name='auth_token',on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(Token, self).save(*args, **kwargs)

    @staticmethod
    def generate_key():
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key


class Municipio(models.Model):
    nombre = models.CharField(max_length=100, blank=True, null=True)
    estado = models.ForeignKey('Estado', related_name='municipios', on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class Estado(models.Model):
    nombre = models.CharField(max_length=100, blank=True, null=True)
    pais = models.ForeignKey('Pais', related_name='estados',on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class Pais(models.Model):
    nombre = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nombre