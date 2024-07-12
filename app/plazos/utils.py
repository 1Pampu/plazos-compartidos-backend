from django.utils import timezone
from datetime import timedelta

def generar_lista_fechas(fecha_inicial, fecha_final = timezone.localtime(timezone.now()).date()):
    fecha_inicial += timedelta(days=1)
    fechas = []
    while fecha_inicial <= fecha_final:
        fechas.append(fecha_inicial)
        fecha_inicial += timedelta(days=1)
    return fechas