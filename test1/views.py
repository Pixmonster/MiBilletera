from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, login, authenticate
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.http import HttpResponse
from .models import *
from .forms import *
from datetime import datetime


def index(request):
    return render(request, 'test1/index.html')

#region PANEL
@never_cache
@login_required
def panel(request):
    return render (request,'test1/home.html')

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
        
        
        # Crear y guardar el usuario en la base de datos
        nuevo_usuario = Usuario(username=username, email=email, password=password)
        nuevo_usuario.save()
        
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

@login_required
def ver_ingreso(request):
    transacciones = Transacciones.objects.all()
    context = {
        'transacciones': transacciones
    }
    return render(request, 'test1/ver_ingresos.html', context)

@login_required
def borrar_ingreso(request, id):
    transacciones = Transacciones.objects.get(id=id)
    transacciones.delete()
    return redirect('/ver_ingreso/')

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