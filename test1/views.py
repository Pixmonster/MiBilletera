from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.http import HttpResponse

def index(request):
    return render(request, 'test1/index.html')

@login_required
def panel(request):
    return render (request,'test1/base.html')

def exit(request):
    logout(request)
    return redirect('/')

