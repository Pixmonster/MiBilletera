from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpResponse
from . models import *


def index(request):
    return render(request, 'test1/index.html')

@login_required
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
            messages.success(request, 'Inicio de sesión exitoso.')
            return redirect('panel')  # Redirigir a la página de inicio después del inicio de sesión
        else:
            messages.error(request, 'Credenciales inválidas. Por favor, verifica tus datos.')
            
    return render(request, 'registration/login.html')

