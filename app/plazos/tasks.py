from .models import PlazoFijo

def interes_diario():
    try:
        plazos = PlazoFijo.objects.all()
        for plazo in plazos:
            plazo.calcular_intereses()
        return 'Intereses diarios generados correctamente.'
    except Exception as e:
        return f'Error al generar los intereses diarios: {e}'