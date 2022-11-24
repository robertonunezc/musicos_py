from rest_framework import serializers
from contratar_musicos.musicos.models import *


class MusicoSerializer(serializers.ModelSerializer):
    class Meta:
        model= Musico
        fields = '__all__'