from .models import PlazoFijo

def interes_diario():
    plazos = PlazoFijo.objects.all()
    for plazo in plazos:
        plazo.calcular_intereses()