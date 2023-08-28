from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    # Agrega los atributos 'related_name' en las relaciones
    def __str__(self):
        return str(self.id)

class Cuentas (models.Model):
    saldo = models.DecimalField(max_digits=15, decimal_places=2, blank=False, null=False)
    fk_user = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True, limit_choices_to={'is_superuser': False})

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
    fk_cuenta = models.ForeignKey(Cuentas, on_delete=models.CASCADE) 

    def save(self, *args, **kwargs):
        super(Transacciones, self).save(*args, **kwargs)
        cuenta = self.fk_cuenta
        if self.es_ingreso:
            cuenta.actualizar_saldo(self.monto)
        else:
            cuenta.actualizar_saldo(-self.monto)
    def __str__(self):
        return f"{self.fecha.strftime('%Y-%m-%d')} - {self.monto}"