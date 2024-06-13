from django.contrib import admin
from .models import PlazoFijo, Entidad, Operacion

# Register your models here.
admin.site.register(PlazoFijo)
admin.site.register(Entidad)
admin.site.register(Operacion)