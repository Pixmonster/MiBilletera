from django.db import models
from datetime import date

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

