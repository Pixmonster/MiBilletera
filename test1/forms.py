from django.contrib.auth.forms import UserCreationForm
from .models import *
from django import forms
from django.forms import ModelForm
from django.forms import DateInput

class UsuarioForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password']

class IngresosForm(ModelForm):
    class Meta:
        model = Transacciones
        fields = ['fecha', 'monto', 'fk_fuente']
    #   extra_fields = ['']
    #   exclude = ('')
        widgets = {
            'fecha': DateInput(attrs={'type': 'date'}),
            'fk_fuente': forms.Select(attrs={'class': 'form-control'}),
            'monto': forms.TextInput(attrs={'class': 'form-control autonumeric', 'data-a-sign': '', 'data-a-dec': ',', 'data-a-sep': '.'}),
            }

    def clean_fk_fuente(self):
        fuente = self.cleaned_data.get('fk_fuente')
        if not fuente:
            raise forms.ValidationError("Debes seleccionar una fuente.")
        return fuente
    


class GastosForm(ModelForm):
    class Meta:
        model = Transacciones
        fields = ['fecha', 'monto', 'fk_categoria']
        widgets = {
            'fecha': DateInput(attrs={'type': 'date'}),
            'fk_categoria': forms.Select(attrs={'class': 'form-control'}),
            'monto': forms.TextInput(attrs={'class': 'form-control autonumeric', 'data-a-sign': '', 'data-a-dec': ',', 'data-a-sep': '.'}),
        }

    def clean_fk_categoria(self):
        categoria = self.cleaned_data.get('fk_categoria')
        if not categoria:
            raise forms.ValidationError("Debes seleccionar una categoría.")
        return categoria

