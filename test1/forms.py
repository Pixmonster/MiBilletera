from django.contrib.auth.forms import UserCreationForm
from .models import *

class UsuarioForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password']