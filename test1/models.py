from django.db import models
from datetime import date
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    # Agrega los atributos 'related_name' en las relaciones
    email = models.EmailField(unique=True)
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

class Ingresos (models.Model):
    cantidad_ingreso = models.IntegerField(blank=False, null= False)
    fuente_ingreso = models.CharField(max_length=50, blank=True, null=True)
    fecha_ingreso = models.DateField()

    def __str__(self):
        return self.fuente_ingreso

class Ahorros (models.Model):
    monto_ahorro = models.IntegerField(blank=False, null=False)
    fecha_ini_ahorro = models.DateField()
    fecha_fin_ahorro = models.DateField()
    ingresos = models.ForeignKey(Ingresos, on_delete=models.CASCADE)

    def __str__(self):
        return self.monto_ahorro

class Gastos (models.Model):
    monto_gasto = models.IntegerField(blank=False, null=False)

    def __str__(self):
        return self.monto_gasto

