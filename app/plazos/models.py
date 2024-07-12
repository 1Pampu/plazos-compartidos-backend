from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

# Create your models here.
class PlazoFijo(models.Model):
    monto = models.FloatField(default=0)
    interes = models.FloatField(null=False)
    titulo = models.CharField(max_length=100)
    dia = models.IntegerField(null=False, validators=[MinValueValidator(1), MaxValueValidator(31)])
    num_entidades = models.IntegerField(default=0)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo

    def calcular_monto(self):
        monto = 0
        entidades = Entidad.objects.filter(plazo=self)

        if not entidades:
            return monto

        for entidad in entidades:
            monto += entidad.monto
        return monto

    def calcular_intereses(self):
        entidades = Entidad.objects.filter(plazo=self)
        for entidad in entidades:
            if entidad.monto > 0:
                interes = (entidad.monto * self.interes) / 100
                operacion = Operacion.objects.create(
                    tipo='Interes',
                    monto=interes,
                    fecha=timezone.localtime(timezone.now()).date(),
                    entidad=entidad,
                    plazo=self,
                    nuevo_monto=entidad.monto + interes
                    )
                entidad.monto += interes
                entidad.save()
                self.monto += interes
        self.save()

class Entidad(models.Model):
    nombre = models.CharField(max_length=100)
    monto = models.FloatField(null=False, blank=False, default=0)
    plazo = models.ForeignKey(PlazoFijo, on_delete=models.CASCADE)

    def generar_interes(self, fecha):
        interes = (self.monto * self.plazo.interes) / 100
        operacion = Operacion.objects.create(
            tipo='Interes',
            monto=interes,
            fecha=fecha,
            entidad=self,
            plazo=self.plazo,
            nuevo_monto=self.monto + interes
            )
        self.monto += interes
        return True

    def __str__(self):
        return self.nombre

class Operacion(models.Model):
    TIPO_CHOICES = [
        ('Deposito', 'Depósito'),
        ('Retiro', 'Retiro'),
        ('Interes', 'Interés'),
    ]

    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    monto = models.FloatField(null=False, blank=False, validators=[MinValueValidator(0)])
    fecha = models.DateField(null=False, blank=False)
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE)
    plazo = models.ForeignKey(PlazoFijo, on_delete=models.CASCADE)
    nuevo_monto = models.FloatField(null=False, blank=False)

    def __str__(self):
        return self.monto