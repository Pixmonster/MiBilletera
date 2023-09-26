from django.contrib.auth.forms import UserCreationForm
from .models import *
from django import forms
from django.forms import ModelForm
from django.forms import DateInput

#region Usuario
class UsuarioForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password','imagen']
        
class ImageForm(ModelForm):
    class Meta:
        model = Usuario
        fields = ['imagen']

#endregion

#region Ingresos/Gastos       
class IngresosForm(ModelForm):
    class Meta:
        model = Transacciones
        fields = ['fecha', 'monto', 'fk_fuente']
    #   extra_fields = ['']
    #   exclude = ('')
        widgets = {
            'fecha': DateInput(attrs={'type': 'date'}),
            'fk_fuente': forms.Select(attrs={'class': 'form-control w-75 mr-2'}),
            'monto': forms.TextInput(attrs={'class': 'form-control autonumeric'}),
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
            'monto': forms.TextInput(attrs={'class': 'form-control autonumeric'}),
        }

    def clean_fk_categoria(self):
        categoria = self.cleaned_data.get('fk_categoria')
        if not categoria:
            raise forms.ValidationError("Debes seleccionar una categoría.")
        return categoria

#endregion

#region Categoria/Fuente Personalizada
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

#endregion

#region Deudas
class CustomDecimalInput(forms.widgets.TextInput):
    def __init__(self, attrs=None):
        attrs = {'class': 'form-control', 'type': 'number'} if attrs is None else attrs
        super().__init__(attrs=attrs)

class DeudasForm(forms.ModelForm):
    valor_de_interes_mensual = forms.DecimalField(widget=CustomDecimalInput)
    valor_de_interes_fijo = forms.DecimalField(widget=CustomDecimalInput)

    class Meta:
        model = Deudas
        fields = ['descripcion_deuda', 'valor_total_deuda', 'tipo_de_interes', 'valor_de_interes_mensual', 'valor_de_interes_fijo', 'plazo_del_prestamo', 'frecuencia_de_pago']
        widgets = {
            'descripcion_deuda': forms.TextInput(attrs={'class': 'form-control w-100'}),
            'valor_total_deuda': forms.TextInput(attrs={'class': 'form-control autonumeric'}),
            'tipo_de_interes': forms.TextInput(attrs={'class': 'form-control w-100'}),
            'plazo_del_prestamo': forms.TextInput(attrs={'class': 'form-control w-100'}),
            'frecuencia_de_pago': forms.TextInput(attrs={'class': 'form-control w-100'})
        }

    def clean_valor_de_interes_mensual(self):
        valor_de_interes_mensual = self.cleaned_data['valor_de_interes_mensual']
        if valor_de_interes_mensual is not None:
            return valor_de_interes_mensual / 100
        else:
            return None
        
    def clean_valor_de_interes_fijo(self):
        valor_de_interes_fijo = self.cleaned_data['valor_de_interes_fijo']
        if valor_de_interes_fijo is not None:
            return valor_de_interes_fijo / 100
        else:
            return None

#endregion
