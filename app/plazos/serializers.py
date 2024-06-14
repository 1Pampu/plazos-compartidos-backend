from rest_framework import serializers
from .models import PlazoFijo, Entidad

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
        exclude = ['plazo_fijo', 'monto']

class EntidadReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entidad
        exclude = ['plazo_fijo']