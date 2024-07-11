from django.urls import path
from .views import PlazoFijoView, EntidadView, OperacionView

urlpatterns = [
    path('plazos', PlazoFijoView),
    path('plazos/<int:id>', PlazoFijoView),
    path('plazos/<int:id>/entidades', EntidadView),
    path('plazos/<int:id>/entidades/<int:id_entidad>', EntidadView),
    path('plazos/<int:id>/operaciones', OperacionView),
    path('plazos/<int:id>/operaciones/<int:id_entidad>', OperacionView),
]
