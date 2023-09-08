from django.contrib.auth.forms import UserCreationForm
from .models import *
from django import forms
from django.forms import ModelForm
from django.forms import DateInput

class UsuarioForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password','imagen']
        
        
class ImageForm(ModelForm):
    class Meta:
        model = Usuario
        fields = ['imagen']
        

class IngresosForm(ModelForm):
    class Meta:
        model = Transacciones
        fields = ['fecha', 'monto', 'fk_fuente']
    #   extra_fields = ['']
    #   exclude = ('')
        widgets = {
            'fecha': DateInput(attrs={'type': 'date'}),
            'fk_fuente': forms.Select(attrs={'class': 'form-control w-75 mr-2'}),
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
            'fk_categoria': forms.Select(attrs={'class': 'form-control w-75 mr-2'}),
            'monto': forms.TextInput(attrs={'class': 'form-control autonumeric', 'data-a-sign': '', 'data-a-dec': ',', 'data-a-sep': '.'}),
        }

    def clean_fk_categoria(self):
        categoria = self.cleaned_data.get('fk_categoria')
        if not categoria:
            raise forms.ValidationError("Debes seleccionar una categoría.")
        return categoria

class CategoriaPersonalizadaForm(forms.ModelForm):
    class Meta:
        model = CategoriaGasto
        fields = ['nombre_categoria']
        widgets = {
            'nombre_categoria': forms.TextInput(attrs={'class': 'form-control '}),
        }

class FuentePersonalizadaForm(forms.ModelForm):
    class Meta:
        model = FuenteIngreso
        fields = ['nombre_fuente']
        widgets = {
            'nombre_fuente': forms.TextInput(attrs={'class': 'form-control '}),
        }