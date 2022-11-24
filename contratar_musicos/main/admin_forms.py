# -*- coding: utf-8 -*-
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django import forms
from .models import *


class MyUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        model = Usuario
        fields = '__all__'

    class Media:
        js = ('http://ajax.googleapis.com/ajax/libs/jquery/1.4.0/jquery.min.js',)


class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ("username",)
