from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from decimal import Decimal


class Usuario(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    imagen = models.ImageField(upload_to='images', height_field=None, width_field=None, max_length=None, default='static/icon-user.png', null=True, blank=True,)
    # Agrega los atributos 'related_name' en las relaciones
    def __str__(self):
        return str(self.id)

class Cuentas(models.Model):
    saldo = models.DecimalField(max_digits=15, decimal_places=2, blank=False, null=False)
    fk_user = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True, limit_choices_to={'is_superuser': False})

    def actualizar_saldo(self, monto):
        ingresos = Transacciones.objects.filter(fk_cuenta=self, es_ingreso=True).aggregate(total=Sum('monto'))['total']
        gastos = Transacciones.objects.filter(fk_cuenta=self, es_ingreso=False).aggregate(total=Sum('monto'))['total']
        
        # Utilice expresiones F para actualizar el saldo según el valor anterior
        self.saldo = F('saldo') - ExpressionWrapper(F('saldo') - (ingresos or 0) + (gastos or 0) + monto, output_field=DecimalField())
        self.save()

    def __str__(self):
        return str(self.fk_user)

    def __str__(self):
        return str(self.fk_user)
    
class CategoriaGasto (models.Model):
    nombre_categoria = models.CharField (max_length=50, null=False, blank=False)
    fk_user = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True, limit_choices_to={'is_superuser': False}, related_name='categorias_personalizadas')


    def __str__(self):
        return self.nombre_categoria

class FuenteIngreso (models.Model):
    nombre_fuente = models.CharField (max_length=50, null=False, blank=False)
    fk_user = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True, limit_choices_to={'is_superuser': False}, related_name='fuentes_personalizadas')


    def __str__(self):
        return self.nombre_fuente

class Transacciones(models.Model):
    fecha = models.DateField()
    monto = models.DecimalField(max_digits=15, decimal_places=2, blank=False, null=False)
    es_ingreso = models.BooleanField(default=True)
    fk_categoria = models.ForeignKey(CategoriaGasto, on_delete=models.CASCADE, null=True, blank=True)
    fk_fuente = models.ForeignKey(FuenteIngreso, on_delete=models.CASCADE, null=True, blank=True)
    fk_cuenta = models.ForeignKey(Cuentas, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        cuenta = self.fk_cuenta
        super(Transacciones, self).save(*args, **kwargs)

        # Obtén los ingresos y gastos actuales de la cuenta
        ingresos = Transacciones.objects.filter(fk_cuenta=cuenta, es_ingreso=True).aggregate(total=Sum('monto'))['total'] or Decimal('0.0')
        gastos = Transacciones.objects.filter(fk_cuenta=cuenta, es_ingreso=False).aggregate(total=Sum('monto'))['total'] or Decimal('0.0')

        # Calcula el saldo de la cuenta
        cuenta.saldo = ingresos - gastos
        cuenta.save()