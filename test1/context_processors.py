from .models import Recordatorio
from django.db.models import Q
from datetime import date 

def notificaciones_context(request):
    context = {}
    if request.user.is_authenticated:
        usuario_actual = request.user
        hoy = date.today()
        recordatorios = Recordatorio.objects.filter(
            Q(fecha__day=hoy.day) | Q(fecha__day=hoy.day - 1),
            usuario=usuario_actual
        )
        context['recordatorios'] = recordatorios
    return context