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

class Cuentas (models.Model):
    tipo = models.CharField(max_length=50, blank=False, null=False)
    saldo = models.DecimalField(max_digits=15, decimal_places=2, blank=False, null=False)

    def actualizar_saldo(self, monto):
        self.saldo += monto
        self.save()

    def __str__(self):
        return self.tipo

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
    monto = models.DecimalField (max_digits=15, decimal_places=2, blank=False, null=False)
    es_ingreso = models.BooleanField(default=True)
    fk_categoria = models.ForeignKey(CategoriaGasto, on_delete=models.CASCADE, null=True, blank=True)
    fk_fuente = models.ForeignKey(FuenteIngreso, on_delete=models.CASCADE, null=True, blank=True)
    fk_cuenta = models.ForeignKey(Cuentas, on_delete=models.CASCADE, default=1) 

    def save(self, *args, **kwargs):
        super(Transacciones, self).save(*args, **kwargs)
        cuenta = self.fk_cuenta
        if self.es_ingreso:
            cuenta.actualizar_saldo(self.monto)
        else:
            cuenta.actualizar_saldo(-self.monto)

    def __str__(self):
        return self.fecha