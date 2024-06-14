from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

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
        entidades = Entidad.objects.filter(plazo_fijo=self)

        if not entidades:
            return monto

        for entidad in entidades:
            monto += entidad.monto
        return monto

class Entidad(models.Model):
    nombre = models.CharField(max_length=100)
    monto = models.FloatField(null=False, blank=False, default=0)
    plazo_fijo = models.ForeignKey(PlazoFijo, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class Operacion(models.Model):
    tipo = models.Choices('Deposito', 'Retiro')
    monto = models.FloatField(null=False, blank=False)
    fecha = models.DateField(null=False, blank=False)
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE)
    plazo = models.ForeignKey(PlazoFijo, on_delete=models.CASCADE)

    def __str__(self):
        return self.monto