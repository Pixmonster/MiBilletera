from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth import logout, login
from django.contrib import messages
from django.http.response import JsonResponse
from .models import *
from .forms import *
from datetime import datetime, datetime
from django.db.models import Sum
import locale
import requests
import cachetools
from django.views.decorators.cache import cache_control
from django.db.models import Q
from django.urls import reverse
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
import logging
from decimal import Decimal
from datetime import date
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.db.models import Sum, F
from django.db.models.functions import TruncMonth, TruncWeek, TruncDay
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

logger = logging.getLogger(__name__)

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
    usuario_actual = request.user  # Usuario actualmente autenticado
    fecha_actual = datetime.now()
    locale.setlocale(locale.LC_ALL, ("es_ES", "UTF-8"))

# FILTROS DE MOVIMIENTOS

    filter_mes_ingresos = Transacciones.objects.filter(
        fk_cuenta__fk_user=usuario_actual,
        fecha__month=fecha_actual.month,
        es_ingreso = True
    ).aggregate(Sum('monto'))['monto__sum'] or 0

    filter_mes_gastos = Transacciones.objects.filter(
        fk_cuenta__fk_user=usuario_actual,
        fecha__month=fecha_actual.month,
        es_ingreso = False
    ).aggregate(Sum('monto'))['monto__sum'] or 0
    
    total_ingresos = Transacciones.objects.filter(
        fk_cuenta__fk_user=usuario_actual,
        es_ingreso=True
    ).aggregate(Sum('monto'))['monto__sum'] or 0

    total_gastos = Transacciones.objects.filter(
        fk_cuenta__fk_user=usuario_actual,
        es_ingreso=False
    ).aggregate(Sum('monto'))['monto__sum'] or 0

# MONTO TOTAL
    cuenta = Cuentas.objects.get(fk_user=usuario_actual)
    monto_total = cuenta.saldo

# MONTO MES
    monto_mes = (filter_mes_ingresos - filter_mes_gastos)

# MES ACTUAL
    mes_actual = fecha_actual.strftime("%b")

# USO API DE CAMBIOS DE MONEDA

    from_currency = 'USD'  # Moneda base (USD)
    to_currencies = ['EUR', 'JPY', 'GBP', 'AUD', 'COP']  # Monedas a convertir

    rates = {}

    for currency in to_currencies:
        rates[currency] = get_exchange_rate(from_currency, currency)

