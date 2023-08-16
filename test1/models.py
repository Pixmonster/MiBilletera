from django.db import models
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
    
class CategoriaGasto (models.Model):
    nombre_categoria = models.CharField (max_length=50, null=False, blank=False)

    def __str__(self):
        return self.nombre_categoria

class FuenteIngreso (models.Model):
    nombre_fuente = models.CharField (max_length=50, null=False, blank=False)

    def __str__(self):
        return self.nombre_fuente

class Transacciones (models.Model):
    fecha = models.DateField ()
    monto = models.IntegerField (blank=False, null=False)
    fk_categoria = models.ForeignKey(CategoriaGasto, on_delete=models.CASCADE, null=True)
    fk_fuente = models.ForeignKey(FuenteIngreso, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.fuente

class Cuentas (models.Model):
    tipo = models.CharField(max_length=50, blank=False, null=False)
    saldo = models.IntegerField(blank=False, null=False) # Se va a llenar o restar con un trigger desde Transacciones
    transacciones_fk = models.ForeignKey(Transacciones, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.tipo