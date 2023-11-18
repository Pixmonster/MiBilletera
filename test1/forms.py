from django.contrib.auth.forms import UserCreationForm
from .models import *
from django import forms
from django.forms import ModelForm
from django.forms import DateInput
from decimal import InvalidOperation
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
TIPOS_DE_INTERES = (
    ('', 'Selecciona un tipo de interés'),
    ('Fijo', 'Interés Fijo'),
    ('Simple', 'Interés Simple'),
)

CAPITALIZACION = (
    ('', 'Selecciona la frecuencia de capitalización'),
    (1, 'Anual'),
    (2, 'Semestral'),
    (4, 'Trimestral'),
    (12, 'Mensual'),
    (365, 'Diaria'),
)

class CustomDecimalInput(forms.widgets.TextInput):
    def __init__(self, attrs=None):
        attrs = {'class': 'form-control', 'type': 'number'} if attrs is None else attrs
        super().__init__(attrs=attrs)

class DeudasForm(forms.ModelForm):
    tasa_de_interes_anual = forms.DecimalField(widget=CustomDecimalInput, required=False)
    tasa_de_interes_mensual = forms.DecimalField(widget=CustomDecimalInput, required=False)
    tipo_de_interes = forms.ChoiceField(choices=TIPOS_DE_INTERES, widget=forms.Select(attrs={'class': 'form-control w-100'}))
    capitalizacion = forms.ChoiceField(choices=CAPITALIZACION, widget=forms.Select(attrs={'class': 'form-control w-100'}), required=False)

    class Meta:
        model = Deudas
        fields = ['descripcion_deuda', 'valor_total_deuda', 'tipo_de_interes', 'tasa_de_interes_anual', 'tasa_de_interes_mensual', 'plazo_del_prestamo', 'capitalizacion', 'dia_pago']
        widgets = {
            'descripcion_deuda': forms.TextInput(attrs={'class': 'form-control w-100'}),
            'dia_pago': forms.TextInput(attrs={'class': 'form-control w-100'}),
            'valor_total_deuda': forms.TextInput(attrs={'class': 'form-control autonumeric'}),
            'tipo_de_interes': forms.TextInput(attrs={'class': 'form-control w-100'}),
            'plazo_del_prestamo': forms.TextInput(attrs={'class': 'form-control w-100'})
        }

    def clean_tasa_de_interes_mensual(self):
        tasa_de_interes_mensual = self.cleaned_data['tasa_de_interes_mensual']
        if tasa_de_interes_mensual is not None:
            return tasa_de_interes_mensual / 100
        else:
            return None
        
    def clean_tasa_de_interes_anual(self):
        tasa_de_interes_anual = self.cleaned_data['tasa_de_interes_anual']
        if tasa_de_interes_anual is not None:
            return tasa_de_interes_anual / 100
        else:
            return None
        
#endregion

class AhorroForm(forms.ModelForm):
    class Meta:
        model = Ahorro
        
        fields = ['fecha', 'monto', 'tipo']