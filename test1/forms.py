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
        fields = ['fecha','monto', 'fk_categoria', 'fk_fuente']
    #   extra_fields = ['']
    #   exclude = ('')
        widgets = {
            'fecha': DateInput(attrs={'type': 'date'}),
            'fk_categoria': forms.Select(attrs={'class': 'form-control'}),
            'fk_fuente': forms.Select(attrs={'class': 'form-control'}),
            'monto': forms.TextInput(attrs={'class': 'form-control autonumeric', 'data-a-sign': '', 'data-a-dec': ',', 'data-a-sep': '.'}),
            }

