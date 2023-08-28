from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, login, authenticate
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.http import HttpResponse
from .models import *
from .forms import *
from datetime import datetime, timedelta
from django.db.models import Sum
import locale
import requests
import cachetools
from django.views.decorators.cache import cache_control

def index(request):
    return render(request, 'test1/index.html')

#region PANEL

# Crea un caché con una política de expiración (por ejemplo, 1 hora)
cache = cachetools.TTLCache(maxsize=100, ttl=3600)  # 1 hora en segundos

def get_exchange_rate(from_currency, to_currency):
    cache_key = f"exchange_rate_{from_currency}_{to_currency}"
    cached_rate = cache.get(cache_key)
    
    if cached_rate:
        return cached_rate
    
    api_key = 'R4FODY1WJFVUIAM6'
    endpoint = 'https://www.alphavantage.co/query'

    params = {
        'function': 'CURRENCY_EXCHANGE_RATE',
        'from_currency': from_currency,
        'to_currency': to_currency,
        'apikey': api_key
    }

    response = requests.get(endpoint, params=params)
    data = response.json()

    if 'Realtime Currency Exchange Rate' in data:
        exchange_rate_data = data['Realtime Currency Exchange Rate']
        exchange_rate = exchange_rate_data.get('5. Exchange Rate', 'No disponible')
        cache[cache_key] = exchange_rate
        return exchange_rate
    else:
        return 'No disponible'

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def panel(request):
    fecha_actual = datetime.now()
    locale.setlocale(locale.LC_ALL, ("es_ES", "UTF-8"))
    filter_mes = Transacciones.objects.filter(fecha__month=fecha_actual.month).aggregate(Sum('monto'))['monto__sum'] or 0
    total_ingresos = Transacciones.objects.filter(es_ingreso=True).aggregate(Sum('monto'))['monto__sum'] or 0
    mes_actual = fecha_actual.strftime("%b")
    
    from_currency = 'USD'  # Moneda base (USD)
    to_currencies = ['EUR', 'JPY', 'GBP', 'AUD', 'COP']  # Monedas a convertir

    rates = {}

    for currency in to_currencies:
        rates[currency] = get_exchange_rate(from_currency, currency)

    context = {
        'total_ingresos': total_ingresos,
        'filter_mes': filter_mes,
        'mes_actual': mes_actual,
        'rates': rates  # Agrega las tasas de cambio al contexto
    }
    return render (request,'test1/home.html', context)

def exit(request):
    logout(request)
    return redirect('logear')
#endregion

#region USUARIO
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if Usuario.objects.filter(username=username).exists():
            # Manejar el error de nombre de usuario duplicado aquí
            error_message = ("El usuario ya está en uso.")
            return render(request, 'test1/register.html', {'error_message': error_message})
        if Usuario.objects.filter(email=email).exists():
            # Manejar el error de nombre de usuario duplicado aquí
            error_message = ("El email ya está en uso.")
            return render(request, 'test1/register.html', {'error_message': error_message})
        
        if Usuario.objects.filter(email=email).exists():
            # Manejar el error de nombre de usuario duplicado aquí
            error_message = ("Email ya está en uso.")
            return render(request, 'test1/register.html', {'error_message': error_message})
        
        
        # Crear y guardar el usuario en la base de datos
        
        nuevo_usuario = Usuario(username=username, email=email, password=password)
        nuevo_usuario.save()
        nueva_cuenta = Cuentas(saldo=0, fk_user=nuevo_usuario)
        nueva_cuenta.save()
        return redirect('login')  # Redirigir a la página de inicio

    return render(request, 'test1/register.html')


def logear(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        try:
            user = Usuario.objects.get(email=email, password=password)
        except Usuario.DoesNotExist:
            user = None
        
        if user is not None:
            login(request, user)
            return redirect('panel')  # Redirigir a la página de inicio después del inicio de sesión
        else:
            messages.error(request, 'Credenciales inválidas. Por favor, verifica tus datos.')
            
    return render(request, 'registration/login.html')

@login_required
def eliminar_usuario(request, user_id):
    usuario = get_object_or_404(Usuario, id=user_id)
    
    if usuario == request.user:
        usuario.delete()
        messages.success(request, 'Tu cuenta ha sido eliminada correctamente.')
        return redirect('index')
    else:
        messages.error(request, 'No tienes permiso para eliminar esta cuenta.')
        return redirect('panel')
    
#endregion

#region INGRESOS
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def nuevo_ingreso(request):
    if request.method == 'POST':
        form = TransaccionesForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ingreso guardado correctamente')
            return redirect('nuevo_ingreso') # Usar redirect para que cuando el formulario se envíe no se recargue con todos los campos llenos
    else:
        form = TransaccionesForm()

    fuentes_ingreso = FuenteIngreso.objects.all()
    form.fields['fk_fuente'].queryset = fuentes_ingreso
    return render(request, 'test1/nuevo_ingreso.html', {'form': form})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def ver_ingreso(request):
    transacciones = Transacciones.objects.filter(fk_cuenta__fk_user=request.user, es_ingreso=True)
    
    context = {
        'transacciones': transacciones
    }
    return render(request, 'test1/ver_ingresos.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def borrar_ingreso(request, id):
    transacciones = Transacciones.objects.get(id=id)
    transacciones.delete()
    return redirect('/ver_ingreso/')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def editar_ingreso(request, id):
    transacciones = Transacciones.objects.get(id=id)

    if(request.method == 'GET'):
        formatted_fecha = transacciones.fecha.strftime('%Y-%m-%d')  # Formatear la fecha
        form = TransaccionesForm(instance = transacciones, initial={'fecha': formatted_fecha})
        context = {
            'form': form,
            'id': id,
            'fecha_actual': transacciones.fecha, 
        }
        return render(request, 'test1/editar_ingresos.html', context)
    
    if(request.method == 'POST'):
        form = TransaccionesForm(request.POST, instance = transacciones)
        if form.is_valid():
            form.save()
        context = {
            'form': form,
            'id': id,
            'fecha_actual': transacciones.fecha,
        }
        return redirect('/ver_ingreso/')
    
#endregion