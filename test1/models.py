from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    # Agrega los atributos 'related_name' en las relaciones
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name='usuarios_groups'  # Cambio de 'user_set' a 'usuarios_groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='usuarios_permissions'  # Cambio de 'user_set' a 'usuarios_permissions'
    )
    
    def __str__(self):
        return self.email

class Cuentas (models.Model):
    tipo = models.CharField(max_length=50, blank=False, null=False)
    saldo = models.IntegerField(blank=False, null=False) # Se va a llenar o restar con un trigger desde Transacciones

    def __str__(self):
        return self.tipo

class Transacciones (models.Model):
    fecha = models.DateField (default=datetime.now())
    monto = models.IntegerField (blank=False, null=False)
    fuente = models.CharField(max_length=20)
    categoria = models.CharField(max_length=50)

    def __str__(self):
        return self.fuente
    
