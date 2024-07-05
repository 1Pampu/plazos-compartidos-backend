from django.core.management.base import BaseCommand
from app.plazos.tasks import interes_diario

class Command(BaseCommand):
    help = 'Generar los intereses diarios de los plazos fijos.'

    def handle(self, *args, **options):
        resultado = interes_diario()
        self.stdout.write(self.style.SUCCESS(resultado))