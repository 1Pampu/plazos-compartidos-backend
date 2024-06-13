from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import PlazoFijoSerializer
from .models import PlazoFijo

# Create your views here.
class PlazoFijoView(APIView):
    [IsAuthenticated]

    def get(self, request):
        plazos = PlazoFijo.objects.all()
        serializer = PlazoFijoSerializer(plazos, many=True)
        return Response(serializer.data)