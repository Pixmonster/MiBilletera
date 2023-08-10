from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from . models import *


def index(request):
    return render(request, 'test1/index.html')


def panel(request):
    return render (request,'test1/home.html')

def exit(request):
    logout(request)
    return redirect('/')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Verificar si el nombre de usuario ya existe
        if Usuario.objects.filter(email=email).exists():
            # Manejar el error de nombre de usuario duplicado aquí
            # Por ejemplo, podrías mostrar un mensaje de error en la plantilla.
            error_message = ("El correo ya está en uso.")
            return render(request, 'test1/register.html', {'error_message': error_message})
        
        # Crear y guardar el usuario en la base de datos
        nuevo_usuario = Usuario(username=username, email=email, password=password)
        nuevo_usuario.save()
        
        return redirect('login')  # Redirigir a la página de inicio

    return render(request, 'test1/register.html')



def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Inicio de sesión exitoso.')
            return redirect('panel')  # Redirigir a la página de inicio después del inicio de sesión
        else:
            messages.error(request, 'Credenciales inválidas. Por favor, verifica tus datos.')
            
    return render(request, 'login.html')