# INGRESOS Y GASTOS MÁS RECIENTES

    ingresos_recientes = Transacciones.objects.filter(fk_cuenta__fk_user=usuario_actual, es_ingreso=True).order_by('-fecha')[:3]
    gastos_recientes = Transacciones.objects.filter(fk_cuenta__fk_user=usuario_actual, es_ingreso=False).order_by('-fecha')[:3]

    context = {
        'total_ingresos': total_ingresos,
        'total_gastos': total_gastos,
        'monto_total': monto_total,
        'filter_mes_ingresos': filter_mes_ingresos,
        'filter_mes_gastos': filter_mes_gastos,
        'mes_actual': mes_actual,
        'rates': rates,  # Agrega las tasas de cambio al contexto
        'ingresos_recientes': ingresos_recientes,
        'gastos_recientes': gastos_recientes,
        'monto_mes': monto_mes,
        'usuario': usuario_actual # Para la foto de perfil
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
        hashed_password = make_password(password)  # Encripta la contraseña
        nuevo_usuario = Usuario(username=username, email=email, password=hashed_password)
        nuevo_usuario.save()
        # Crear y guardar la cuenta en la base de datos
        nueva_cuenta = Cuentas(saldo=0, fk_user=nuevo_usuario)
        nueva_cuenta.save()
        return redirect('login')  # Redirigir a la página de inicio

    return render(request, 'test1/register.html')

def logear(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        try:
            user = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            user = None
        
        if user is not None and check_password(password, user.password):
            # La contraseña es válida, inicia sesión
            login(request, user)
            return redirect('panel')  # Redirige a la página de inicio después del inicio de sesión
        else:
            # Las credenciales son inválidas, muestra un mensaje de error
            messages.error(request, 'Credenciales inválidas. Por favor, verifica tus datos.')
            
    return render(request, 'registration/login.html')

@login_required
def ver_perfil(request):
    usuario = request.user  # Obtener el usuario autenticado
    return render(request, 'test1/ver_perfil.html', {'usuario': usuario})

@login_required
def actualizar_imagen(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Su imagen fue actualizada")
            return redirect("ver_perfil")
        else:
            logger.error("Error al procesar el formulario de imagen: %s", form.errors)
            messages.error(request, "Ooops!! ocurrió un error")
    else:
        form = ImageForm(instance=request.user)

    return render(request, "test1/ver_perfil.html", {'form': form})
    
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
    usuario_actual = request.user
    if request.method == 'POST':
        form = IngresosForm(request.POST)
        if form.is_valid():
            ingreso = form.save(commit=False)# Guarda el formulario pero no en la base de datos todavía
            cuenta_usuario = Cuentas.objects.get(fk_user=usuario_actual)

            ingreso.fk_cuenta = cuenta_usuario
            ingreso.save()  # Ahora sí guarda la transacción en la base de datos
            
            messages.success(request, 'Ingreso guardado correctamente')
            return redirect('nuevo_ingreso') # Usar redirect para que cuando el formulario se envíe no se recargue con todos los campos llenos
    else:
        form = IngresosForm()
        
    fuente_ingreso = FuenteIngreso.objects.filter(
        Q(fk_user=usuario_actual) | Q(fk_user__isnull=True)
    )

    form.fields['fk_fuente'].queryset = fuente_ingreso
    form_fuente = FuentePersonalizadaForm()
    return render(request, 'test1/nuevo_ingreso.html', {'form': form, 'form_fuente': form_fuente, 'usuario': usuario_actual})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def list_ingresos(request):
    transacciones = Transacciones.objects.filter(fk_cuenta__fk_user=request.user, es_ingreso=True).values('id', 'fecha', 'monto', 'fk_fuente__nombre_fuente')

    for transaccion in transacciones:
        transaccion['url_edicion'] = reverse('editar_ingreso', args=[transaccion['id']])

    context = {
        'transacciones': list(transacciones),

    }
    return JsonResponse(context, safe=False)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def ver_ingreso(request):
    transacciones = Transacciones.objects.filter(fk_cuenta__fk_user=request.user, es_ingreso=True)
    
    context = {
        'transacciones': transacciones,
        'usuario': request.user
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
    usuario_actual = request.user
    transaccion = Transacciones.objects.get(id=id)
    if request.method == 'GET':
        formatted_fecha = transaccion.fecha.strftime('%Y-%m-%d')
        form = IngresosForm(instance=transaccion, initial={'fecha': formatted_fecha})
        context = {
            'form': form,
            'id': id,
            'fecha_actual': transaccion.fecha,
            'usuario': usuario_actual
        }
        return render(request, 'test1/editar_ingresos.html', context)

    if request.method == 'POST':
        form = IngresosForm(request.POST, instance=transaccion)
        if form.is_valid():
            # Guarda la transacción y actualiza el saldo en el modelo Transacciones
            form.save()
            return redirect('/ver_ingreso/')
    
#endregion

#region GASTOS
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def nuevo_gasto (request):
    usuario_actual = request.user
    if request.method == 'POST':
        form = GastosForm(request.POST)
        if form.is_valid():
            gasto = form.save(commit=False)
            cuenta_usuario = Cuentas.objects.get(fk_user=usuario_actual)

            gasto.fk_cuenta = cuenta_usuario
            gasto.es_ingreso = False  # Establecer es_ingreso en False para los gastos
            gasto.save()

            messages.success(request, 'Gasto guardado correctamente')
            return redirect('nuevo_gasto')
    else:
        form = GastosForm()
        
    categoria_gasto = CategoriaGasto.objects.filter(
        Q(fk_user=usuario_actual) | Q(fk_user__isnull=True)
    )

    form.fields['fk_categoria'].queryset = categoria_gasto
    form_categoria = CategoriaPersonalizadaForm()  # formulario de categoría
    return render (request, 'test1/nuevo_gasto.html', {'form': form, 'form_categoria': form_categoria, 'usuario': usuario_actual})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def list_gastos(request):
    transacciones = Transacciones.objects.filter(fk_cuenta__fk_user=request.user, es_ingreso=False).values('id', 'fecha', 'monto', 'fk_categoria__nombre_categoria')

    for transaccion in transacciones:
        transaccion['url_edicion'] = reverse('editar_gasto', args=[transaccion['id']])

    context = {
        'transacciones': list(transacciones)
    }
    return JsonResponse(context, safe=False)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def ver_gastos(request):
    transacciones = Transacciones.objects.filter(fk_cuenta__fk_user=request.user,es_ingreso=False)

    context = {
        'transacciones': transacciones,
        'usuario': request.user
    }
    return render(request, 'test1/ver_gastos.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def borrar_gasto(request, id):
    transacciones = Transacciones.objects.get(id=id)
    transacciones.delete()
    return redirect('ver_gasto')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def editar_gasto(request, id):
    usuario_actual = request.user
    transaccion = Transacciones.objects.get(id=id)
    if request.method == 'GET':
        formatted_fecha = transaccion.fecha.strftime('%Y-%m-%d')
        form = GastosForm(instance=transaccion, initial={'fecha': formatted_fecha})
        context = {
            'form': form,
            'id': id,
            'fecha_actual': transaccion.fecha,
            'usuario': usuario_actual
        }
        return render(request, 'test1/editar_gastos.html', context)

    if request.method == 'POST':
        form = GastosForm(request.POST, instance=transaccion)
        if form.is_valid():
            # Guarda la transacción y actualiza el saldo en el modelo Transacciones
            form.save()
            return redirect('/ver_gasto/')
#endregion

#region CATEGORIA Y FUENTE PERSONALIZADOS
@login_required
def crear_categoria_personalizada(request):
    if request.method == 'POST':
        form_categoria = CategoriaPersonalizadaForm(request.POST)
        if form_categoria.is_valid():
            categoria = form_categoria.save(commit=False)
            categoria.fk_user = request.user  # Asigna el usuario actual
            categoria.save()
            messages.success(request, 'Nueva categoria  guardada correctamente')
            return redirect('nuevo_gasto')
        
        # Resto del código en caso de formulario no válido
    else:
        form_categoria = CategoriaPersonalizadaForm()
    return render(request, 'test1/form_categoria_personalizada.html', {'form_categoria': form_categoria})

@login_required
def crear_fuente_personalizada(request):
    if request.method == 'POST':
        form_fuente = FuentePersonalizadaForm(request.POST)
        if form_fuente.is_valid():
            fuente = form_fuente.save(commit=False)
            fuente.fk_user = request.user  # Asigna el usuario actual
            fuente.save()
            messages.success(request, 'Nueva fuente guardada correctamente')
            return redirect('nuevo_ingreso')
    else:
        form_fuente = FuentePersonalizadaForm()
    return render(request, 'nuevo_ingreso.html', {'form_categoria': form_fuente})

#endregion

#region DEUDAS

def calcular_interes_fijo(valor_total_deuda, tasa_de_interes_mensual):
    return valor_total_deuda * tasa_de_interes_mensual

def calcular_interes_simple(valor_total_deuda, tasa_de_interes_anual, plazo_del_prestamo_en_meses):
    tasa_de_interes_mensual = tasa_de_interes_anual / 12
    interes_mensual = valor_total_deuda * tasa_de_interes_mensual * plazo_del_prestamo_en_meses
    return interes_mensual

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def nueva_deuda(request):
    usuario_actual = request.user
    if request.method == 'POST':
        form_deuda = DeudasForm(request.POST)
        if form_deuda.is_valid():
            try:
                valor_total_deuda = Decimal(form_deuda.cleaned_data['valor_total_deuda'] or 0)  # Si es None, se establece como 0
                tasa_de_interes_mensual = Decimal(form_deuda.cleaned_data['tasa_de_interes_mensual'] or 0)  # Si es None, se establece como 0
                tasa_de_interes_anual = Decimal(form_deuda.cleaned_data['tasa_de_interes_anual'] or 0)  # Si es None, se establece como 0
                plazo_del_prestamo = form_deuda.cleaned_data['plazo_del_prestamo'] or 0  # Si es None, se establece como 0
                tipo_de_interes = form_deuda.cleaned_data['tipo_de_interes']

                # Calcula el interés según el tipo seleccionado
                if tipo_de_interes == 'Fijo':
                    interes_mes = calcular_interes_fijo(valor_total_deuda, tasa_de_interes_mensual)
                elif tipo_de_interes == 'Simple':
                    interes_mes = calcular_interes_simple(valor_total_deuda, tasa_de_interes_anual, plazo_del_prestamo)
            
                # Crea una instancia del modelo Deuda y guarda los datos en la base de datos
                deuda = form_deuda.save(commit=False)
                deuda.fk_user = request.user
                deuda.valor_interes_mensual = Decimal(interes_mes)  # Almacena el interés en el campo 'valor_interes'
                deuda.save()

                # Crear el recordatorio
                dia_pago = deuda.dia_pago  # Obtiene el día de pago de la deuda
                hoy = date.today()

                # Verifica si el día de pago ya pasó en este mes
                if hoy.day > dia_pago:
                    fecha_recordatorio = hoy.replace(day=dia_pago, month=hoy.month + 1)
                else:
                    fecha_recordatorio = hoy.replace(day=dia_pago)

                mensaje_recordatorio = f"Recuerda pagar la deuda: {deuda.descripcion_deuda}"
                recordatorio = Recordatorio(fecha=fecha_recordatorio, mensaje=mensaje_recordatorio, usuario=request.user, deuda=deuda)
                recordatorio.save()

                # Redirige a alguna otra vista o página después de guardar
                return redirect('nueva_deuda')

            except Exception as e:
                print("Error al guardar en la base de datos:", str(e))
                messages.error(request, 'Hubo un error al guardar la nueva deuda.')
        else:
            print("El formulario no es válido:", form_deuda.errors)
    else:
        form_deuda = DeudasForm()
    return render(request, 'test1/nueva_deuda.html', {'form_deuda': form_deuda, 'usuario': usuario_actual})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def ver_deudas(request):
    deudas = Deudas.objects.filter(fk_user=request.user)

    context = {
        'deudas': deudas,
        'usuario': request.user
    }
    return render(request, 'test1/ver_deudas.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def list_deudas(request):
    deudas = Deudas.objects.filter(fk_user=request.user).values('id', 'descripcion_deuda', 'dia_pago', 'valor_total_deuda', 'tipo_de_interes', 'valor_interes_mensual')

    for deuda in deudas:
        deuda['url_edicion'] = reverse('editar_deuda', args=[deuda['id']])

    context = {
        'deudas': list(deudas)
    }
    return JsonResponse(context, safe=False)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def editar_deuda(request, id):
    usuario_actual = request.user
    transaccion = Transacciones.objects.get(id=id)
    if request.method == 'GET':
        formatted_fecha = transaccion.fecha.strftime('%Y-%m-%d')
        form = GastosForm(instance=transaccion, initial={'fecha': formatted_fecha})
        context = {
            'form': form,
            'id': id,
            'fecha_actual': transaccion.fecha,
            'usuario': usuario_actual
        }
        return render(request, 'test1/editar_gastos.html', context)

    if request.method == 'POST':
        form = GastosForm(request.POST, instance=transaccion)
        if form.is_valid():
            # Guarda la transacción y actualiza el saldo en el modelo Transacciones
            form.save()
            return redirect('/ver_gasto/')

#endregion

#region Graficos


def generar_grafico(request):
    if request.method == "POST":
        option = request.POST.get('option')
        tipo = request.POST.get('tipo')
        model = None
        fields = None

        if option == 'ingresos':
            model = Transacciones
            fields = {'es_ingreso': True}
        elif option == 'gastos':
            model = Transacciones
            fields = {'es_ingreso': False}
        elif option == 'ahorros':
            model = Ahorro
            fields = {'monto__isnull': False}  # Ajusta según tus necesidades


        graphic = generate_chart(request, option, tipo, model, fields)
        context = {'graphic': graphic}
        return render(request, 'test1/grafico.html', context)

    return render(request, 'test1/grafico.html', {})

@login_required
def generate_chart(request, option, tipo, model, fields, group_by_field='fecha'):
    items = model.objects.filter(**fields)
    if option == 'ahorros':
        if tipo == 'mensual':
            items = items.annotate(period=TruncMonth('fecha')).filter(period__month=datetime.now().month)
        elif tipo == 'semanal':
            items = items.annotate(period=TruncWeek('fecha')).filter(period__week=datetime.now().isocalendar()[1])
        elif tipo == 'diario':
            items = items.annotate(period=TruncDay('fecha')).filter(period=datetime.now().date())

        # Filtra por cuenta si es necesario, ajusta según tus necesidades
        usuario_actual = request.user
        items = items.filter(fk_cuenta__fk_user=usuario_actual)

        xlabel, title = tipo, 'Ahorros'
    else:
        if tipo == 'mensual':
            group_by = TruncMonth(group_by_field)
            xlabel, title = 'Mes', 'Ingresos' if 'es_ingreso' in fields and fields['es_ingreso'] else 'Gastos'
        elif tipo == 'semanal':
            group_by = TruncWeek(group_by_field)
            xlabel, title = 'Semana', 'Ingresos' if 'es_ingreso' in fields and fields['es_ingreso'] else 'Gastos'
        elif tipo == 'diario':
            group_by = TruncDay(group_by_field)
            xlabel, title = 'Día', 'Ingresos' if 'es_ingreso' in fields and fields['es_ingreso'] else 'Gastos'


        data = items.annotate(
            period=group_by
        ).values('period').annotate(
            total=Sum('monto')
        ).order_by('period')
        if not data:
            print("No hay datos para mostrar.")

        labels = [item['period'].strftime('%b %Y' if tipo == 'mensual' else '%b %d %Y') for item in data]
        totals = [item['total'] for item in data]

        fig, ax = plt.subplots()
        ax.bar(labels, totals)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(f'Total de {title.lower()}')
        ax.set_title(f'{title} {xlabel}')
        plt.xticks(rotation=15, ha='right')

        buffer = BytesIO()
        fig.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()

        graphic = base64.b64encode(image_png).decode('utf-8')
        return graphic
#endregion


#region ahorros
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def nuevo_ahorro(request):
    usuario_actual = request.user
    if request.method == 'POST':
        form = AhorroForm(request.POST)
        print(form) 
        if form.is_valid():
            fecha = form.cleaned_data['fecha']
            monto = form.cleaned_data['monto']
            tipo = form.cleaned_data['tipo']
            cuenta_usuario = Cuentas.objects.get(fk_user=usuario_actual) # Se obtiene la cuenta del usuario
            nuevo_ahorro = Ahorro(fecha=fecha, monto=monto, tipo=tipo, fk_cuenta=cuenta_usuario)
            nuevo_ahorro.save()
            cuenta_usuario.saldo -= monto 
            cuenta_usuario.save()
            messages.success(request, 'Ahorro guardado correctamente')
            return redirect('nuevo_ahorro')
    else:
        form = AhorroForm()
    return render(request, 'test1/nuevo_ahorro.html', {'form': form})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def ver_ahorros(request):
    usuario_actual = request.user
    ahorros = Ahorro.objects.filter(fk_cuenta__fk_user=usuario_actual)
    total_ahorros = ahorros.aggregate(total=Sum('monto'))['total']

    if request.method == 'POST':
        form = AhorroForm(request.POST)
        if form.is_valid():
            monto_devuelto = form.cleaned_data['monto_a_devolver']
            if monto_devuelto <= total_ahorros:
                cuenta_usuario = Cuentas.objects.get(fk_user=usuario_actual)
                cuenta_usuario.saldo += monto_devuelto
                cuenta_usuario.save()

                # Resta el monto devuelto de los ahorros
                for ahorro in ahorros:
                    if monto_devuelto > 0:
                        if ahorro.monto > monto_devuelto:
                            ahorro.monto -= monto_devuelto
                            monto_devuelto = 0
                            ahorro.save()
                        else:
                            monto_devuelto -= ahorro.monto
                            ahorro.delete()

    else:
        form = AhorroForm()

    return render(request, 'test1/ver_ahorros.html', {'ahorros': ahorros, 'total_ahorros': total_ahorros, 'form': form})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def editar_ahorro(request, id):
    usuario_actual = request.user
    ahorro = Ahorro.objects.get(id=id)
    monto_anterior = ahorro.monto  
    cuenta_usuario = Cuentas.objects.get(fk_user=usuario_actual)
    if request.method == 'GET':
        form = AhorroForm(instance=ahorro)
        context = {
            'form': form,
            'id': id,
        }
        return render(request, 'test1/editar_ahorro.html', context)

    if request.method == 'POST':
        form = AhorroForm(request.POST, instance=ahorro)
        if form.is_valid():
            nuevo_monto = form.cleaned_data['monto']
            diferencia_monto = nuevo_monto - monto_anterior
            form.save()
            cuenta_usuario.saldo += diferencia_monto
            cuenta_usuario.save()
            return redirect('ver_ahorros') 


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def borrar_ahorro(request, id):
    ahorro = Ahorro.objects.get(id=id)
    usuario_actual = request.user
    cuenta_usuario = Cuentas.objects.get(fk_user=usuario_actual)
    cuenta_usuario.saldo += ahorro.monto
    cuenta_usuario.save()
    ahorro.delete()
    return redirect('/ver_ahorros/')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def list_ahorro(request):

    usuario_actual = request.user
    ahorros = Ahorro.objects.filter(fk_cuenta__fk_user=usuario_actual)
    

    ahorros_data = []

    for ahorro in ahorros:
        ahorro_info = {
            'id': ahorro.id,
            'fecha': ahorro.fecha.strftime('%Y-%m-%d'), 
            'tipo' : ahorro.tipo,
            'monto': ahorro.monto,
            'url_edicion': reverse('editar_ahorro', args=[ahorro.id]),  
        }
        ahorros_data.append(ahorro_info)


    context = {
        'ahorros': ahorros_data,
    }
    return JsonResponse(context, safe=False)

#endregion

