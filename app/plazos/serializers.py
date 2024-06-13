from rest_framework import serializers
from .models import PlazoFijo

# Create your serializers here.
class PlazoFijoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlazoFijo
        fields = '__all__'
        exclude = ['user']