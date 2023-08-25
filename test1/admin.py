from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Usuario)
admin.site.register(Cuentas)
admin.site.register(Transacciones)
admin.site.register(FuenteIngreso)
admin.site.register(CategoriaGasto)
