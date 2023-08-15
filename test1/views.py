from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, login, authenticate
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.http import HttpResponse
from .models import *
from .forms import *


def index(request):
    return render(request, 'test1/index.html')

@never_cache
@login_required
def panel(request):
    return render (request,'test1/home.html')

def exit(request):
    logout(request)
    return redirect('logear')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if Usuario.objects.filter(username=username).exists():
            # Manejar el error de nombre de usuario duplicado aquí
            error_message = ("El usuario ya está en uso.")
            return render(request, 'test1/register.html', {'error_message': error_message})
        
        
        # Crear y guardar el usuario en la base de datos
        nuevo_usuario = Usuario(username=username, email=email, password=password)
        nuevo_usuario.save()
        
        return redirect('login')  # Redirigir a la página de inicio

    return render(request, 'test1/register.html')


def logear(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        try:
            user = Usuario.objects.get(username=username, password=password)
        except Usuario.DoesNotExist:
            user = None
        
        if user is not None:
            login(request, user)
            return redirect('panel')  # Redirigir a la página de inicio después del inicio de sesión
        else:
            messages.error(request, 'Credenciales inválidas. Por favor, verifica tus datos.')
            
    return render(request, 'registration/login.html')

def nuevo_ingreso(request):
    if request.method == 'POST':
        form = TransaccionesForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ingreso guardado correctamente')
            return redirect('nuevo_ingreso') # Usar redirect para que cuando el formulario se envíe no se recargue con todos los campos llenos
    else:
        form = TransaccionesForm()
    return render(request, 'test1/nuevo_ingreso.html', {'form': form})
<<<<<<< HEAD

def ver_ingreso(request):
    return render(request, 'test1/ver_ingresos.html')
=======
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
>>>>>>> 24d48cf74de3e5d4980629a970a095f7838468d5
