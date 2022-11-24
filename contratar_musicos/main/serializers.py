# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import *


class UsuarioSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(source='first_name')
    apellido = serializers.CharField(source='last_name')
    imagen = serializers.ImageField(source='image', allow_empty_file=True)
    token = serializers.SerializerMethodField()

    def get_token(self, obj):
        try:
            token = obj.auth_token
        except Token.DoesNotExist:
            token = Token.objects.create(user=obj)
        return token.key

    class Meta:
        model = Usuario
        fields = ('token', 'nombre', 'email', 'apellido', 'imagen', )


class UsuarioPublicoSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(source='first_name')
    apellido = serializers.CharField(source='last_name')
    imagen = serializers.ImageField(source='image', allow_empty_file=True)

    class Meta:
        model = Usuario
        fields = ('id', 'nombre', 'apellido', 'imagen', )
