from django.contrib.auth.forms import UserCreationForm
from .models import *
from django import forms
from django.forms import ModelForm
from django.forms import DateInput

class UsuarioForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password']

class TransaccionesForm(ModelForm):
    class Meta:
        model = Transacciones
        fields = ['fecha','monto']
    #   extra_fields = ['']
    #   exclude = ('')
        widgets = {
            'fecha': DateInput(attrs={'type': 'date'}),
            }
