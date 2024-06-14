from django.urls import path
from .views import PlazoFijoView, EntidadView

urlpatterns = [
    path('plazos/', PlazoFijoView),
    path('plazos/<int:id>/', PlazoFijoView),
    path('plazos/<int:id>/entidades/', EntidadView),
    path('plazos/<int:id>/entidades/<int:id_entidad>/', EntidadView),
]
