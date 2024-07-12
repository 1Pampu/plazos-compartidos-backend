from rest_framework import serializers
from django.utils import timezone
from .models import PlazoFijo, Entidad, Operacion

# Create your serializers here.
class PlazoFijoWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlazoFijo
        exclude = ['user', 'num_entidades', 'monto']

class PlazoFijoReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlazoFijo
        exclude = ['user']

class EntidadWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entidad
        exclude = ['plazo', 'monto']

class EntidadReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entidad
        exclude = ['plazo']

class OperacionReadSerializer(serializers.ModelSerializer):
    entidad_nombre = serializers.SerializerMethodField()

    class Meta:
        model = Operacion
        fields = ['tipo', 'monto', 'fecha', 'entidad_nombre']

    def get_entidad_nombre(self, obj):
        return obj.entidad.nombre

class OperacionWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operacion
        exclude = ['plazo', 'entidad', 'nuevo_monto']

    def validate_tipo(self, value):
        restricted_choices = ['Interes']
        if value in restricted_choices:
            raise serializers.ValidationError(f'{value} is not a valid choice')
        return value

    def validate_fecha(self, value):
        if value > timezone.localtime(timezone.now()).date():
            raise serializers.ValidationError('The date cannot be in the future')
        return value