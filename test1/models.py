from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from decimal import Decimal

class Usuario(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    imagen = models.ImageField(upload_to='images', default='images/icon-user.png', null=True, blank=True,)
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

class Deudas(models.Model):
    descripcion_deuda = models.CharField(max_length=50, null= True, blank= True)
    dia_pago = models.IntegerField(null= True, blank= True)
    valor_total_deuda = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    tipo_de_interes = models.CharField(max_length=50, null=True, blank=True)
    tasa_de_interes_anual = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    tasa_de_interes_mensual = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    plazo_del_prestamo = models.IntegerField(null=True, blank=True)
    valor_interes_mensual = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    fk_user = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.descripcion_deuda
    
class Recordatorio(models.Model):
    fecha = models.DateField()
    mensaje = models.CharField(max_length=255)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    activo = models.BooleanField(default=True)
    deuda = models.ForeignKey(Deudas, on_delete=models.CASCADE, related_name='recordatorios', null=True, blank=True)

    def __str__(self):
        return self.mensaje
    
class Ahorro(models.Model):
    tipo = models.CharField(max_length=50, default="Mi ahorro")
    fecha = models.DateField(null=True)
    monto = models.DecimalField(max_digits=15, decimal_places=2, blank=False, null=False)
    fk_cuenta = models.ForeignKey(Cuentas, on_delete=models.CASCADE)

    def __str__(self):
        return self.tipo
    