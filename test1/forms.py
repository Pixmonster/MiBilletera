from django.contrib.auth.forms import UserCreationForm
from .models import *
from django import forms
from django.forms import ModelForm

class UsuarioForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password']

class TransaccionesForm(ModelForm):
    class Meta:
        model = Transacciones
        fields = '__all__'
    #   extra_fields = ['']