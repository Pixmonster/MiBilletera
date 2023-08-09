from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import HttpResponse

def index(request):
    return render(request, 'test1/index.html')

@login_required
def panel(request):
    return render (request,'test1/login.html')

def exit(request):
    logout(request)
    return redirect('/')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Iniciar sesión automáticamente después del registro
            return redirect('panel')  # Cambia 'home' por la URL a la que quieres redirigir después del registro
    else:
        form = UserCreationForm()
    return render(request, 'test1/register.html', {'form': form})

